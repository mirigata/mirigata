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

    def _update(self, attr, metadata, *fields):
        value = None
        for field in fields:
            value = metadata.get(field)
            if value:
                break

        if value:
            setattr(self, attr, value)

    def add_metadata(self, d):
        self._update('link', d, 'canonical_url')
        self._update('description', d, 'description')
        self._update('author_name', d, 'author_name')
        self._update('thumbnail_url', d, 'og_image')
        self._update('title', d, 'og_title', 'title')

        self.save()


def get_random_surprise():
    count = Surprise.objects.count()
    rnd = random.randint(0, count - 1)
    return Surprise.objects.all().order_by('id')[rnd]


def update_metadata(surprise):
    response = requests.get(settings.INFIKSI_BASE_URL, dict(q=surprise.link))
    response.raise_for_status()     # TODO: Handle this gracefully

    metadata = response.json()
    surprise.add_metadata(metadata)
