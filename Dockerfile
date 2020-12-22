FROM python:3.8

WORKDIR /app

RUN apt update \
      # curl: command line tool for transferring data with URL syntax
      # make: utility for directing compilation
      # default-jdk-headless: Standard Java or Java compatible Development Kit (headless)
      # ant: Java based build tool like make
      # nodejs: evented I/O for V8 javascript - runtime executable
      # php: server-side, HTML-embedded scripting language (default)
      && apt-get install -y curl make default-jdk-headless ant nodejs php \
      # add node source.
      && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
      # install npmjs.
      && curl -L https://www.npmjs.com/install.sh | sh


# install testsuite dependencies
# phpunit: php testsuite
# jest: node testsuite
RUN apt install -y phpunit \
      && npm install -g jest

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ARG PORT=8000
ENV PORT=$PORT

EXPOSE $PORT

CMD gunicorn srv:app -b 0.0.0.0:$PORT
