from django.contrib import admin
from .models import News,Youtube,Ads,SiteSettings,Tag,Author
from django.contrib.auth.models import Group


admin.site.unregister(Group)
admin.site.register(News)
admin.site.register(Youtube)
admin.site.register(Ads)
admin.site.register(Tag)
admin.site.register(Author)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['show_jobs', 'show_youtube']