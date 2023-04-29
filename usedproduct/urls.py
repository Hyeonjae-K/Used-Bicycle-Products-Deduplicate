from django.urls import path

from usedproduct import views

urlpatterns = [
    path('', views.index),
]
