from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/signin')
def desk_home(request):
    return render(request, 'desk/home.html')


def desk_logout(request):
    logout(request)
    return redirect('/')
