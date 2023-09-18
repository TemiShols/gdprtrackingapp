FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
WORKDIR /app
CMD python manage.py runserver 0.0.0.0:8000