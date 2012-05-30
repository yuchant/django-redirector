"""
Redirect Middleware
-------------------

Get cached copy of redirects and apply if match found
# must be in memory - don't execute a DB call every time a page is hit

Created on Wednesday, May 2012 by Yuji Tomita
"""
import logging

from django import http

from django_redirector.models import Redirect

log = logging.getLogger(__name__)


class RedirectMiddleware(object):
	def process_request(self, request):
		try:
			redirect_url = Redirect.objects.get_redirect_for_path(request.path)
			if redirect_url:
				return http.HttpResponsePermanentRedirect(redirect_url)
		except Exception, e:
			# catch all exceptions -- this middleware is fired in all views.
			log.critical("Exception fired on Redirect Middleware catch all! {0}".format(e))
		return None