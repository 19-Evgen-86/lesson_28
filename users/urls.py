from django.urls import path

from users.views import *

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('update/<int:pk>/', UserUpdateView.as_view()),
    path('delete/<int:pk>/', UserDeleteView.as_view()),
    path('loc/', LocListViews.as_view()),
    path('loc/<int:pk>/', LocViewId.as_view()),
    path('loc/create/', LocCreateView.as_view()),
    path('loc/update/<int:pk>/', LocUpdateView.as_view()),
    path('loc/delete/<int:pk>/', LocDeleteView.as_view()),

]
