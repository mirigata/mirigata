from django.contrib.messages import views

from django.core.urlresolvers import reverse
from django.views import generic

from surprise import models, forms


class HomepageView(generic.TemplateView):
    template_name = "website/index.html"


class AddSurpriseView(views.SuccessMessageMixin, generic.CreateView):
    template_name = "website/add-surprise.html"
    model = models.Surprise
    form_class = forms.CreateSurpriseForm

    success_message = "Your surprise has been added to our collection! Thank you. "


class SurpriseDetailView(generic.DetailView):
    template_name = "website/surprise-detail.html"
    model = models.Surprise


class RandomSurpriseView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        surprise = models.get_random_surprise()
        return reverse("surprise-detail", kwargs=dict(pk=surprise.id))
