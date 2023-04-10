#!/usr/bin/env bash

# Use "run program" to run it only if it is not already running
# Use "program &" to run it regardless

function run {
    if ! pgrep $1 > /dev/null ;
    then
        $@&
    fi
}

# describe multimonitor
xrandr --output DVI-D-0 --mode 1280x1024 --pos 1920x210 --rotate normal --output HDMI-0 --off --output DP-0 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1 --off &
nitrogen --restore &    # wallpaper
redshift -P -O 3500 &   # night light
picom --backend glx &
firefox &
alacritty -e lvim &
discord-canary &
spotify &
tutanota-desktop &
flameshot &             # screenshots
pulseaudio --start &
