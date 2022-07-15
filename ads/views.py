import json
from typing import Dict

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ads, Categories, User
from lesson_27 import settings


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


# ------------------------------ ADS -----------------------------------------------------------------------------------

@method_decorator(csrf_exempt, name="dispatch")
class AdsListViews(ListView):
    """Список всех объявлений"""
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # получаем список всех записей из БД
        # select_related - связь по первичному ключу, prefetch_related - связь many2many
        self.object_list = self.object_list.select_related('author').prefetch_related('categories').order_by("-price")

        # Пагинация
        paginator: Paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        # номер странице запрашиваемой пользователем
        pape_number: str = request.GET.get('page')
        # страница возвращенная объектом класса пагинации
        page: Paginator = paginator.get_page(pape_number)

        ads_result = []

        for ads in page:
            ads_result.append({'id': ads.id,
                               "name": ads.name,
                               'author': ads.author.first_name,
                               'price': ads.price,
                               'description': ads.description,
                               'address': ads.address,
                               'categories': list(map(str, ads.categories.all())),
                               'image': ads.image.url if ads.image else None
                               })

        response = {
            'items': ads_result,
            'num_pages': paginator.num_pages,
            'total': paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdsViewId(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Ads, id=self.kwargs['pk'])

        return JsonResponse({
            "id": obj.id,
            "name": obj.name,
            'author': obj.author.first_name,
            'price': obj.price,
            'description': obj.description,
            'address': obj.address,
            'is_published': obj.is_published,
            "categories": list(map(str, obj.categories.all())),
            'image': obj.image.url if obj.image else None
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdsCreateView(CreateView):
    """ Добавление нового объявления"""
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'address', 'is_published', 'categories']

    def post(self, request, *args, **kwargs):
        ads_data: Dict = json.loads(request.body)
        ads: Ads = Ads.objects.create(
            name=ads_data['name'],
            price=ads_data['price'],
            author=get_object_or_404(User, pk=ads_data['author_id']),
            description=ads_data['description'],
            address=ads_data['address'],
            is_published=ads_data['is_published'],
        )

        for cat in ads_data['categories']:
            cat_obj, _ = Categories.objects.get_or_create(name=cat)

        ads.categories.add(cat_obj)
        ads.save()

        return JsonResponse({
            'id': ads.id,
            'name': ads.name,
            'price': ads.price,
            'description': ads.description,
            'categories': list(map(str, ads.categories.all()))
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsUpdateView(UpdateView):
    """Изменение объявления"""

    model = Ads
    fields = ['name', 'price', 'description', 'address', 'is_published', 'categories']

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, *kwargs)
        ads_data = json.loads(request.body)

        self.object.name = ads_data['name']
        self.object.price = ads_data['price']
        self.object.description = ads_data['description']
        self.object.address = ads_data['address']
        self.object.is_published = ads_data['is_published']

        if ads_data["categories"]:
            for cat in ads_data['categories']:
                cat_obj, _ = Categories.objects.get_or_create(name=cat)
            self.object.categories.add(cat_obj)
        self.object.save()

        return JsonResponse({"Message": f"update ads with ID = {self.kwargs['pk']} is ok"}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class AdsAddImageView(UpdateView):
    """ Добавление картинки к объявлению """

    model = Ads
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'image': self.object.image.url if self.object.image else None

        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"Message": f"delete ads with ID = {self.kwargs['pk']} is ok"}, status=200)


# ----------------------- Categories ------------------------------------------------------------------------------------

@method_decorator(csrf_exempt, name="dispatch")
class CatListViews(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

        # Пагинация
        paginator: Paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        # номер странице запрашиваемой пользователем
        pape_number: str = request.GET.get('page')
        # страница возвращенная объектом класса пагинации
        page: Paginator = paginator.get_page(pape_number)

        cat_result = []

        for cat in page:
            cat_result.append({'id': cat.id,
                               "name": cat.name,
                               })

        response = {
            'items': cat_result,
            'num_pages': paginator.num_pages,
            'total': paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CatViewId(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Categories, id=self.kwargs['pk'])

        return JsonResponse({
            "id": obj.id,
            "name": obj.name
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CatCreateView(CreateView):
    model = Categories
    fields = ['name']
    def post(self, request, *args, **kwargs):
        cat_data: Dict = json.loads(request.body)
        cat = Categories.objects.create(
            name=cat_data['name']
        )

        return JsonResponse({"id": cat.id,
                             "name": cat.name
                             }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CatUpdateView(UpdateView):
    model = Categories
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, *kwargs)
        cat_data = json.loads(request.body)

        self.object.name = cat_data['name']
        self.object.save()
        return JsonResponse({"Message": f"update category with ID = {self.kwargs['pk']} is ok"}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CatDeleteView(DeleteView):
    model = Categories

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"Message": f"delete category with ID = {self.kwargs['pk']} is ok"}, status=200)
