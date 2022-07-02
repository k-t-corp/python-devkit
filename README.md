# python-devkit
Opinionated development CLI for my opinionated Python stacks

It does two things

1. Generate `docker-compose` file for local development that starts databases auxiliary to a main Python application
2. Generate files for production deployment that starts and updates the main Python application on an Ubuntu 20.04 machine that's based on `docker-compose` and `uwsgi`

## Prerequisites
* `Python 3.9+`
* `Docker` and `docker-compose`
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (used for running `Procfile`s locally)

## Install
```bash
mkdir -p ~/.python-devkit/tool
git clone https://github.com/k-t-corp/python-devkit.git ~/.python-devkit/tool
python3 -m venv ~/.python-devkit/tool/.venv
~/.python-devkit/tool/.venv/bin/pip install poetry
pushd ~/.python-devkit/tool && ~/.python-devkit/tool/.venv/bin/poetry install && popd
```

## Use
```bash
cd path/to/a/project
~/.python-devkit/tool/.venv/bin/python ~/.python-devkit/tool/up.py
```

You should also add the command as an alias `up` in your `.bashrc` or `.zshrc`
```bash
alias up='~/.python-devkit/tool/.venv/bin/python ~/.python-devkit/tool/up.py'
```
