import logging
import random
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import models as auth
from django.utils import timezone
import requests
from shortuuidfield import ShortUUIDField


log = logging.getLogger(__name__)


class SurpriseManager(models.Manager):

    def get_surprises_for_homepage(self):
        return self.filter(link_exists=True).order_by('-created').select_related('creator')


class Surprise(models.Model):
    id = ShortUUIDField(primary_key=True, auto=True)
    link = models.URLField(max_length=500)
    description = models.TextField(max_length=1000)

    points = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    title = models.TextField(max_length=500, null=True, blank=True)
    author_name = models.TextField(max_length=500, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    creator = models.ForeignKey(auth.User, null=True, blank=True)
    metadata_retrieved = models.DateTimeField(null=True)

    link_exists = models.BooleanField(default=True, db_index=True)

    objects = SurpriseManager()

    def __str__(self):
        return "Surprise({}, {})".format(self.id, self.link)

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


class VoteManager(models.Manager):

    def get_vote_for(self, user, surprise_id):
        if not user or not user.is_authenticated():
            return None

        result = self.filter(user=user, surprise__id=surprise_id)
        if result:
            return result[0]
        else:
            return None

    def get_history_for(self, surprise_id):
        return self.filter(surprise__id=surprise_id).order_by('-created').select_related('user')


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(auth.User)
    surprise = models.ForeignKey(Surprise, related_name="votes")
    amount = models.SmallIntegerField(choices=((1, 'Up'), (-1, 'Down')))
    created = models.DateTimeField(auto_now_add=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'surprise')

    def is_upvote(self):
        return self.amount > 0

    def is_downvote(self):
        return self.amount < 0
