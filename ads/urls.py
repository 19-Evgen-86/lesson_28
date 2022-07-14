from django.urls import path

from ads.views import *

urlpatterns = [
    path('', AdsListViews.as_view()),
    path('<int:pk>/', AdsViewId.as_view()),
    path('create/', AdsCreateView.as_view()),
    path('update/<int:pk>/', AdsUpdateView.as_view()),
    path('update/<int:pk>/upload_image/', AdsAddImageView.as_view()),
    path('delete/<int:pk>/', AdsDeleteView.as_view()),
    path('cat/', CatListViews.as_view()),
    path('cat/<int:pk>/', CatViewId.as_view()),
    path('cat/create/', CatCreateView.as_view()),
    path('cat/update/<int:pk>/', CatUpdateView.as_view()),
    path('cat/delete/<int:pk>/', CatDeleteView.as_view()),
]
