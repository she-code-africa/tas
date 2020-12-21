FROM python:3.8

WORKDIR /app

RUN apt update \
      &&  apt-get install -y openjdk-8-jre-headless ant \
      && apt-get install -y curl php composer php-mbstring php-xml \
      && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
      && apt-get install -y nodejs \
      && curl -L https://www.npmjs.com/install.sh | sh

RUN php --ini

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

ARG PORT=8000
ENV PORT=$PORT

EXPOSE $PORT

CMD gunicorn srv:app -b 0.0.0.0:$PORT
