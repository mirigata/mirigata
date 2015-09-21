from django.conf.urls import url
from website import views


urlpatterns = [
    url('^$', views.HomepageView.as_view(), name="homepage"),
    url('^add-surprise$', views.AddSurpriseView.as_view(), name="add-surprise"),

    url('^surprise/(?P<pk>\d+)$', views.SurpriseDetailView.as_view(), name="surprise-detail"),
]
