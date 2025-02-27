FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN pip install -r requirements.txt

WORKDIR /code/api_usuarios

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
