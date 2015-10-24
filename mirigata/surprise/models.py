import logging
import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import models as auth
from django.utils import timezone
import requests
from shortuuidfield import ShortUUIDField


log = logging.getLogger(__name__)


class Surprise(models.Model):
    id = ShortUUIDField(primary_key=True, auto=True)
    link = models.URLField(max_length=500)
    description = models.TextField(max_length=1000)

    title = models.TextField(max_length=500, null=True, blank=True)
    author_name = models.TextField(max_length=500, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    creator = models.ForeignKey(auth.User, null=True, blank=True)
    metadata_retrieved = models.DateTimeField(null=True)

    link_exists = models.BooleanField(default=True, db_index=True)

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
        self.metadata_retrieved = timezone.now()

        self.save()


def get_random_surprise():
    query_set = Surprise.objects.exclude(link_exists=False)

    count = query_set.count()
    rnd = random.randint(0, count - 1)
    return query_set.all().order_by('id')[rnd]


def update_metadata(surprise):
    response = requests.get(settings.INFIKSI_BASE_URL, dict(q=surprise.link))

    if response.status_code == 404:
        log.warning("Got 404 while retrieving %s; link does not exist?", surprise.link)
        surprise.link_exists = False
        surprise.metadata_retrieved = timezone.now()
        surprise.save()
        return

    if response.status_code == 200:
        metadata = response.json()
        surprise.link_exists = True
        surprise.add_metadata(metadata)
        return

    # status_code is probably 504
    log.warning("Could not retrieve metadata for %s; received status code %d", surprise.link, response.status_code)
    return
