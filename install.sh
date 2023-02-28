#!/usr/bin/env sh

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}Creating and entering virtual environment${NC}"
# Find a python executable
if command -v python; then
    cmd=python
elif command -v python3; then
    cmd=python
else
    echo "${RED}Unable to find python; is it installed?${NC}"
    exit 1
fi
python_location=$(which $cmd)
echo -e "Using command ${CYAN}$cmd${NC} at ${CYAN}$python_location${NC}"
python -m venv ./venv
venv/bin/activate

echo -e "${CYAN}Installing dependencies${NC}"
pip install -r requirements.txt
pip install -e .

echo -e "${NC}Installing node dependencies${NC}"
npm install
npm run compile

echo -e "${NC}Attempting to fetch and update scripts submodule${NC}"
./update_scripts.sh

echo -e "${GREEN}finished installing!${NC}"
