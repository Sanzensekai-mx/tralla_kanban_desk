# Tralla
 Иван Яманчев

### Запуск
Для запуска необходим .env файл, создайте его в подкаталоге tralla. Внутри впишите строчку:
`SECRET_KEY=<Ваш секретный ключ>`

Из корневой директории:
`cd tralla`
Применение миграций:
`python manage.py migrate`
Создание администратора:
`python manage.py createsuperuser`
Следовать подсказкам командной строки.
Запуск сервера:
`python manage.py runserver`
