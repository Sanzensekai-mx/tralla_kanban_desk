from django.shortcuts import render


# Create your views here.
def index(request):
    # return HttpResponse("<h4>Проверка</h4>")
    # Прописывается шаблон так, будто уже находишься в папке templates
    return render(request, 'main/index.html')


def about(request):
    # return HttpResponse("<h4>Сделал Яманчев Иван</h4>")
    return render(request, 'main/about.html')
