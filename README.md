django-redirector
=================

Django Redirector adds simple admin powered 301 redirects.


Example rules:
Path: /foo/bar/
Type: Exact (case insensitive) 

Path: /products/
Type: Startswith

Uses caching heavily since the middleware is called on every request.

1: redirect rules are cached once
2: redirect results are cached per request path

Cache is invalidated when a new rule is saved/added.


Installation
------------
Add the package to your python path, pip install, setup.py install, etc. 

Add `'django_redirects'` to `INSTALLED_APPS`

Add `'django_redirects.middleware.RedirectMiddleware'` immediately after `CommonMiddleware` in `MIDDLEWARE_CLASSES`

Syncdb, then navigate to your admin panel!


Settings
--------
``REDIRECT_CACHE_TIME``: _default: 60*30_
Seconds to cache individual page redirect results. 

