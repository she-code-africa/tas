FROM python:3.8

WORKDIR /app

RUN apt update \
      &&  apt-get install -y default-jre \
      && apt-get install -y curl php composer \
      && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
      && apt-get install -y nodejs \
      && curl -L https://www.npmjs.com/install.sh | sh


COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

ARG PORT=8000
ENV PORT=$PORT

EXPOSE $PORT

CMD gunicorn srv:app -b 0.0.0.0:$PORT
