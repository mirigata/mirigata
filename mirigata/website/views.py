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
