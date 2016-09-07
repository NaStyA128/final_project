Выполнила Головизнина Анастасия.

Программный продукт разработан:

    1. django_project and server.py - с помощью python3.5
    2. scraping_images - с помощью python2.7
    
Для работы необходимо иметь 2 виртуальные машины и в каждую внедрить связи:

    1) для .env на python3.5 - requirements.txt;
    2) для .env2 на python2.7 - requirements2.txt.

Документация к програмному продукту находится в папке docs/_build/html/, файл - index.htlml.

Для дальнейшей работы с програмным продуктом необходимо:

    1. Запустить django-сервер, зайдя в папку django_project/: 
        python manage.py runserver под .env
    2. Запустить работу redis-server и парсеров, выполнив команду под .env2:
        honcho -e .env2 -f Procfile.dev start
    3. Запустить сервер в папке sockets/ под .env:
        python3 server.py

