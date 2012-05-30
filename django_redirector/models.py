"""
Django Admin Powered Redirects
----------------

Todo: determine if target URL in redirect loop and prevent saving.

Created on Wednesday, May 2012 by Yuji Tomita
"""
import logging

from functools import partial

from django.db import models
from django.conf import settings
from django.core.cache import cache


REDIRECT_CACHE_TIME = getattr(settings, 'REDIRECT_CACHE_TIME', 60*30)

CACHE_PREFIX = 'REDIRECT'
CACHE_GENERATION_KEY = '-'.join([CACHE_PREFIX, 'GENERATION'])

log = logging.getLogger(__name__)


def generate_cache_prefix():
    """
    Generate cache prefix with generation number
    """
    generation = cache.get(CACHE_GENERATION_KEY, 0)
    return '-'.join([CACHE_PREFIX, str(generation)])


class RedirectGroup(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return u'{self.name}'.format(self=self)


class RedirectManager(models.Manager):
    def get_redirect_for_path(self, path, cached=True):
        """ 
        Get all matching redirects for given request path.
        Keep objects small - tuples.

        redirect[0] = path
        redirect[1] = type
        redirect[2] = target
        """
        cache_key = '-'.join([generate_cache_prefix(), path])
        redirect_url = cache.get(cache_key)
        print 'cache key ', cache_key, ' returned ', redirect_url

        if redirect_url:
            return redirect_url

        # determine if this url has a redirect
        redirects = filter(partial(self.get_matches, path), self._get_cached_redirects())
        redirects.sort(key=lambda x: -len(x[0]))

        if redirects:
            # prioritize exact matches first sorted by length of match
            try:
                redirect = filter(partial(self.exact, path), redirects)[0]
            except IndexError:
                redirect = redirects[0]
            redirect_url = redirect[2]
        cache.set(cache_key, redirect_url, 1) # set redirect_url for future
        return redirect_url

    def _get_cached_redirects(self):
        cache_key = '-'.join([generate_cache_prefix(), 'REDIRECTS-LIST'])
        redirects = cache.get(cache_key)
        if not redirects:
            redirects = list(self.filter(is_active=True).values_list('match_path', 'match_type', 'redirect_url'))
            cache.set(cache_key, redirects)
        return redirects

    def get_matches(self, path, data):
        match_path = data[0]
        match_type = data[1]
        try:
            match_func = getattr(self, match_type)
        except AttributeError:
            log.warn("Match type {0} has no corresponding method in middleware".format(match_type))
        if match_func:
            return match_func(path, match_path)
        return False

    def exact(self, path, match_path):
        return path == match_path

    def iexact(self, path, match_path):
        return path.lower() == match_path.lower()

    def startswith(self, path, match_path):
        return path.startswith(match_path)

    def istartswith(self, path, match_path):
        return path.lower().startswith(match_path.lower())

    def endswith(self, path, match_path):
        return path.endswith(match_path)

    def iendswith(self, path, match_path):
        return path.lower().endswith(match_path.lower())


class Redirect(models.Model):
    MATCH_TYPE_CHOICES = [
        ('exact', 'Exact'),
        ('iexact', 'Exact (case insensitive)'),
        ('startswith', 'Starts with'),
        ('istartswith', 'Starts with (case insensitive)'),
        ('endswith', 'Ends with'),
        ('iendswith', 'Ends with (case insensitive)'),
    ]
    is_active = models.BooleanField(default=True, blank=True, help_text="Is rule active?")
    group = models.ForeignKey(RedirectGroup, blank=True, null=True)
    match_path = models.CharField(max_length=256, help_text="URL path to match")
    match_type = models.CharField(max_length=256, choices=MATCH_TYPE_CHOICES)

    redirect_url = models.CharField(max_length=256)

    objects = RedirectManager()

    def __unicode__(self):
        return u'{self.match_path}'.format(self=self)


def clear_redirect_cache(sender, instance, **kwargs):
    """
    Invalidate all cache on redirect save / delete.
    """
    generation = cache.get(CACHE_GENERATION_KEY)
    if generation is None:
        cache.set(CACHE_GENERATION_KEY, 0)
    cache.incr(CACHE_GENERATION_KEY)


models.signals.post_save.connect(clear_redirect_cache, sender=Redirect)
models.signals.post_delete.connect(clear_redirect_cache, sender=Redirect)
