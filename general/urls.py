from django.urls import re_path, path

from general import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('contact', views.contact, name='contact'),
    path('test/fizzbuzz-python', views.fizzbuzz_python, name='fizzbuzz_python'),
    path('test/coding-assessment-tool', views.coding_assessment_tool, name='coding_assessment_tool'),
    path('test/widget', views.widget, name='widget'),
    path('test/fizzbuzz-python', views.fizzbuzz_python, name='fizzbuzz-python'),

    path('tutorial/python_tutorial1', views.python_tutorial1, name='python_tutorial1'),
]
