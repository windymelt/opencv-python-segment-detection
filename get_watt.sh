#!/bin/bash
set -e
docker compose run --rm app python recognition.py
docker compose run --rm app ssocr -d-1 ./IMG_det.jpg -D./IMG_det_debug.jpg