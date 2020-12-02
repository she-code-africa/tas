FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY srv/ .
COPY scrips/ .
COPY engines/ .

CMD ["gunicorn", "srv:app"]
