from django.contrib import admin

from .models import CustomUser, UserConfiguration


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'last_login', 'is_active')

    def full_name(self, obj):
        return '%s %s' % (obj.first_name, obj.last_name)


class UserConfigurationAdmin(admin.ModelAdmin):
    list_display = ('user', 'pt_token')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserConfiguration, UserConfigurationAdmin)
