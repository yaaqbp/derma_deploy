FROM python:3.9-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN mkdir -p /usr/share/man/man1

RUN apt-get update && apt-get install -y

COPY . .

CMD gunicorn -b 0.0.0.0:$PORT derma_deploy.wsgi:application