import flickrapi, threading

from sdb.social.models import Service
from sdb.photos.models import Photo


running_sync = False
running_sync_lock = threading.RLock()


def sync():
  global running_sync
  global running_sync_lock

  running_sync_lock.acquire()
  if not running_sync:
    running_sync = True
    running_sync_lock.release()
    SyncThread().start()
    
    

class SyncThread ( threading.Thread ):
  
  def __init__(self):
    threading.Thread.__init__(self)

  def run ( self ):
    global running_sync

    # check that service exists, if not throw exception ?
    service = Service.objects.get(name='flickr')
    flickr = flickrapi.FlickrAPI(service.args['key'])
    photos = flickr.photos_search(user_id=service.args["user"],
                                tags='fav',
                                sort='date-taken-desc',
                                extras='description,date_upload,date_taken,url_sq,tags,url_t,url_s,url_m,url_o')
    Photo.objects.all().delete()
    [p.save() for p in map(lambda p: map_photo(p), photos.find('photos').findall('photo'))]
    running_sync = False


def map_photo(p):
  photo = Photo(photo_id=p.attrib['id'],
                title=p.attrib['title'],
                date_taken=p.attrib['datetaken'],
                data=p.attrib)
  desc = p.find('description').text
  photo.description = desc if desc != None else ''
  return photo
