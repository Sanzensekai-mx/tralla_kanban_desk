from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Board, Column, Card
from .forms import BoardForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


# Create your views here.


@login_required(login_url='/signin')
def desk_home(request):
    user_id = request.user.id
    boards = Board.objects.filter(user__id=user_id)
    return render(request, 'desk/home.html', {'boards': boards})


def desk_logout(request):
    logout(request)
    return redirect('/')


# @login_required(login_url='/signin')
def create_board(request, board_id):
    user = request.user
    # user = get_object_or_404(User, id=user_id)
    board = get_object_or_404(Board, id=board_id)
    error = ''
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            new_board = form.save(commit=False)
            new_board.user = user
            new_board.update_board(new_board)
            return redirect('/desk/home')
        else:
            error = f'Форма неверна'
    else:
        form = BoardForm()
    # if user.id == board.user.id:
    return render(request, 'desk/board.html', {'form': form, 'error': error, 'user': user})
    # else:
    #     return HttpResponse('Иди нахер')


class BoardView(LoginRequiredMixin, generic.DetailView):
    model = Board
    # login_url = reverse_lazy('signin')
    board_form = BoardForm
    template_name = 'desk/board.html'
    context_object_name = 'board'

    def get(self, *args, **kwargs):
        board_form = self.board_form()
        board_id = self.kwargs.get('id')
        user = self.request.user
        username = self.request.user.get_username()
        board = get_object_or_404(Board, id=board_id)
        columns = Column.objects.filter(board__id=board_id)
        card = Card.objects.filter(column__board__id=board_id)
        if user.id == board.user.id:
            return render(self.request, self.template_name,
                          {
                              'board_form': board_form, 'board': board,
                              'current_user': username, 'columns': columns,
                              'cards': card, 'user': user
                          })
        else:
            return HttpResponse('Тебе сюда нельзя.')

    def post(self, *args, **kwargs):
        error = ''
        board_id = self.kwargs.get('id')
        user = self.request.user
        user_id = self.request.user.id
        username = self.request.user.get_username()
        board = get_object_or_404(Board, id=board_id)
        boards = Board.objects.filter(user__id=user_id)
        columns = Column.objects.filter(board__id=board_id)
        card = Card.objects.filter(column__board__id=board_id)
        if self.request.method == 'POST':
            board_form = self.board_form(self.request.POST)
            if board_form.is_valid():
                board = board_form.update_board(board)
                return render(self.request, self.template_name,
                              {
                                  'board_form': board_form, 'board': board,
                                  'current_user': username, 'columns': columns,
                                  'cards': card, 'boards': boards, 'user': user
                              })
            else:
                error = f'Форма неверна'
        else:
            board_form = self.board_form()
        return render(self.request, self.template_name,
                      {
                          'board_form': board_form, 'board': board,
                          'current_user': username, 'columns': columns,
                          'cards': card, 'boards': boards, 'user': user
                      })
    # def get_object(self, **kwargs):
    #     return self.request.user
