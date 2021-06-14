from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('<str:username>', views.IndexView.as_view(), name='home'),
    # path('home', views.desk_home, name='desk_home'),
    path('logout', views.desk_logout, name='log_out'),
    path('<int:id>/board', views.BoardView.as_view(), name='board'),
    path('add/<int:id>', views.AddColumnView.as_view(), name='add_column'),
    path('update/<int:id>', views.UpdateColumnView.as_view(), name='update_column'),
    path('add_card/<int:id>', views.AddCardView.as_view(),  name="add_card"),
    path('get_board/<int:id>', views.GetBoardDetails.as_view(),  name="get_board"),
    path('get_card/<int:id>', views.GetCardDetails.as_view(),  name="get_card_detail"),
    path('update_card_title/<int:id>', views.UpdateCardTitle.as_view(), name="update_card_title"),
    path('update_card_description/<int:id>', views.UpdateCardDescription.as_view(), name="update_card_description"),
]
