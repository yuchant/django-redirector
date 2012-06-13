from django.contrib import admin

from django_redirector.models import Redirect, RedirectGroup


class RedirectAdmin(admin.ModelAdmin):
    list_display = ('group', 'match_path', 'match_type')
    list_display_links = list_display
    list_filter = ('group',)
    actions = [
        'action_disable',
        'action_enable',
    ]

    def action_disable(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, "Disabled {0} redirects".format(count))
    action_disable.short_description = 'Disable Selected Redirects'

    def action_enable(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, "Enabled {0} redirects".format(count))       
    action_enable.short_description = 'Enable Selected Redirects'

admin.site.register(Redirect, RedirectAdmin)
admin.site.register(RedirectGroup)