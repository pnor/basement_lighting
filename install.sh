#!/usr/bin/env sh

echo "Installing dependencies"
pip install -r requirements.txt
pip install -e .

echo "Installing node dependencies"
npm install
npm run compile
