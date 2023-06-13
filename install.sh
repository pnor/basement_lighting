#!/usr/bin/env sh
set -o errexit

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
CYAN=$(tput setaf 6)
NC=$(tput sgr0)

printf "%sCreating and entering virtual environment%s\n" "$CYAN" "$NC"
# Find a python executable
if command -v python3; then
    cmd=python3
elif command -v python; then
    if [ "$(python --version | awk '{ print(substr($2, 0, 1)) }')" != "3" ]; then
        printf "$%sPython at was not Python3!%s\n" "$RED" "$NC"
        printf "Using python at %s%s%s\n" "$RED" "$(which python)" "$NC"
        exit 1
    fi
    cmd=python
else
    printf "%sUnable to find python; is it installed?%s\n" "$RED" "$NC"
    exit 1
fi
printf "Using command %s%s%s at %s%s%s\n" "$CYAN" "$cmd" "$NC" "$CYAN" "$(which $cmd)" "$NC"
$cmd -m venv ./venv
. venv/bin/activate

printf "%sInstalling dependencies%s" "$CYAN" "$NC"
if [ "$(uname)" = "Darwin" ]; then
    printf "%s ~ Installing on MacOS; omitting rs_ws281x in build%s\n" "$CYAN" "$NC"
    if ! pip install -r requirements_macos.txt; then
        printf "%sError occured while installing dependencies ): %s\n" "$RED" "$NC"
        exit 1
    fi
else
    printf "%s ~ Assuming Linux%s\n" "$CYAN" "$NC"
    if ! pip install -r requirements.txt; then
        printf "%sError occured while installing dependencies ): %s\n" "$RED" "$NC"
        exit 1
    fi
fi
pip install -e .

printf "%sInstalling node dependencies%s\n" "$CYAN" "$NC"
npm install
npm run compile

printf "%sfinished installing!%s\n" "$GREEN" "$NC"
printf "Can fetch light scripts to run with %s ./update_scripts.sh%s or add your own in %s scripts/light_scripts%s\n" "$CYAN" "$NC" "$CYAN" "$NC"
