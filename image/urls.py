from django.contrib import admin
from django.urls import path, include
from image.views import ImageAPIView

urlpatterns = [
    path('api/v1/images/', ImageAPIView.as_view()),
]