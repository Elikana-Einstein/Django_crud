from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.task_list, name='task_list'),
    path('register/', views.register, name='register'),
    path('create/', views.task_create, name='task_create'),
   
]