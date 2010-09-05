from django.conf import settings
import threading
from jogging import logging
from datetime import datetime, timedelta
from sdb.social.models import Service, Entry
import simplejson as json


# registry of feeders
registry = {}

registry['delicious']        = lambda service: parse_generic_feed('http://feeds.delicious.com/v2/rss/%s', service, 'Delicious Bookmark', 'bookmark')
registry['twitter']          = lambda service: parse_generic_feed('http://twitter.com/statuses/user_timeline/%s.rss', service, 'Tweet', 'status')
registry['hypem']            = lambda service: parse_generic_feed('http://hypem.com/feed/loved/%s/1/feed.xml', service, 'Hypem Fav', 'fav')
registry['github']           = lambda service: parse_generic_feed('http://github.com/%s.atom', service, 'GitHub Activity', 'collab')
registry['disqus']           = lambda service: parse_generic_feed('http://disqus.com/%s/comments.rss', service, 'Disqus Update', 'comment')
registry['wakoopa']          = lambda service: parse_generic_feed('http://wakoopa.com/%s/newly_used.rss', service, 'Wakoopa Update', 'program')
registry['goodreads']        = lambda service: parse_generic_feed('http://www.goodreads.com/user/updates_rss/%s', service, 'GoodReads Update', 'book')
registry['getsatisfaction']  = lambda service: parse_url('http://api.getsatisfaction.com/people/%s/replies', service, lambda e: getsatisfaction_entry(e, service))
registry['stumbleupon']      = lambda service: parse_generic_feed('http://rss.stumbleupon.com/user/%s/favorites', service, 'StumbleUpon Fav', 'fav')
registry['lastfm']           = lambda service: update_lastfm(service)
registry['posterous']        = lambda service: update_posterous(service)
registry['flickr']           = lambda service: update_flickr(service)
registry['stackoverflow']    = lambda service: parse_generic_feed('http://stackoverflow.com/feeds/user/%s', service, 'Stack Overflow Activity', 'comment')
registry['dopplr']           = lambda service: parse_dopplr(service)


running_update = False
running_update_lock = threading.RLock()


def update():
  """ Updates all services which require an update. """

  global running_update
  global running_update_lock

  to_update = []
  services = Service.objects.all()

  for service in services:
    if registry.has_key(service.name):
      prev_update = service.updated
      if prev_update + timedelta(minutes=service.period) <= datetime.utcnow():
        to_update.append(service)
    else:
      logging.warning('updater for service %s not found' %service.name)

  running_update_lock.acquire()
  if not running_update and len(to_update) > 0:
    running_update = True  
    running_update_lock.release()
    msg = 'Thank you! %d services are scheduled for an update.' %len(to_update)
    if (settings.UPDATE_THREAD):
      UpdateThread(to_update).start()
    else:
      do_update(to_update)
  else:
    msg = 'Nothing to feed! All services are up-to-date. Thanks anyway!'

  return msg


def do_update(services):
  """ Updates the given services. """

  global running_update

  for service in services:
    feed = registry[service.name]
    try:
      entries = feed(service)
      # TODO should be in a transaction
      for entry in entries:
        entry.save()
      service.updated = datetime.utcnow()
      service.save()
    except:
      logging.exception(msg='updater exception for service %s' %service.name, exception=True)
  running_update = False
    

class UpdateThread ( threading.Thread ):
  """ Update thread for running an update as a background job. """
  
  def __init__(self, services=None):
    threading.Thread.__init__(self)
    self.services = services

  def run ( self ):
    do_update(self.services)


def update_flickr(service):
  import flickrapi
  entries = []
  prev_update = service.updated
  args = json.loads(service.args)
  flickr = flickrapi.FlickrAPI(args["key"])
  photos = flickr.people_getPublicPhotos(user_id=args["user"], extras='date_upload,url_sq')
  photos = photos.find('photos').findall('photo')
  new_photos = []
  for i in range(len(photos)):
    photo = photos[i]
    upload_date = datetime.utcfromtimestamp(int(photo.attrib["dateupload"]))
    if upload_date > prev_update:
      new_photos.append({'id':photo.attrib['id'], 'thumb':photo.attrib['url_sq'], 'url':"http://www.flickr.com/photos/%s/%s" % (args['user_name'], photo.attrib['id'])})
    if i == len(photos) - 1 or upload_date - timedelta(minutes=5) > datetime.utcfromtimestamp(int(photos[i+1].attrib["dateupload"])):
      if (len(new_photos) > 0):
        entry = Entry(uuid="TODO", service=service, desc='Flickr Update', data=json.dumps(new_photos), pub_date=upload_date, typ='photos')
        entries.append(entry)
      new_photos = []
  return entries


def update_posterous(service):
  import posterous
  entries = []
  args = json.loads(service.args)
  api = posterous.API()
  for post in api.read_posts(hostname=args["hostname"]):
    if post.date > service.updated:
      entry = Entry(uuid=post.id, service=service, desc='Posterous Post', data=json.dumps({"title":post.title, "url":post.link}), pub_date=post.date, typ='post')
      entries.append(entry)
  return entries


def update_lastfm(service):
  import lastfm
  entries = []
  args = json.loads(service.args) 
  api = lastfm.Api(args['api_key'])
  user = api.get_user(args['user'])
  tracks = user.get_recent_tracks()
  for track in tracks:
    if track.played_on > service.updated:
      entry = Entry(uuid=track.url, service=service, desc='Last.fm Update', data=json.dumps({'title':track.name, 'artist':track.artist.name, 'url':track.url, 'image':track.image['large']}), pub_date=track.played_on, typ='scrobble')
      entries.append(entry)
  return entries


def getsatisfaction_entry(entry, service):

  def get_attr(attr):
    return getattr(entry, attr) if hasattr(entry, attr) else ''

  if not hasattr(entry, 'title'):
    return None

  data = {'title' : get_attr('title'),
          'url' : get_attr('link'),
          'desc' : get_attr('description')}
  return Entry(uuid=entry.id, service=service, desc='Get Satifaction Reply', data=json.dumps(data), pub_date=datetime(*entry.updated_parsed[:6]), typ='comment')


def parse_dopplr(service):
  import feedparser
  return parse_feed(feedparser.parse('http://www.dopplr.com/traveller/sdb/feed/mytrips/%s/all' %json.loads(service.args)['feed']), service.updated, lambda e: dopplr_entry(e, service))


def dopplr_entry(entry, service):
  uuid = entry.id
  entries = Entry.objects.filter(uuid=uuid)
  if len(entries) > 0:
    return None
  data = {'title' : entry.title,
          'url' : entry.link}
  return Entry(uuid=entry.id, service=service, desc='Dopplr Activity', data=json.dumps(data), pub_date=datetime.utcnow(), typ='travel')


def generic_entry(entry, service, desc, typ):

  def get_attr(attr):
    return getattr(entry, attr) if hasattr(entry, attr) else ''

  if not hasattr(entry, 'title') or not hasattr(entry, 'link'):
    return None

  uuid = entry.id if hasattr(entry, 'id') else entry.link
  data = {'title' : get_attr('title'),
          'url' : get_attr('link'),
          'desc' : get_attr('description')}
  return Entry(uuid=uuid, service=service, desc=desc, data=json.dumps(data), pub_date=datetime(*entry.updated_parsed[:6]), typ=typ)


def parse_generic_feed(url, service, desc, typ):
  return parse_url(url, service, lambda e: generic_entry(e, service, desc, typ))


def parse_url(url, service, entry):
  import feedparser
  args = json.loads(service.args)
  return parse_feed(feedparser.parse(url %args['user']), service.updated, entry)


def parse_feed(feed, last_update, entry):
  """ Parses the given feed and returns all new entries after last_update. """

  entries = []
  for e in feed.entries:
    if datetime(*e.updated_parsed[:6]) > last_update:
      new = entry(e)
      if new != None:
        entries.append(new)
  return entries


