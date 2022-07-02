# ref https://ep2020.europython.eu/media/conference/slides/CeKGczx-best-practices-for-production-ready-docker-packaging.pdf
# ref https://pythonspeed.com/articles/multi-stage-docker-python/

# builder outputs a virtualenv with installed dependencies
FROM python:3.9 AS builder

# makes sure system is up-to-date
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

# use regular user
RUN useradd --create-home app
USER app
WORKDIR /home/app

# creates a venv and install dependencies
RUN python -m venv venv
ENV PATH="./venv/bin:$PATH"
COPY requirements.txt .
COPY requirements.prod.txt .
RUN pip install -r requirements.txt -r requirements.prod.txt

# runner intakes the builder's virtualenv, does various things and define an entrypoint
FROM python:3.9 AS runner

# use regular user
RUN useradd --create-home app
USER app
WORKDIR /home/app

# intakes the virtualenv from builder
COPY --from=builder /home/app/venv ./venv

# intakes all files
COPY . /home/app/

ENV PATH="./venv/bin:$PATH"
ENV PYTHONFAULTHANDLER=1
EXPOSE 5000
