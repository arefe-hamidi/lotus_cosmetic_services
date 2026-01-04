#!/bin/bash
# Script to stop Django development server

echo "Stopping Django server on port 8000..."

# Find and kill process on port 8000
PID=$(lsof -ti:8000)
if [ -n "$PID" ]; then
    kill $PID
    echo "Server stopped (PID: $PID)"
else
    echo "No server running on port 8000"
fi

# Also kill any manage.py runserver processes
pkill -f "manage.py runserver" 2>/dev/null

echo "Done!"

