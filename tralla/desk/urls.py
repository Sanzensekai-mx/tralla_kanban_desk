from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.desk_home, name='desk_home')
]
