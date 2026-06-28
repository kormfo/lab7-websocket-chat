# Лабораторная работа №7 — Чат на WebSockets

Чат на FastAPI с WebSockets. Клиент на HTML + JavaScript, сервер на Python.


## Запуск

Установить библиотеки:

pip install fastapi uvicorn jinja2 pydantic websockets

Запустить сервер:

python main.py

Открыть в браузере:

http://localhost:8000

## Структура

- main.py — сервер
- models.py — проверка сообщений
- templates/chat.html — страница чата

## Что сделано

### Задание 1 — Имя пользователя

При подключении передаётся имя через ссылку: ws://localhost:8000/ws?username=Alice
<img width="678" height="215" alt="image" src="https://github.com/user-attachments/assets/fd2599b6-29a3-4f9e-baad-8e60faba0965" />

Если имя не указать — сервер не пустит.
<img width="736" height="199" alt="image" src="https://github.com/user-attachments/assets/b3b83fdb-5a3c-4d40-809c-434a13593108" />

### Задание 2 — Системные сообщения

Когда кто-то заходит, всем приходит "Alice joined (Online: 2)".
<img width="508" height="193" alt="image" src="https://github.com/user-attachments/assets/1c2d2a58-4338-4c91-9988-183026592fda" />

Когда выходит — "Alice left (Online: 1)".
<img width="548" height="265" alt="image" src="https://github.com/user-attachments/assets/8342af26-9924-4057-896d-b763826a53b5" />

Выдача количества online
<img width="244" height="33" alt="image" src="https://github.com/user-attachments/assets/7bbbf9bb-94a4-4719-b59f-e1012d0dc1b7" />

Отображение в списке сообщений
<img width="574" height="66" alt="image" src="https://github.com/user-attachments/assets/79c708ea-45a0-457e-a7a4-c0ed99536254" />


### Задание 3 — JSON формат
<img width="482" height="74" alt="image" src="https://github.com/user-attachments/assets/29802c93-060e-4284-ad1f-e848a69be925" />
<img width="435" height="122" alt="image" src="https://github.com/user-attachments/assets/6c7245c2-6df2-4638-aba4-26c37da80009" />

Сообщения передаются в JSON:

{
    "type": "message",
    "user": "Alice",
    "text": "Привет",
    "ts": "2026-06-28T12:30:00"
}
<img width="650" height="316" alt="image" src="https://github.com/user-attachments/assets/3bfb8bf2-f0c7-4f63-8eca-5f74f9285b8f" />

### Задание 4 — Проверка сообщений

Через Pydantic проверяется что сообщение не пустое и не длиннее 200 символов.
<img width="655" height="361" alt="image" src="https://github.com/user-attachments/assets/2a081940-21bf-451c-bc1f-279a294ca42a" />

<img width="568" height="292" alt="image" src="https://github.com/user-attachments/assets/804a8435-a4a6-4ce0-86c4-df58b1ba9984" />

<img width="386" height="84" alt="image" src="https://github.com/user-attachments/assets/34aadab3-c993-400d-b6e5-f45e958bbdef" />


Если что-то не так — сервер присылает ошибку:

{
    "type": "error",
    "detail": "Message is empty"
}
<img width="583" height="96" alt="image" src="https://github.com/user-attachments/assets/f2481ab8-4586-4c85-9cde-5fa5788f5547" />

### Задание 5 — Приватные сообщения

Можно написать личное сообщение командой:

/w Bob привет, как дела?

Тогда его увидит только Bob. Если Bob не в сети — сервер скажет об этом.


### Чат с тремя пользователями

<img width="633" height="183" alt="image" src="https://github.com/user-attachments/assets/75da7f64-413e-46ca-877b-25b2765eae09" />


### Приватное сообщение

<img width="505" height="52" alt="image" src="https://github.com/user-attachments/assets/028db266-6614-4702-8e30-06efb3ac576b" />


### Ошибка валидации

<img width="374" height="74" alt="image" src="https://github.com/user-attachments/assets/23508f95-9379-4c3d-882c-f0b6aa49c8c6" />
