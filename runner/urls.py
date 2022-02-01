from django.urls import path, re_path

from runner import views

urlpatterns = [
    path('', views.index, name='index'),
]
