#!/bin/bash
# Script to run Django development server

cd "$(dirname "$0")"
./venv/bin/python manage.py runserver

