from django.db.models import Max
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
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
    login_url = '/signin'
    form = BoardForm

    def get(self, *args, **kwargs):
        context = self.form()
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        # board = get_object_or_404(Board, user=user)
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
            # board = get_object_or_404(Board, user=user)
            boards = Board.objects.filter(user__id=user.id)
            form = self.form()
            return render(self.request, self.template_name,
                          {'form': form, 'boards': boards,
                           'current_user': username}
                          )
        else:
            boards = Board.objects.filter(user__id=user.id)

        return render(self.request, self.template_name,
                      {'form': form, 'boards': boards,
                       'current_user': username}
                      )


class BoardView(LoginRequiredMixin, generic.DetailView):
    model = Board
    board_form = BoardForm
    template_name = 'desk/board.html'
    login_url = '/signin'

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
        # if self.request.method == 'POST':
        board_form = self.board_form(self.request.POST)
        if board_form.is_valid():
            board = board_form.update_board(board)
        else:
            error = f'Введите название доски'
        return render(self.request, self.template_name,
                      {
                          'board_form': board_form, 'board': board,
                          'current_user': username, 'columns': columns,
                          'cards': cards, 'boards': boards, 'user': user, 'error': error
                      })
        # else:
        #     board_form = self.board_form()
        # return render(self.request, self.template_name,
        #               {
        #                   'board_form': board_form, 'board': board,
        #                   'current_user': username, 'columns': columns,
        #                   'cards': cards, 'boards': boards, 'user': user
        #               })
    # def get_object(self, **kwargs):
    #     return self.request.user


class DeleteBoard(LoginRequiredMixin, AJAXHomeMixIn, View):
    login_url = '/signin'
    template_name = 'desk/home.html'
    form = BoardForm

    def post(self, *args, **kwargs):
        board_id = self.request.POST.get('board_id')
        print(board_id)
        username = self.request.POST.get('username')
        board = get_object_or_404(Board, id=board_id)
        # print(board.user.username)
        # print(board.user.username)
        # data = self.return_boards()

        user = board.user
        boards = Board.objects.filter(user__id=user.id)
        print(boards)
        form = self.form()
        board.delete()
        return redirect(f'/desk/{user.username}')
        # return HttpResponse('Sucess')
        # return JsonResponse(data)
        # return render(self.request, self.template_name,
        #               {'form': form, 'boards': boards,
        #                'current_user': username})


class CreateBoard(LoginRequiredMixin, AJAXHomeMixIn, View):
    board_form = BoardForm
    template_name = 'desk/board.html'
    login_url = reverse_lazy('/signin')

    def post(self, *args, **kwargs):
        error = ''
        user = self.request.user
        username = user.username
        # if self.request.method == 'POST':
        board_form = self.board_form(self.request.POST)
        if board_form.is_valid():
            board = board_form.save_board(user)
            board_id = board.id
            columns = Column.objects.filter(board__id=board_id)
            cards = Card.objects.filter(column__board__id=board_id)
            print(board_id)
        else:
            error = f'Введите название доски'
        return render(self.request, self.template_name,
                      {
                          'board_form': board_form, 'board': board,
                          'current_user': username, 'columns': columns,
                          'cards': cards, 'user': user, 'error': error
                      })
        # board_name = self.request.POST.get('name')
        # username = self.request.POST.get('username')
        # user = get_object_or_404(User, username=username)
        # new_board = Board(name=board_name, user=self.request.user)
        # new_board.save()
        # data = self.return_boards()
        # return JsonResponse(data)


class GetBoardsInfo(LoginRequiredMixin, AJAXHomeMixIn, View):
    login_url = '/signin'

    def get(self, *args, **kwargs):
        data = self.return_boards()
        print(data)
        return JsonResponse(data)


class AddColumnView(LoginRequiredMixin, AJAXBoardMixIn, View):
    login_url = '/signin'

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
    login_url = '/signin'

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
    login_url = '/signin'

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
    login_url = '/signin'

    def get(self, *args, **kwargs):
        data = self.return_board()
        return JsonResponse(data)


class GetCardDetails(LoginRequiredMixin, AJAXCardMixIn, View):
    login_url = '/signin'

    def get(self, *args, **kwargs):
        data = self.return_card()
        return JsonResponse(data)


# class UpdateCardName(LoginRequiredMixin, AJAXCardMixIn, View):
#
#     def post(self, *args, **kwargs):
#         name = self.request.POST.get('name')
#         card_id = self.request.POST.get('card_id')
#         board = get_object_or_404(Board, pk=self.kwargs.get('id'))
#         card = get_object_or_404(Card, pk=card_id)
#         card.name = name
#         card.save()
#
#         data = self.return_card()
#         return JsonResponse(data)


class TransferCard(LoginRequiredMixin, AJAXBoardMixIn, View):
    login_url = '/signin'

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
    login_url = '/signin'

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
    login_url = '/signin'

    def post(self, *args, **kwargs):
        description = self.request.POST.get('description')
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card, pk=card_id)
        card.description = description
        card.save()
        return HttpResponse('success!')


class DeleteCard(LoginRequiredMixin, View, AJAXBoardMixIn):
    login_url = '/signin'

    def post(self, *args, **kwargs):
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card, id=card_id)
        board = get_object_or_404(Board, id=self.kwargs.get('id'))
        card.delete()
        data = self.return_board()
        return JsonResponse(data)


class DeleteColumn(LoginRequiredMixin, View, AJAXBoardMixIn):
    login_url = '/signin'

    def post(self, *args, **kwargs):
        column_id = self.request.POST.get('id')
        column = get_object_or_404(Column, id=column_id)
        board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        column.delete()
        data = self.return_board()
        # needs to be changed
        return JsonResponse(data)
