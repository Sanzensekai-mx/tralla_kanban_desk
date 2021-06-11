from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm


# Create your views here.
def index(request):
    # return HttpResponse("<h4>Проверка</h4>")
    # Прописывается шаблон так, будто уже находишься в папке templates
    data = {
        'title': 'Tralla',
        'values': ['Some', 'Hello', '123'],
    }
    return render(request, 'main/index.html', data)


def about(request):
    # return HttpResponse("<h4>Сделал Яманчев Иван</h4>")
    return render(request, 'main/about.html')


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return render(request, 'desk/')
                    return HttpResponse('Аутентификация прошла успешно')
                else:
                    return HttpResponse('Аккаунт отключен')
            else:
                return HttpResponse('Неправильный логин или пароль')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    return render(request, 'main/signin.html', {'form': form})


def sign_up(request):
    return render(request, 'main/signup.html')
