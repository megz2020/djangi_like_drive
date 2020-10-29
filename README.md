# Ayen Task
# instructions
- docker build .
-  docker-compose  run --rm app sh -c  "python manage.py makemigrations"
-  docker-compose  run --rm app sh -c  "python manage.py migrate"
- docker up
- http://localhost:8000/signup/