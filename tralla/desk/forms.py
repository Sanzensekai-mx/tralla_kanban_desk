from django.forms import ModelForm, TextInput, Textarea, Form
from django import forms
from .models import Board, Column, Card


class BoardForm(Form):
    # class Meta:
    #     model = Board
    #     fields = ['name']
    #     widgets = {
    #         'name': TextInput(attrs={
    #             'class': 'form-control sign-up-input',
    #         })
    #     }
    board_name = forms.CharField(max_length=40, required=True, widget=TextInput(attrs={
        'class': 'form-control sign-up-input',
    }))

    def save_board(self, user):
        new_board = Board(name=self.cleaned_data['board_name'], user=user)
        new_board.save()

    def update_board(self, board):
        board.name = self.cleaned_data['board_name']
        board.save()
        return board