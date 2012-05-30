from django.contrib import admin

from django_redirector.models import Redirect, RedirectGroup


class RedirectAdmin(admin.ModelAdmin):
	list_display = ('group', 'match_path', 'match_type')
	list_display_links = list_display
	list_filter = ('group',)


admin.site.register(Redirect, RedirectAdmin)
admin.site.register(RedirectGroup)