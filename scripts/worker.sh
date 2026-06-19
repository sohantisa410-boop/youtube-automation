#!/usr/bin/env bash
set -e
cd workers
celery -A tasks.celery_app.celery_app worker -l info
