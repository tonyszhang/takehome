import logging

from django.http import HttpResponse, JsonResponse

logger = logging.getLogger(__name__)

def index(request):
    logger.debug('Request URL: %s%s', request.get_host(), request.get_full_path())

    if request.method == "POST":
        return HttpResponse("<p>POST not yet implemented.</p>")

    if request.META.get('HTTP_ACCEPT') == 'application/json':
        return JsonResponse({"message": "Hello, World"})

    return HttpResponse("<p>Hello, World</p>")
