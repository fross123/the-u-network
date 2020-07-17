FROM python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade -r requirements.txt
RUN python manage.py collectstatic --noinput
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
