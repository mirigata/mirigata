from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages import views
from django.core.urlresolvers import reverse
from django.views import generic
from braces import views as braces

from surprise import models, forms


class HomepageView(generic.TemplateView):
    template_name = "website/index.html"


class AddSurpriseView(views.SuccessMessageMixin, braces.LoginRequiredMixin, generic.FormView):
    template_name = "website/add-surprise.html"
    form_class = forms.CreateSurpriseCommand

    success_message = "Your surprise has been added to our collection! Thank you. "

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.execute(self.request.user)
        return super().form_valid(form)


class SurpriseDetailView(generic.DetailView):
    template_name = "website/surprise-detail.html"
    model = models.Surprise


class RandomSurpriseView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        surprise = models.get_random_surprise()
        return reverse("surprise-detail", kwargs=dict(pk=surprise.id))


def error(request):
    raise ValueError("Expected error")


class SignupView(views.SuccessMessageMixin, generic.CreateView):
    form_class = UserCreationForm
    template_name = "website/signup.html"
    success_url = "/"

    success_message = "Thank you for signing up!"

    def form_valid(self, form):
        result = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        login(self.request, user)
        return result
