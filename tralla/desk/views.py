from django.shortcuts import render

# Create your views here.


def desk_home(request):
    return render(request, 'main/about.html')
