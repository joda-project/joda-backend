# Building joda-backend for development

Joda backend packages are powered by Python and Django.

## Requirements
You will need the following things properly installed on your computer:
* [Git](https://git-scm.com)
* [Python 3](https://python.org) with pip
* [Foreman](https://ddollar.github.io/foreman/) (optional)

## Installation
* Create virtual Python environment `python3 -m venv venv`
* `source venv/bin/activate`
* `git clone https://github.com/joda-project/joda-backend` this repository
* `cd joda-backend`
* `pip install -r requirements.txt`
* install required addons
* copy `sample.env` to `.env` and adapt to your local environment

## Running Joda backend for development
* `foreman run manage.py migrate`
* `foreman start`

## Running Tests
Run `foreman run coverage run manage.py test`. To see coverage report run `coverage report`.
