from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('signin', views.sign_in, name='sign_in'),
    path('signup', views.sign_up, name='sign_up'),
]
