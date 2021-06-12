from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='/signin')
def desk_home(request):
    boards = Board.objects.all()
    return render(request, 'desk/home.html', {'boards': boards})


def desk_logout(request):
    logout(request)
    return redirect('/')


def create_board(request, user_id):
    user = get_object_or_404(User, id=user_id)
    error = ''
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            new_board = form.save(commit=False)
            new_board.user = user
            new_board.save()
            return redirect('/desk/home')
        else:
            error = f'Форма неверна {user.username}'
    else:
        form = BoardForm()
    return render(request, 'desk/create_board.html', {'form': form, 'error': error, 'user': user})
