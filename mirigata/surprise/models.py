import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import models as auth
import requests
from shortuuidfield import ShortUUIDField


class Surprise(models.Model):
    id = ShortUUIDField(primary_key=True, auto=True)
    link = models.URLField(max_length=500)
    description = models.TextField(max_length=1000)

    title = models.TextField(max_length=500, null=True, blank=True)
    author_name = models.TextField(max_length=500, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    creator = models.ForeignKey(auth.User, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('surprise-detail', kwargs={"pk": self.id})

    def add_metadata(self, d):
        canonical_url = d.get('canonical_url')
        if canonical_url:
            self.link = canonical_url

        title = d.get('og_title')
        if not title:
            title = d.get('title')
        if title:
            self.title = title

        description = d.get('description')
        if description:
            self.description = description

        author = d.get('author_name')
        if author:
            self.author_name = author

        thumbnail = d.get('og_image')
        if thumbnail:
            self.thumbnail_url = thumbnail

        self.save()


def get_random_surprise():
    count = Surprise.objects.count()
    rnd = random.randint(0, count - 1)
    return Surprise.objects.all().order_by('id')[rnd]


def update_metadata(surprise):
    response = requests.get(settings.INFIKSI_BASE_URL, dict(q=surprise.link))
    response.raise_for_status()

    metadata = response.json()
    surprise.add_metadata(metadata)
