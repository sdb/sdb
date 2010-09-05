The Django project for my personal site. Still in early development.

## Features ##

### Social stream ###

* show updates from on-line services
* supports Twitter, Flickr, Delicious, Disqus, Wakoopa, GitHub, The Hype Machine, Posterous, GoodReads, Last.fm, Get Satisfaction, Stack Overflow, Dopplr, and StumbleUpon.
* filter by types of updates
* admin interface


## Dependencies ##

* [Django](http://www.djangoproject.com/) (1.2.1)
* [simplejson](http://code.google.com/p/simplejson/) (2.1.1)
* [jogging](http://github.com/zain/jogging) (0.2.2)
* [feedparser](http://www.feedparser.org/) (trunk) (optional)
* [posterous-python](http://github.com/nureineide/posterous-python) (trunk) (optional)
* [flickrapi](http://stuvel.eu/projects/flickrapi) (1.4.2) (optional)
* [python-lastfm](http://code.google.com/p/python-lastfm/) (trunk) (optional)


## Installation ##

This is a general overview of the steps to be taken to install the app. Note that at the moment this description is not yet complete.

First of all, install the required dependencies.

### Fresh ###

* setup a database for the application
* clone the repository with `git clone git://github.com/sdb/sdb.git`
* create a separate Django settings file (see [this Gist](http://gist.github.com/557667#file_settings_deployment.py) for an example settings for production purposes)
* sync the database with `python manage.py syncdb --settings=settings_deployment.py`

### Update ###

* in case of an update to the models, dump the current data to a file with `python manage.py dumpdata social > dump.json --settings=settings_deployment`
* pull the latest version from the repository with `git pull`
* update the settings file (if necessary)
* in case of an update to the models, reset the database with `python manage.py reset social --settings=settings_deployment`
* in case of an update to the models, import the old data with `python manage.py loaddata dump.json --settings=settings_deployment`

Note that this procedure doesn't always work, especially in those cases where new non-null fields are added to the models.

