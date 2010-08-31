## Features ##

### Social stream ###

* show updates from your on-line services
* supports Twitter, Flickr, Delicious, Disqus, Wakoopa, GitHub, The Hype Machine, Posterous, GoodReads and Last.fm.
* filter by types of updates
* admin interface


## Dependencies ##

* [Django](http://www.djangoproject.com/) (1.2.1)
* [flickrapi](http://stuvel.eu/projects/flickrapi) (1.4.2)
* [simplejson](http://code.google.com/p/simplejson/) (2.1.1)
* [feedparser](http://www.feedparser.org/) (trunk)
* [posterous-python](http://github.com/nureineide/posterous-python) (trunk)
* [jogging](http://github.com/zain/jogging) (0.2.2)
* [python-lastfm](http://code.google.com/p/python-lastfm/) (trunk)


## Installation ##

This is a general overview of the steps to be taken to install the app. Note that at the moment this description is not yet complete.

If not done yet, install the required dependencies.

### Fresh ###

* setup a database for the application
* clone the repository with `git clone git://github.com/sdb/sdb.git`
* create a separate Django settings file (see [this Gist](http://gist.github.com/557667#file_settings_deployment.py) for an example settings for production purposes)
* sync the database with `python manage.py syncdb --settings=settings_deployment.py`

### Update ###

* in case of an update to the models, dump the current data to a file with `python manage.py dumpdata social > dump.json --settings=settings_deployment`
* pull the latest version from the repository with `git pull`
* update the settings file (if necessary)
* in case of an update to the models, reset the database with `python manage.py reset social > dump.json --settings=settings_deployment`
* in case of an update to the models, import the old data with `python manage.py loaddata dump.json --settings=settings_deployment`

Note that this procedure doesn't always work, especially in those cases where new non-null fields are added to the models.

