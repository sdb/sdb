import flickrapi, posterous, feedparser
import simplejson as json
from datetime import datetime, timedelta
from sdb.social.models import Service, Entry


updaters = {
  'flickr' : lambda service: flickr(service),
  'twitter' : lambda service: twitter(service),
  'delicious' : lambda service: delicious(service),
  'hypem' : lambda service: hypem(service),
  'posterous' : lambda service: update_posterous(service),
  'github' : lambda service: github(service),
  'disqus' : lambda service: disqus(service),
}


def flickr(service):
  prev_update = service.updated
  args = json.loads(service.args)
  flickr = flickrapi.FlickrAPI(args["key"])
  photos = flickr.people_getPublicPhotos(user_id=args["user"], extras='date_upload,url_sq')
  photos = photos.find('photos').findall('photo')
  new_photos = []
  for i in range(len(photos)):
    photo = photos[i]
    upload_date = datetime.fromtimestamp(int(photo.attrib["dateupload"]))
    if upload_date > prev_update:
      new_photos.append({'id':photo.attrib['id'], 'thumb':photo.attrib['url_sq'], 'url':"http://www.flickr.com/photos/%s/%s" % (args['user_name'], photo.attrib['id'])})
    if i == len(photos) - 1 or upload_date - timedelta(minutes=5) > datetime.fromtimestamp(int(photos[i+1].attrib["dateupload"])):
      if (len(new_photos) > 0):
        entry = Entry(service=service, desc='Flickr Update', data=json.dumps(new_photos), pub_date=upload_date, typ='photos')
        entry.save()
      new_photos = []


def twitter(service):
  prev_update = service.updated
  args = json.loads(service.args)
  feed = feedparser.parse('http://twitter.com/statuses/user_timeline/' + args['user'] + '.rss')
  for msg in feed.entries:
    pub_date = datetime(*msg.updated_parsed[:6])
    if pub_date > prev_update:
      entry = Entry(service=service, desc='Twitter Update', data=json.dumps({'title':msg.title, 'url':msg.link}), pub_date=pub_date, typ='status')
      entry.save()


def delicious(service):
  prev_update = service.updated
  args = json.loads(service.args)
  feed = feedparser.parse('http://feeds.delicious.com/v2/rss/' + args['user'])
  service.updated = datetime.utcnow()
  for msg in feed.entries:
    pub_date = datetime(*msg.updated_parsed[:6])
    if pub_date > prev_update:
      entry = Entry(service=service, desc='Delicious Bookmark', data=json.dumps({'title':msg.title, 'url':msg.link}), pub_date=pub_date, typ='bookmark')
      entry.save()


def hypem(service):
  prev_update = service.updated
  args = json.loads(service.args)
  feed = feedparser.parse('http://hypem.com/feed/loved/' + args['user'] + '/1/feed.xml')
  for msg in feed.entries:
    pub_date = datetime(*msg.updated_parsed[:6])
    if pub_date > prev_update:
      entry = Entry(service=service, desc='Hypem Fav', data=json.dumps({'title':msg.title, 'url':msg.link}), pub_date=pub_date, typ='fav')
      entry.save()


def update_posterous(service):
  prev_update = service.updated
  args = json.loads(service.args)
  api = posterous.API()
  for post in api.read_posts(hostname=args["hostname"]):
    if post.date > prev_update:
      entry = Entry(service=service, desc='Posterous Post', data=json.dumps({"title":post.title, "url":post.link}), pub_date=post.date, typ='post')
      entry.save()


def github(service):
  prev_update = service.updated
  args = json.loads(service.args)
  feed = feedparser.parse('http://github.com/' + args['user'] + '.atom')
  for msg in feed.entries:
    pub_date = datetime(*msg.updated_parsed[:6])
    if pub_date > prev_update:
      entry = Entry(service=service, desc='Github Activity', data=json.dumps({'title':msg.title, 'url':msg.link}), pub_date=pub_date, typ='collab')
      entry.save()


def disqus(service):
  prev_update = service.updated
  args = json.loads(service.args)
  feed = feedparser.parse('http://disqus.com/' + args['user'] + '/comments.rss')
  for msg in feed.entries:
    pub_date = datetime(*msg.updated_parsed[:6])
    if pub_date > prev_update:
      entry = Entry(service=service, desc='Disqus Update', data=json.dumps({'title':msg.title, 'url':msg.link, 'desc':msg.description}), pub_date=pub_date, typ='comment')
      entry.save()

