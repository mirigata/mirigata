from django.contrib import admin
from surprise import models

class SurpriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', )


admin.site.register(models.Surprise, SurpriseAdmin)
