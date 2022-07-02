#!/usr/bin/env bash
set -ex

/usr/bin/docker build -t app .
/usr/local/bin/docker-compose -f docker-compose.prod.yml run db-migration
/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
