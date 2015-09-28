FROM python:3
MAINTAINER yigal@publysher.nl

WORKDIR /app/mirigata
EXPOSE 8000

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

RUN adduser --system mirigata
USER mirigata

COPY . /app/

CMD python manage.py runserver 0.0.0.0:8000
