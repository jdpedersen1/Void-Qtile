#!/usr/bin/env bash

# Created By: Jake@Linux
# Created On: Mon 29 Aug 2022 09:08:33 AM CDT
# Project: autostart for qtile

picom --experimental-backend &
xfce4-power-manager &
#volumeicon &
pa-applet &
cbatticon  -i notification /sys/class/power_supply/BAT0 &
nm-applet &
mpd --no-daemon $HOME/.config/mpd/mpd.conf &
$HOME/.config/herbstluftwm/updicon.sh &
