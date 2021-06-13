from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('home', views.desk_home, name='desk_home'),
    path('logout', views.desk_logout, name='log_out'),
    path('<int:id>', views.BoardView.as_view(), name='board-detail')
    # re_path(r'^board/?P<id>[\d]+&', views.BoardView.as_view(), name='board')
]
