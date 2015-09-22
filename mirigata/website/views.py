import random

from django.core.urlresolvers import reverse
from django.views import generic

from surprise import models


class HomepageView(generic.TemplateView):
    template_name = "website/index.html"


class AddSurpriseView(generic.CreateView):
    template_name = "website/add-surprise.html"
    model = models.Surprise
    fields = ('link', 'description')


class SurpriseDetailView(generic.DetailView):
    template_name = "website/surprise-detail.html"
    model = models.Surprise


class RandomSurpriseView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        count = models.Surprise.objects.count()
        rnd = random.randint(0, count-1)
        surprise = models.Surprise.objects.all().order_by('id')[rnd]

        return reverse("surprise-detail", kwargs=dict(pk=surprise.id))
