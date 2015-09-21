from django.views import generic

class HomepageView(generic.TemplateView):
    template_name = "website/index.html"


class AddSurpriseView(generic.TemplateView):
    template_name = "website/add-surprise.html"
