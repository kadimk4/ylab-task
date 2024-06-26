# FastAPI проект для Ylab

API предоставляет CRUD операции для `Menu`, `Submenu` и `Dishes`

## Установка:

1. Откройте командную строку и с помощью `cd "folder_name"` перейдите в необходимый каталог, куда хотите скачать мой проект
2. Скопируйте и вставьте следующее:
   
  > `git clone https://github.com/kadimk4/ylab-task.git`

Готово! Вы завершили скачивание моего проекта

## Настройка без Docker'a:

1. Создайте и активируйте виртуальное окружение по след. командам
   
   > `python -m venv venv`

   > `venv\Scripts\activate.bat` либо `venv\Scripts\activate`

2. Установите все зависимости из `requirements.txt` с помощью

   > `pip install -r requirements.txt`

3. Вставьте данные от базы данных в файле `.env`
4. В терминале Ide пропишите
   > `alembic upgrade head`

## Запуск без Docker:

1. Для запуска сервера необходимо прописать в терминале следующее:

   > `uvicorn main:app`
   
3. Перейдите по ссылке(в конце пропишите `/docs`) в терминале IDE либо в браузере `{ваш localhost}:{ваш port}/docs`

Готово! Теперь вы можете пользоваться CRUD функционалом

## Запуск с Docker:

   > ВАЖНО! Контейнеры находятся на одном порту, запускать только один контейнер за раз!

1. Удалите `.env` и переименуйте `.env.example` в `.env` 
2. Для запуска апи пропишите в терминале

   > `docker-compose -f docker-compose.yml up --build`

3. Для запуска апи тестов пропишите в терминале

   > `docker-compose -f docker-compose-tests.yml up --build`

Тестовый сценарий лежит в test/test_dishes_submenus_count
Сложный орм запрос в services/crud.py -> class Menu -> функция get
