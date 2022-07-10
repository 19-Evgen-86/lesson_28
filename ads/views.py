import json
from collections import defaultdict
from typing import List, Dict

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ads, Categories


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdsViews(View):
    def get(self, request):
        result: List = []
        db_data = Ads.objects.all()
        for row in db_data:
            result.append({
                "id": row.id,
                "name": row.name,
                'author': row.author,
                'price': row.price,
                'description': row.description,
                'address': row.address,
                'is_published': row.is_published
            })
        return JsonResponse(result, safe=False)

    def post(self, request):

        response: Dict = defaultdict(lambda: 0)
        post_data: Dict = json.loads(request.body)
        ads = Ads()

        ads.name = post_data['name']
        ads.author = post_data['author']
        ads.price = post_data['price']
        ads.address = post_data['address']
        ads.description = post_data['description']
        ads.is_published = post_data['is_published']
        ads.save()

        for key, value in post_data.items():
            response[key] = value

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CatViews(View):
    def get(self, request):
        result: List = []
        db_data = Categories.objects.all()
        for row in db_data:
            result.append({
                "id": row.id,
                "name": row.name,
            })
        return JsonResponse(result, safe=False)

    def post(self, request):

        response: Dict = defaultdict(lambda: 0)
        post_data: Dict = json.loads(request.body)
        cat = Categories()

        cat.name = post_data['name']
        cat.save()

        for key, value in post_data.items():
            response[key] = value

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdsViewId(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Ads, id=self.kwargs['pk'])

        return JsonResponse({
            "id": obj.id,
            "name": obj.name,
            'author': obj.author,
            'price': obj.price,
            'description': obj.description,
            'address': obj.address,
            'is_published': obj.is_published
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CatViewId(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Categories, id=self.kwargs['pk'])

        return JsonResponse({
            "id": obj.id,
            "name": obj.name
        }, safe=False)
