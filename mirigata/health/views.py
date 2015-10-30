from django.conf import settings
from django.db import OperationalError
from django.http import HttpResponse
import requests
from health import models


def ping(request):
    return HttpResponse("ok", content_type="text/plain")


def health(request):
    # check database connection
    try:
        models.HealthCheck.objects.all().count()
    except OperationalError:
        return HttpResponse("db-fail", content_type="text/plain", status=500)

    # check infiksi connection
    infiksi_url = "{}status/ping".format(settings.INFIKSI_BASE_URL)
    try:
        response = requests.get(infiksi_url)
        response.raise_for_status()
    except:
        return HttpResponse("infiksi-fail", content_type="text/plain", status=500)

    return HttpResponse("ok", content_type="text/plain")
