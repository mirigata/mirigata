from django.contrib import admin

from surprise import models


def update_metadata(model_admin, request, queryset):
    for surprise in queryset:
        models.update_metadata(surprise)

update_metadata.short_description = "Update metadata"


class SurpriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'link',)
    actions = [update_metadata]


admin.site.register(models.Surprise, SurpriseAdmin)
