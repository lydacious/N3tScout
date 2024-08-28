#!/bin/bash

echo "Starting N3tScout..."

# First run initialization: install dependencies if needed
if [ ! -f ".initialized" ]; then
    echo "First run detected. Installing dependencies..."

    # Install Python dependencies
    pip install -r requirements.txt

    touch .initialized
fi

# Run the application
/usr/bin/env python3 gui.py
