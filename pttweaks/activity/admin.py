from django.contrib import admin
from django.utils.html import format_html

from .models import ActivityChangeLog
from .story_manager import story_manager


class ActivityChangeLogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'project_link_display', 'story_link_display', 'changes_display', 'created', 'is_reverted'
    )
    actions = ['revert_accepted_date_change']
    list_filter = ['project_id', 'created', 'is_reverted']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changes_display(self, obj):
        changes = obj.changes
        return '\n'.join([
            'Change on "{field}": From "{from_val}" to "{to_val}"'.format(
                field=key,
                from_val=val['old'],
                to_val=val['new']
            ) for key, val in changes.items()
        ])
    changes_display.short_description = 'Changes'

    def story_link_display(self, obj):
        return format_html('<a href="https://www.pivotaltracker.com/story/show/{id}" target="_blank">{id}</a>'.format(
            id=obj.story_id
        ))
    story_link_display.short_description = 'PT Story'

    def project_link_display(self, obj):
        return format_html('<a href="https://www.pivotaltracker.com/n/projects/{id}" target="_blank">{id}</a>'.format(
            id=obj.project_id
        ))
    project_link_display.short_description = 'PT Project'

    def revert_accepted_date_change(self, request, queryset):
        count = 0
        for activity_change_log in queryset:
            new_accepted_at = activity_change_log.changes['accepted_at']['old'] if not activity_change_log.is_reverted \
                else activity_change_log.changes['accepted_at']['new']
            activity_change_log.is_reverted = not activity_change_log.is_reverted

            story_manager.update_story(
                activity_change_log.project_id,
                activity_change_log.story_id,
                accepted_at=new_accepted_at,
            )
            activity_change_log.save()
            count += 1
        message_bit = '1 change was' if count == 1 else '%s changes were' % count
        self.message_user(request, '%s successfully reverted' % message_bit)
    revert_accepted_date_change.short_description = 'Revert accepted date change'


admin.site.register(ActivityChangeLog, ActivityChangeLogAdmin)
