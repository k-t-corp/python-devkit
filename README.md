# python-devkit
Opinionated development CLI for my opinionated Python stacks
It's mainly responsible for starting up very similar docker-compose stacks for multiple projects locally
Although it may also build production-ready Python docker containers in the future

## Prerequisites
* `Python 3.9+`
* `Docker` and `docker-compose`
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (used for running `Procfile`s locally)

## Install
```bash
mkdir -p ~/.python-devkit/tool
git clone git@github.com:k-t-corp/python-devkit.git ~/.python-devkit/tool
python3 -m venv ~/.python-devkit/venv
```

## Development
