from django.urls import path
from . import views
app_name = 'friends'
urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='f_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('friends/', views.list_friends, name='list_friends'),
    path('myprofile/',views.view_your_profile, name='my_profile'),
]