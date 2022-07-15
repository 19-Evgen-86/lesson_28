import json
from typing import List, Dict

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from lesson_27 import settings
from users.models import User, Location


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('location_id').order_by('username').filter(
            ads__is_published=True).annotate(
            num_ads=Count('ads'))

        paginate: Paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number: str = request.GET.get('page')
        page: Paginator = paginate.get_page(page_number)

        user: User
        users_result: List = []

        for user in page:
            users_result.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": user.location_id.name,
                "ads": user.num_ads,

            })
        response = {
            "items": users_result,
            "num_pages": paginate.num_pages,
            'total': paginate.count
        }
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        obj: User = get_object_or_404(User, id=self.kwargs['pk'])

        return JsonResponse({
            "id": obj.id,
            "username": obj.username,
            "first_name": obj.first_name,
            'last_name': obj.last_name,
            'age': obj.age,
            'role': obj.role,
            'location': obj.location_id.name,
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location_id']

    def post(self, request, *args, **kwargs):
        user_data: Dict = json.loads(request.body)
        user: User = User.objects.create(
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role'],
            age=user_data['age'],

        )

        user.location_id, _ = Location.objects.get_or_create(name=user_data['location'])

        user.save()

        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location': user.location_id.name
        }, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location_id']

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, *kwargs)
        user_data = json.loads(request.body)

        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.username = user_data['username']
        self.object.role = user_data['role']
        self.object.age = user_data['age']
        self.object.location_id, _ = Location.objects.get_or_create(name=user_data['location'])

        if user_data['password']:
            self.object.password = user_data['password']

        self.object.save()

        return JsonResponse({"Message": f"update user with ID = {self.kwargs['pk']} is ok"}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"Message": f"delete user with ID = {self.kwargs['pk']} is ok"}, status=200)


# ----------------------- location --------------------------------------------------------------------------------------


@method_decorator(csrf_exempt, name="dispatch")
class LocListViews(ListView):
    model = Location

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator: Paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        pape_number: str = request.GET.get('page')
        page: Paginator = paginator.get_page(pape_number)

        loc_result: List = []
        location: Location
        for location in page:
            loc_result.append({'id': location.id,
                               "name": location.name,
                               })

        response = {
            'items': loc_result,
            'num_pages': paginator.num_pages,
            'total': paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class LocViewId(DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        obj: Location = get_object_or_404(Location, id=self.kwargs['pk'])

        return JsonResponse({
            "id": obj.id,
            "name": obj.name,
            'lat': obj.lat,
            'lng': obj.lng,
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class LocCreateView(CreateView):
    model = Location
    fields = ['name', 'lat', 'lng']

    def post(self, request, *args, **kwargs):
        loc_data: Dict = json.loads(request.body)
        loc: Location = Location.objects.create(
            name=loc_data['name'],
            lng=loc_data['lng'],
            lat=loc_data['lat']
        )

        return JsonResponse({"id": loc.id,
                             "name": loc.name
                             }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class LocUpdateView(UpdateView):
    model = Location
    fields = ['name', 'lat', 'lng']

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, *kwargs)
        loc_data: Dict = json.loads(request.body)

        if loc_data["name"]:
            self.object.name = loc_data['name']

        self.object.lat = loc_data['lat']
        self.object.lng = loc_data['lng']
        self.object.save()

        return JsonResponse({"Message": f"update location with ID = {self.kwargs['pk']} is ok"}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class LocDeleteView(DeleteView):
    model = Location

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"Message": f"delete Location with ID = {self.kwargs['pk']} is ok"}, status=200)
