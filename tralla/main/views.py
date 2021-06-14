from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm


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
                    return redirect(f'desk/{user.username}')
                    # return render(request, 'desk/home.html', {'user': user})
                else:
                    form = LoginForm()
                    return render(request, 'main/signin.html', {'form': form, 'not_valid': 'Аккаунт отключен'})
            else:
                form = LoginForm()
                return render(request, 'main/signin.html', {'form': form, 'not_valid': 'Неправильный логин или пароль'})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        return render(request, 'main/signin.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # return redirect('desk/home')
            return render(request, 'main/signup_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'main/signup.html', {'user_form': user_form})


def sign_up_done(request):
    return render(request, 'main/signup_done.html')
