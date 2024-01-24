# FastAPI проект для Ylab

API предоставляет CRUD операции для `Menu`, `Submenu` и `Dishes`

## Установка:

1. Откройте командную строку и с помощью `cd "folder_name"` перейдите в необходимый каталог, куда хотите скачать мой проект
2. Скопируйте и вставьте следующее:
   
  > `git clone https://github.com/kadimk4/ylab-task.git`

Готово! Вы завершили скачивание моего проекта

## Настройка общая:

1. Создайте и активируйте виртуальное окружение по след. командам
   
  > `python -m venv venv`

  > `venv\Scripts\activate.bat` либо `venv\Scripts\activate`

2. Установите все зависимости из `requirments.txt` с помощью

  > `pip install -r requirments.txt`

4. Вставьте данные от базы данных в файле `.env`
5. В терминале Ide пропишите
   > `alembic upgrade head`

## Запуск без Doker:

1. Для запуска сервера необходимо прописать в терминале следующее:

   > `uvicorn main:app`
   
3. Перейдите по ссылке(в конце пропишите `/docs`) в терминале IDE либо в браузере `{ваш localhost}:{ваш port}/docs`

Готово! Теперь вы можете пользоваться CRUD функционалом

## Запуск с Doker:

1. Вставьте данные от базы данных в файле `.env-non-dev` ,`"DB_HOST"` - не трогаем!
2. Для запуска с тестами вводим в терминал 

   > `docker-compose -f docker-compose-tests.yml up --build`

3. Для запуска без тестов вводим

   > `docker-compose -f docker-compose.yml up --build`

4. Перейдите по ссылке(в конце пропишите `/docs`) в терминале IDE либо в браузере `{ваш ipV4}:{ваш port}/docs`
