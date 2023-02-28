#!/usr/bin/env sh
set -o errexit

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "${CYAN}Creating and entering virtual environment${NC}"
# Find a python executable
if command -v python; then
    cmd=python
elif command -v python3; then
    cmd=python3
else
    echo "${RED}Unable to find python; is it installed?${NC}"
    exit 1
fi
python_location=$(which $cmd)
echo "Using command ${CYAN}$cmd${NC} at ${CYAN}$python_location${NC}"
$cmd -m venv ./venv
. venv/bin/activate

echo "${CYAN}Installing dependencies${NC}"
if [[ $(uname) == "Darwin" ]]; then
    echo "${CYAN} ~ Installing on MacOS; omitting rs_ws281x in build${NC}"
    pip install -r requirements_macos.txt
else
    echo "${CYAN} ~ Assuming Linux${NC}"
    pip install -r requirements.txt
fi
pip install -e .

echo "${NC}Installing node dependencies${NC}"
npm install
npm run compile

echo "${GREEN}finished installing!${NC}"
echo "Can fetch light scripts to run with ${CYAN}./update_scripts.sh${NC} or add your own in ${CYAN}scripts/light_scripts${NC}"
