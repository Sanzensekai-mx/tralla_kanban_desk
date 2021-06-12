from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Board

# Create your views here.


@login_required(login_url='/signin')
def desk_home(request):
    boards = Board.objects.all()
    return render(request, 'desk/home.html', {'boards': boards})


def desk_logout(request):
    logout(request)
    return redirect('/')
