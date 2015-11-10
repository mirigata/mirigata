from braces import views as braces
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages import views
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic

from surprise import models, forms


class HomepageView(generic.TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['surprises'] = models.Surprise.objects.exclude(link_exists=False).order_by('-created')

        return ctx


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

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['vote'] = models.Vote.objects.get_vote_for(
            user=self.request.user,
            surprise_id=self.kwargs['pk'],
        )
        return result

    def get_queryset(self):
        return models.Surprise.objects.select_related('creator')


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


class _SurpriseVoteView(braces.LoginRequiredMixin, generic.View):
    form_class = None

    def post(self, request, *args, pk=None, **kwargs):
        # noinspection PyCallingNonCallable
        form = self.form_class(dict(
            surprise_id=pk
        ))
        form.full_clean()
        form.execute(user=self.request.user)
        return redirect(reverse("surprise-detail", args=(pk,)))


class SurpriseUpvoteView(_SurpriseVoteView):
    form_class = forms.UpvoteCommand


class SurpriseDownvoteView(_SurpriseVoteView):
    form_class = forms.DownvoteCommand


class SurpriseHistoryView(generic.DetailView):
    template_name = "website/surprise-history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = self.get_object().votes.order_by('-created')
        return context

    def get_queryset(self):
        return models.Surprise.objects.select_related('creator')
