from django.conf.urls import url
from website import views


urlpatterns = [
    url('^$', views.HomepageView.as_view(), name="homepage")
]
