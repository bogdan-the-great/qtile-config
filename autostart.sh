#!/usr/bin/env bash

# Use "run program" to run it only if it is not already running
# Use "program &" to run it regardless

function run {
    if ! pgrep $1 > /dev/null ;
    then
        $@&
    fi
}

/home/piotr/.screenlayout/layout1.sh
nitrogen --restore &
redshift -P -O 3500 &
picom --backend glx &
firefox &
vscodium &
discord-canary &
spotify &
tutanota-desktop &
flameshot &
volctl &
