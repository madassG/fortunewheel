# Wheel of fortune for getcourse users

Here I use 2 groups from getcourse. I email them with the auto-generated link. 
They follow it and are available to spin the wheel.

How to build the project for the development?
1. Set up the environment (.env file firstly)
```bash
  virtualenv env
  source env/bin/activate
  pip install -r requirements.txt
```
2. Load Django
```bash 
    python manage.py migrate
    python manage.py createsuperuser
```
<sub>During the user creation follow the instructions</sub>
<br>Now we can start or development server
```bash
    python manage.py runserver
```

3. Start celery beat and worker
```bash
    celery -A glisti worker -l INFO
    celery -A glisti beat -l INFO
```