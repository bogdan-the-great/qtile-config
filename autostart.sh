#!/usr/bin/env bash
function run {
    if ! pgrep $1 > /dev/null ;
    then
        $@&
    fi
}

/home/piotr/.screenlayout/layout1.sh
nitrogen --restore &
picom &
firefox &
discord-canary &
flameshot &
volctl &
