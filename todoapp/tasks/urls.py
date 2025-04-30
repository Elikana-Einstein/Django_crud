from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.task_list, name='task_list'),
    path('register/', views.register, name='register'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:task_id>/',views.update_task,name='update_task'),
    path('delete/<int:task_id>/',views.delete_task,name='delete_task'),
    path('complete/<int:task_id>/',views.complete_task,name='update_complete_task'),
   
]