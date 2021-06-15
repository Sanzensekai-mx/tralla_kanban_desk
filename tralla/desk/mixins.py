from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import render
from .models import Column, Card, Board
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.shortcuts import get_object_or_404


class AJAXBoardMixIn:

    def return_board(self):
        board_id = self.kwargs.get('id')
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        all_columns = Column.objects.filter(board__id=board_id).order_by('position')
        cards = Card.objects.filter(column__board__id=board_id).order_by('position')

        serialized_data_card = serializers.serialize('json', cards)
        serialized_data_column = serializers.serialize('json', all_columns)

        data = {'column': serialized_data_column,
                'card': serialized_data_card
                }
        return data


class AJAXCardMixIn:

    def return_card(self):
        card_id = 0
        if self.request.method == "GET":
            card_id = self.request.GET.get('card_id')
        else:
            card_id = self.request.POST.get('card_id')
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        # brackets are needed since they are single objects
        card = [get_object_or_404(Card, pk=card_id)]
        current_user = {'current_user': self.request.user.username}
        serialized_data_card = serializers.serialize('json', card)

        data = {'cards': serialized_data_card,
                'current_user': current_user
                }
        return data


class AJAXHomeMixIn:

    def return_boards(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        boards = Board.objects.filter(user__id=user.id)
        serialized_data_boards = serializers.serialize('json', boards)

        data = {'boards': boards}

        return data
