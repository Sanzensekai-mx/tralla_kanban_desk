from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import Board, Column, Card
from .forms import BoardForm
from .mixins import AJAXBoardMixIn, AJAXCardMixIn, AJAXHomeMixIn
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View


# Create your views here.


@login_required(login_url='/signin')
def desk_home(request):
    user_id = request.user.id
    boards = Board.objects.filter(user__id=user_id)
    return render(request, 'desk/home.html', {'boards': boards})


def desk_logout(request, username):
    logout(request)
    return redirect('/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "desk/home.html"
    form = BoardForm

    def get(self, *args, **kwargs):
        context = self.form()
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        boards = Board.objects.filter(user__id=user.id)
        return render(self.request, self.template_name,
                      {'form': context, 'boards': boards, 'current_user': username}
                      )

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        username = self.request.user.get_username()
        user = get_object_or_404(User, username=username)
        if form.is_valid():
            form.save_board(user)
            boards = Board.objects.filter(user__id=user.id)
            form = self.form()
            return render(self.request, self.template_name,
                          {'form': form, 'boards': boards, 'current_user': username}
                          )
        else:
            boards = Board.objects.filter(user__id=user.id)

        return render(self.request, self.template_name,
                      {'form': form, 'boards': boards, 'current_user': username}
                      )


# # @login_required(login_url='/signin')
# def create_board(request, board_id):
#     user = request.user
#     # user = get_object_or_404(User, id=user_id)
#     board = get_object_or_404(Board, id=board_id)
#     error = ''
#     if request.method == 'POST':
#         form = BoardForm(request.POST)
#         if form.is_valid():
#             new_board = form.save(commit=False)
#             new_board.user = user
#             new_board.update_board(new_board)
#             return redirect('/desk/home')
#         else:
#             error = f'Форма неверна'
#     else:
#         form = BoardForm()
#     # if user.id == board.user.id:
#     return render(request, 'desk/board.html', {'form': form, 'error': error, 'user': user})
#     # else:
#     #     return HttpResponse('Иди нахер')


class BoardView(LoginRequiredMixin, generic.DetailView):
    model = Board
    board_form = BoardForm
    template_name = 'desk/board.html'

    def get(self, *args, **kwargs):
        board_form = self.board_form()
        board_id = self.kwargs.get('id')
        user = self.request.user
        username = self.request.user.get_username()
        board = get_object_or_404(Board, id=board_id)
        boards = Board.objects.filter(user__id=user.id)
        columns = Column.objects.filter(board__id=board_id)
        card = Card.objects.filter(column__board__id=board_id)
        if user.id == board.user.id:
            return render(self.request, self.template_name,
                          {
                              'board_form': board_form, 'board': board,
                              'current_user': username, 'columns': columns,
                              'cards': card, 'user': user, 'boards': boards
                          })
        else:
            # Вернуть шаблон, либо ошибку 403
            return HttpResponse('403')

    def post(self, *args, **kwargs):
        error = ''
        board_id = self.kwargs.get('id')
        user = self.request.user
        user_id = self.request.user.id
        username = self.request.user.get_username()
        board = get_object_or_404(Board, id=board_id)
        boards = Board.objects.filter(user__id=user_id)
        columns = Column.objects.filter(board__id=board_id)
        cards = Card.objects.filter(column__board__id=board_id)
        if self.request.method == 'POST':
            board_form = self.board_form(self.request.POST)
            if board_form.is_valid():
                board = board_form.update_board(board)
                return render(self.request, self.template_name,
                              {
                                  'board_form': board_form, 'board': board,
                                  'current_user': username, 'columns': columns,
                                  'cards': cards, 'boards': boards, 'user': user
                              })
            else:
                error = f'Форма неверна'
        else:
            board_form = self.board_form()
        return render(self.request, self.template_name,
                      {
                          'board_form': board_form, 'board': board,
                          'current_user': username, 'columns': columns,
                          'cards': cards, 'boards': boards, 'user': user
                      })
    # def get_object(self, **kwargs):
    #     return self.request.user


class CreateBoard(LoginRequiredMixin, AJAXHomeMixIn, View):
    # form = BoardForm

    def post(self, *args, **kwargs):
        board_name = 'Новая доска'
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        new_board = Board(name=board_name, user=self.request.user)
        new_board.save()
        data = self.return_boards()
        return JsonResponse(data)


class AddColumnView(LoginRequiredMixin, AJAXBoardMixIn, View):

    def post(self, *args, **kwargs):
        column_name = self.request.POST.get('name')
        board_id = self.kwargs.get('id')
        board = get_object_or_404(Board, id=board_id)
        max_position = Column.objects.aggregate(Max('position'))
        to_add_position = 1
        maximum_exists = max_position.get('position__max')
        if maximum_exists:
            to_add_position = maximum_exists + 1
        new_column = Column(board=board, name=column_name, position=to_add_position, user=self.request.user)
        new_column.save()
        data = self.return_board()
        # needs to be changed
        return JsonResponse(data)


class UpdateColumnView(LoginRequiredMixin, AJAXBoardMixIn, View):

    def post(self, *args, **kwargs):
        name = self.request.POST.get('name')
        to_update_id = self.request.POST.get('id')
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        column = get_object_or_404(Column, id=to_update_id)
        column.name = name
        column.save()
        data = self.return_board()
        # needs to be changed
        return JsonResponse(data)


class AddCardView(LoginRequiredMixin, AJAXBoardMixIn, View):

    def post(self, *args, **kwargs):
        name = self.request.POST.get('name')
        column_id = self.request.POST.get('id')
        column = get_object_or_404(Column, pk=column_id)
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        new_card = Card(name=name, column=column, position=0)
        new_card.save()

        data = self.return_board()
        return JsonResponse(data)


class GetBoardDetails(LoginRequiredMixin, AJAXBoardMixIn, View):

    def get(self, *args, **kwargs):
        data = self.return_board()
        return JsonResponse(data)


class GetCardDetails(LoginRequiredMixin, AJAXCardMixIn, View):

    def get(self, *args, **kwargs):
        data = self.return_card()
        return JsonResponse(data)


class UpdateCardName(LoginRequiredMixin, AJAXCardMixIn, View):
    login_url = reverse_lazy('users:log_in')

    def post(self, *args, **kwargs):
        name = self.request.POST.get('name')
        card_id = self.request.POST.get('card_id')
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        card = get_object_or_404(Card, pk=card_id)
        card.name = name
        card.save()

        data = self.return_card()
        return JsonResponse(data)


class TransferCard(LoginRequiredMixin, AJAXBoardMixIn, View):

    def post(self, *args, **kwargs):
        card_id = self.request.POST.get('card_id')
        board = get_object_or_404(Board, id=self.kwargs.get('id'))
        card = get_object_or_404(Card, id=card_id)
        column_instance = get_object_or_404(
            Column, id=self.request.POST.get('to_column_id')
        )
        card.column = column_instance
        card.save()

        from_column_instance = get_object_or_404(
            Column, id=self.request.POST.get('from_column_id')
        )

        data = self.return_board()
        return JsonResponse(data)


class UpdateCardTitle(LoginRequiredMixin, AJAXCardMixIn, View):

    def post(self, *args, **kwargs):
        name = self.request.POST.get('title')
        card_id = self.request.POST.get('card_id')
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        card = get_object_or_404(Card, pk=card_id)
        card.name = name

        card.save()

        data = self.return_card()
        return JsonResponse(data)


class UpdateCardDescription(LoginRequiredMixin, View):

    def post(self, *args, **kwargs):
        description = self.request.POST.get('description')
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card, pk=card_id)
        card.description = description
        card.save()
        return HttpResponse('success!')


class DeleteCard(LoginRequiredMixin, View, AJAXBoardMixIn):

    def post(self, *args, **kwargs):
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card, id=card_id)
        board = get_object_or_404(Board, id=self.kwargs.get('id'))
        card.delete()
        data = self.return_board()
        return JsonResponse(data)


class DeleteColumn(LoginRequiredMixin, View, AJAXBoardMixIn):

    def post(self, *args, **kwargs):
        column_id = self.request.POST.get('id')
        column = get_object_or_404(Column, id=column_id)
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        column.delete()
        data = self.return_board()
        # needs to be changed
        return JsonResponse(data)
