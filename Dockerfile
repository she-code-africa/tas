FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ARG PORT=8000
ENV PORT=$PORT

EXPOSE $PORT

CMD gunicorn srv:app -b 0.0.0.0:$PORT
