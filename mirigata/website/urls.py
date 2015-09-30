from django.conf.urls import url
from website import views


urlpatterns = [
    url('^$', views.HomepageView.as_view(), name="homepage"),
    url('^add-surprise$', views.AddSurpriseView.as_view(), name="add-surprise"),

    url('^surprise/random$', views.RandomSurpriseView.as_view(), name="random-surprise"),
    url('^surprise/(?P<pk>[a-zA-Z0-9]+)$', views.SurpriseDetailView.as_view(), name="surprise-detail"),

    url('^system/error$', views.error)
]

