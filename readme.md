# Track Assessment Server

## Install

Install required packages

* Requirement: Python 3

``` sh
pip install -e . '.[test]'
```

## Run

* Run Flask

``` sh
FLASK_APP=srv FLASK_ENV=development flask run
```

## Test

``` sh
pytest
```
