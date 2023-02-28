#!/usr/bin/env sh

echo "Creating and entering virtual environment"
# Find a python executable
if command -v python; then
    cmd=python
elif command -v python3; then
    cmd=python
else
    echo "Unable to find python; is it installed?"
    exit 1
fi
echo "Using python cmd $cmd at" $(which $cmd)
python -m venv ./venv
venv/bin/activate

echo "Installing dependencies"
pip install -r requirements.txt
pip install -e .

echo "Installing node dependencies"
npm install
npm run compile

echo "Attempting to fetch and update scripts submodule"
./update_scripts.sh
