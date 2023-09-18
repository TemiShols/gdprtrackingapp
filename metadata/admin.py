from django.contrib import admin
from .models import Chrome, Download, LoginItem, LocalStorage


class ChromeAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'pc_username', 'user')


class LoginItemAdmin(admin.ModelAdmin):
    list_display = ('creation_time', 'user', 'name', 'value')


class LocalStorageAdmin(admin.ModelAdmin):
    list_display = ('date', 'origin', 'key', 'value',)


class DownloadAdmin(admin.ModelAdmin):
    list_display = ('download_url', 'user', 'download_target_path', 'download_danger_type',)


admin.site.register(Chrome, ChromeAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(LocalStorage, LocalStorageAdmin)
admin.site.register(LoginItem, LoginItemAdmin)
