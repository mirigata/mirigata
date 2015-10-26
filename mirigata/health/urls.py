from django.conf.urls import url
from health import views


urlpatterns = [
    url('^ping$', views.ping, name="health_ping"),
    url('^health$', views.health, name="health_health"),
]

