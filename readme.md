# Track Assessment Server

Automates track assessment scoring using test suites and testcase for each specific track.

## Setup local environment

    Required: Python version: 3.6^

``` shell
$: python -m pip install virtualenv

$: python -m venv venv/

$: source venv/bin/activate
```

## Install packages

``` shell
$: pip install -r requirements.txt
```

## Running the server

* __Expose required common environment variables__

``` shell
$: export APP_SETTINGS="development"
```

### Using Flask (Hot Reload)

``` shell
$: export FLASK_APP=srv

$: export FLASK_ENV=development

$: flask run -p 8000
```

### Using Gunicorn

``` shell
$: gunicorn srv:app
```

## Testing

``` shell
$: pytest
```
