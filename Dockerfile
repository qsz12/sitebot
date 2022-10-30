FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk add install libpq-dev

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "-k=eventlet", "--bind=127.0.0.1:8080", "--access-logfile=-", "--reload"]