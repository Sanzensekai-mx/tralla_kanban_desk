from django.urls import path
from . import views


urlpatterns = [
    path('<str:username>', views.IndexView.as_view(), name='desk_home'),
    path('home', views.desk_home, name='desk_home'),
    path('<str:username>/logout', views.desk_logout, name='log_out'),
    path('<str:username>/set_new_board_title', views.GetBoardsInfo.as_view(), name="set_new_board"),
    path('<str:username>/create_board', views.CreateBoard.as_view(), name='create_board'),
    path('<int:id>/delete_board', views.DeleteBoard.as_view(), name='delete_board'),
    path('<int:id>/board', views.BoardView.as_view(), name='board'),
    path('<int:id>/add', views.AddColumnView.as_view(), name='add_column'),
    path('<int:id>/update', views.UpdateColumnView.as_view(), name='update_column'),
    path('<int:id>/add_card', views.AddCardView.as_view(),  name="add_card"),
    path('<int:id>/get_card', views.GetCardDetails.as_view(),  name="get_card_detail"),
    path('<int:id>/update_card_title', views.UpdateCardTitle.as_view(), name="update_card_title"),
    path('<int:id>/update_card_description', views.UpdateCardDescription.as_view(), name="update_card_description"),
    path('<int:id>/transfer_card', views.TransferCard.as_view(), name="transfer_cards"),
    path('<int:id>/delete_card', views.DeleteCard.as_view(), name="delete_card"),
    path('<int:id>/delete_column', views.DeleteColumn.as_view(), name="delete_column")
]
