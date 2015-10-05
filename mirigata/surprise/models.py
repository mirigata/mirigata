import random
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import models as auth
from shortuuidfield import ShortUUIDField


class Surprise(models.Model):
    id = ShortUUIDField(primary_key=True, auto=True)
    link = models.URLField(max_length=500)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(auth.User, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('surprise-detail', kwargs={"pk": self.id})


def get_random_surprise():
    count = Surprise.objects.count()
    rnd = random.randint(0, count-1)
    return Surprise.objects.all().order_by('id')[rnd]

