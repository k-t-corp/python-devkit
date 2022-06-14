# python-devkit
Opinionated development CLI for my opinionated Python stacks

For now, it's mainly responsible for starting up very similar docker-compose stacks for multiple projects locally

Although it may also build production-ready Python docker containers in the future

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
~/.python-devkit/tool/.venv/bin/pip poetry install
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
