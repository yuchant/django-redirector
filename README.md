django-redirector
=================

Django Redirector adds admin powered 301 redirects.


Installation
------------
Add the package to your python path, pip install, setup.py install, etc. 

Add `'django_redirects'` to `INSTALLED_APPS`

Add `'django_redirects.middleware.RedirectMiddleware'` immediately after `CommonMiddleware` in `MIDDLEWARE_CLASSES`

Syncdb, then navigate to your admin panel!


Settings
--------
``REDIRECT_CACHE_TIME``: _default: 60*10_
Seconds to cache individual page redirect results. 

Note that caches are invalidated automatically when a Redirect is saved or deleted.


