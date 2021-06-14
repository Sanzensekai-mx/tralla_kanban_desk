from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('<str:username>', views.IndexView.as_view(), name='desk_home'),
    # path('home', views.desk_home, name='desk_home'),
    path('<str:username>/logout', views.desk_logout, name='log_out'),
    path('<int:id>/board', views.BoardView.as_view(), name='board'),
    path('<int:id>/add', views.AddColumnView.as_view(), name='add_column'),
    path('<int:id>/update', views.UpdateColumnView.as_view(), name='update_column'),
    path('<int:id>/add_card', views.AddCardView.as_view(),  name="add_card"),
    path('<int:id>/get_board', views.GetBoardDetails.as_view(),  name="get_board"),
    path('<int:id>/get_card', views.GetCardDetails.as_view(),  name="get_card_detail"),
    path('<int:id>/update_card_title', views.UpdateCardTitle.as_view(), name="update_card_title"),
    path('<int:id>/update_card_description', views.UpdateCardDescription.as_view(), name="update_card_description"),
]
