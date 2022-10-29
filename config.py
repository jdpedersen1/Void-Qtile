# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401
from libqtile.backend.x11 import window
from libqtile.confreader import ConfigError
from libqtile.widget import base
XEMBED_PROTOCOL_VERSION = 0

#=-/ Created variables /-=#
mod = "mod1" 
myTerm = "alacritty" 
myBrowser = "brave-browser-stable"
logoutMenu = "kitty -e herbst-logout.sh"

#=-/ Keybindings /-=#
keys = [
         #=-/ Main sys control /-=#
         Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
         Key([mod, "shift"], "q", lazy.window.kill(), desc='Kill active window'),
         Key([mod, "control"], "r", lazy.restart(), desc='Restart Qtile'),

         #=-/ Terminals /-=#
         Key([mod, "shift"], "Return", lazy.spawn(myTerm), desc='Run Launcher'),
         Key([mod, "shift"], "a", lazy.spawn("alacritty")),
         Key([mod, "shift"], "s", lazy.spawn("kitty -e bettercd.sh"), desc='my file manager'),

         #=-/ Browsers /-=#
         Key([mod, "shift"], "b", lazy.spawn(myBrowser), desc='brave-browser-stable'),
         Key([mod, "shift"], "f", lazy.spawn("firefox"), desc='another browser'),
         Key([mod, "shift"], "l", lazy.spawn("librewolf"), desc='school browser'),

         #=-/ Window manipulation /-=#
         Key([mod], "j", lazy.layout.down(), desc='Move focus down in current stack pane'),
         Key([mod], "k", lazy.layout.up(), desc='Move focus up in current stack pane'),
         Key([mod, "shift"], "j", lazy.layout.shuffle_down(), lazy.layout.section_down(), desc='Move windows down in current stack'),
         Key([mod, "shift"], "k", lazy.layout.shuffle_up(), lazy.layout.section_up(), desc='Move windows up in current stack'),
         Key([mod], "h", lazy.layout.shrink(), lazy.layout.decrease_nmaster(), desc='Shrink window (MonadTall), decrease number in master pane (Tile)'),
         Key([mod], "l", lazy.layout.grow(), lazy.layout.increase_nmaster(), desc='Expand window (MonadTall), increase number in master pane (Tile)'),
         Key([mod], "n", lazy.layout.normalize(), desc='normalize window size ratios'),
         Key([mod], "m", lazy.layout.maximize(), desc='toggle window between minimum and maximum sizes'),
         Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
         
         #=-/ Stack and master manipulation /-=#
         Key([mod, "shift"], "Tab", lazy.layout.rotate(), lazy.layout.flip(), desc='flip master and stack'),
         Key([mod], "space", lazy.layout.next(), desc='Switch window focus to other pane(s) of stack'),
         
         #=-/ Multimedia keys /-=#
         Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -10%")),
         Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +10%")),
         Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

         #=-/ Scratchpads /-=#
         Key([mod], "Return", lazy.group['scratchpad'].dropdown_toggle('term')),
         Key([mod, "shift"], "d", lazy.group['menu'].dropdown_toggle('launch')),
         Key([mod, "shift"], "c", lazy.group['logout'].dropdown_toggle('exitMenu')),
         Key([mod], "t", lazy.group['music'].dropdown_toggle('tunes')),
]

#=-/ Window groups settings /-=#
groups = [Group(" 1 ", layout='monadtall'),
          Group(" 2 ", layout='monadtall'),
          Group(" 3 ", layout='monadtall'),
          Group(" 4 ", layout='monadtall'),
          Group(" 5 ", layout='monadtall'),
          Group(" 6 ", layout='monadtall'),
          Group(" 7 ", layout='monadtall'),
          Group(" 8 ", layout='monadtall'),
          Group(" 9 ", layout='monadtall'),
          #=-/ Scratchpad groups /-=#
          ScratchPad("music",[DropDown("tunes", "alacritty -e ncmpcpp", x=0.05, y=0.02, width=0.90, height=0.6, on_focus_lost_hide=False)]),
          ScratchPad("menu",[DropDown("launch", "alacritty -e launch.sh", x=0.33, y=0.02, width=0.35, height=0.95, on_focus_lost_hide=False)]),
          ScratchPad("logout",[DropDown("exitMenu", "kitty -e herbst-logout.sh", x=0.40, y=0.30, width=0.20, height=0.20, on_focus_lost_hide=False)]),
          ScratchPad("scratchpad",[DropDown("term", "alacritty", x=0.12, y=0.02, width=0.75, height=0.6, on_focus_lost_hide=False)]),
]

from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod1")

#=-/ Layout settings /-=#
layout_theme = {"border_width": 2,
                "margin": 6,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    layout.Matrix(**layout_theme),
    layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

#=-/ System colors /-=#
colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#5f875f", "#5f875f"],
          ["#000000", "#000000"],
          ["#51afef", "#51afef"],
          ["#259ec1", "#259ec1"],
          ["#46d9ff", "#46d9ff"],
          ["#1f5b70", "#1f5b70"]]

#=-/ Default settings for widgets /-=#
widget_defaults = dict(
    font="Hermit Bold",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

#=-/ Widgets /-=#
def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0, padding = 6,
                       foreground = colors[2], background = colors[5]
                       ),
              widget.Image(
                       filename = "~/Downloads/artix-logo.png", scale = "False",
                       background = colors[5],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
                       ),
             widget.TextBox(
                       text = ' ', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[0], foreground = colors[5],
                       padding = 0
                       ),
              widget.Sep(
                       linewidth = 0, padding = 0,
                       foreground = colors[2], background = colors[5]
                       ),
              widget.GroupBox(
                       font = "FontAwesome Bold", fontsize = 12,
                       margin_y = 3, margin_x = 0, padding_y = 5, padding_x = 3,
                       borderwidth = 3, rounded = False,
                       active = colors[2], inactive = colors[7],
                       highlight_color = colors[1], highlight_method = "line",
                       this_current_screen_border = colors[4], this_screen_border = colors [4],
                       other_current_screen_border = colors[6], other_screen_border = colors[4],
                       foreground = colors[2], background = colors[0]
                       ),
             widget.TextBox(
                       text = '', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[5], foreground = colors[0],
                       padding = 0
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2], background = colors[5],
                       padding = 6, scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[7], background = colors[5],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[5], foreground = colors[5],
                       padding = 0
                       ),
              widget.WindowName(
                       foreground = colors[2], background = colors[5],
                       padding = 0
                       ),
              widget.TextBox(
                       text='', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[5], foreground = colors[0],
                       padding = 0
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
              widget.Sep(
                       linewidth = 0, padding = 6,
                       foreground = colors[0], background = colors[0]
                       ),
              widget.TextBox(
                       text='', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[0], foreground = colors[5],
                       padding = 0
                       ),
              widget.CheckUpdates(
                       update_interval = 10, distro = "Arch_checkupdates",
                       display_format = "System: {updates}  ",
                       foreground = colors[2], background = colors[5], colour_have_updates = colors[2], colour_no_updates = colors[2],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syyu')},
                       padding = 5,
                       ),
              widget.TextBox(
                       text = '', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[5], foreground = colors[7],
                       padding = 0
                       ),
               widget.GenPollText(
                       name = "ytsubs",
                       fmt = " " " {} ", update_interval = 3600,
                       foreground = colors[1], background = colors[7],
                       func = lambda: subprocess.check_output("/home/jake/.local/scripts/ytsubs.sh").decode("utf-8"),
                       padding = 0
                       ),
              widget.TextBox(
                       text ='', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[7], foreground = colors[0],
                       padding = 0
                       ),
              widget.Clock(
                       foreground = colors[4], background = colors[0],
                       format = "%A, %B %d - %H:%M ",
                       padding = 5
                       ),
              widget.TextBox(
                       text = '', font = "Ubuntu Mono", fontsize = 37,
                       background = colors[0], foreground = colors[5],
                       padding = 0
                       ),
              widget.Sep(
                       linewidth = 0, padding = 20,
                       foreground = colors[2], background = colors[5]
                       ),
              ]
    return widgets_list

#=-/ Set bar to screen /-=#
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

#=-/ Set bar height and opacity, also set wallpaper /-=#
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20),
            wallpaper='~/.config/herbstluftwm/wallpaper/teal/city.jpg',
            wallpaper_mode='fill')]

#=-/ Initiate functions for screens and widgets /-=#
if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()

#=-/ Mouse settings /-=#
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#=-/ Cursor rules /-=#
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True

#=-/ Window rules /-=#
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

