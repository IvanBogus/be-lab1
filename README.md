be-lab1

Навчальний бекенд-проєкт на Python/Flask для лабораторних робіт.
ЛР1 — /healthcheck, Docker/Compose, деплой на Render.
ЛР2 — базове REST API для обліку витрат (users, categories, records), ін-меморі.


Структура
app/
  __init__.py
  views.py
Dockerfile
docker-compose.yml
requirements.txt
README.md


Локальний запуск (Docker Compose)
    docker compose up --build
    # після старту: http://localhost:5050/healthcheck

Production
    https://be-lab1-nvb9.onrender.com/healthcheck


Ендпоінти

ЛР1

    GET /healthcheck → 200 OK, тіло: { "date": "<ISO-8601 UTC>", "status": "ok" }
    GET / → вітальне повідомлення (JSON)


ЛР2 (ін-меморі)

Users

    POST /user body: {"name":"Alex"} → 201

    GET /user/<id> → 200 / 404

    DELETE /user/<id> → 204

    GET /users → 200

    Categories

    POST /category body: {"title":"Food"} → 201

    GET /category → 200

    DELETE /category?id=<id> → 204

Records

    POST /record body: {"user_id":1,"category_id":1,"amount":12.5} → 201

    GET /record/<id> → 200 / 404

    DELETE /record/<id> → 204

    GET /record?user_id=<id>&category_id=<id> → 200
    
    Примітка: хоча б один із параметрів (user_id або category_id) обов’язковий; без них — 400.

Postman: імпортуй /postman/*, обери env (local|prod) і запусти Run collection.

Приклади запитів (Windows PowerShell, prod)
    $base = "https://be-lab1-nvb9.onrender.com"

    Invoke-WebRequest "$base/healthcheck"

    Invoke-WebRequest "$base/user" -Method POST -ContentType "application/json" -Body '{"name":"Alex"}'
    Invoke-WebRequest "$base/category" -Method POST -ContentType "application/json" -Body '{"title":"Food"}'
    Invoke-WebRequest "$base/record" -Method POST -ContentType "application/json" -Body '{"user_id":1,"category_id":1,"amount":12.5}'

    Invoke-WebRequest "$base/users"
    Invoke-WebRequest "$base/record?user_id=1"
