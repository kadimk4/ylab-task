<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
        }
        h1 {
            font-size: 2em;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 1.5em;
            margin-bottom: 15px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Меню API</h1>
    <p>Проект реализован на FastAPI и предоставляет CRUD операции для "Menu", "Submenu" и "Dishes".</p>

    <h2>Инструкция:</h2>
    <ol>
        <li>Необходимо активировать виртуальное окружение в вашей IDE. Для этого пропишите в терминале:</li>
        <code>venv/Scripts/activate</code>
        <li>Укажите данные вашей базы данных в файле <code>.env</code>.</li>
        <li>Запуск локального сервера происходит также в терминале IDE:</li>
        <code>uvicorn {ipV4}:{port} main:app</code>
        <li>Перейдите по ссылке, появившейся в терминале, либо в браузере введите:</li>
        <code>{ipV4}:{port}/docs</code>
    </ol>

    <p>Готово! Теперь вы можете пользоваться CRUD функционалом сайта. Приятного использования!</p>
</body>
</html>
