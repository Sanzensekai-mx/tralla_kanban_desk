from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.desk_home, name='desk_home'),
    path('logout', views.desk_logout, name='log_out'),
    path(r'create/<int:user_id>', views.create_board, name='create_board')
]
