from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from surprise import models


def update_metadata(model_admin, request, queryset):
    for surprise in queryset:
        models.update_metadata(surprise)

update_metadata.short_description = "Update metadata"


class SurpriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'metadata_retrieved', 'link_exists')
    actions = [update_metadata]


admin.site.register(models.Surprise, SurpriseAdmin)
admin.site.register(models.Comment, MPTTModelAdmin)
