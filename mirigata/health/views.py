from django.http import HttpResponse


def ping(request):
    return HttpResponse("ok", content_type="text/plain")


def health(request):
    return HttpResponse("ok", content_type="text/plain")
