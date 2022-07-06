from django.http import JsonResponse, HttpResponse


def index(request):
    return JsonResponse({"status": "ok"}, status=200)
