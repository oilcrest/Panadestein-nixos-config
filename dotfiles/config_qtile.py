r"""Qtile configuration.

  ___  _   _ _
 / _ \| |_(_) | ___
| | | | __| | |/ _ \
| |_| | |_| | |  __/
 \__\_\\__|_|_|\___|

100% PEP8 compliant.
"""
import os
import socket
import subprocess
from typing import List
from pathlib import Path
from libqtile import qtile
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.dgroups import simple_key_binder
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Define global variables

mod = "mod4"
terminal = guess_terminal()
dgroups_key_binder = simple_key_binder("mod4")
ranp = f"{Path.home()}/.config/scripts/randr_conf.sh"
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
cmdh = 'python -c "print(`qtile cmd-obj -o cmd -f display_kb`)" | rofi -dmenu'

# Useful colors
# https://www.schemecolor.com/python-logo-colors.php

cl_pal = {
    "cazure": ["#4b8bbe", "#4b8bbe"],
    "sunglow": ["#ffe873", "#ffe873"],
    "amag": ["#c678dd", "#c678dd"]
}

# Define keybindings

keys = [
    # Get help
    Key([mod], "F1", lazy.spawn(cmdh, shell=True)),

    # Applications
    Key([mod], "Return", lazy.spawn(terminal),
        desc="Launches detected terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("alacritty -e ipython"),
        desc="Launches a handy Ipython session"),
    Key([mod], "r", lazy.spawn("rofi -show drun -show-icons"),
        desc="Triggers the Rofi launcher"),
    Key([mod, "shift"], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key([mod], "w", lazy.spawn("firefox"),
        desc="Launches the Firefox web browser"),
    Key([mod], "e", lazy.spawn("emacsclient -c"),
        desc="Launches an emacsclient frame"),
    Key([mod], "v", lazy.spawn("neovide"),
        desc="Launches Neovide"),
    Key([mod, "shift"], "f", lazy.spawn("nautilus"),
        desc="Launches the Nautilus file browser"),
    Key([mod], "f", lazy.spawn("alacritty -e ranger"),
        desc="Launches the Ranger file browser"),
    Key([mod], "f", lazy.spawn("alacritty -e ranger"),
        desc="Launches the Ranger file browser"),
    Key([], "Print",
        lazy.spawn("maim -s | xclip -selection clipboard -t image/png"),
        desc="Takes a screenshot with the Maim utility"),

    # Media Keys
    Key([], 'XF86AudioLowerVolume', lazy.spawn("amixer set Master 5%- unmute"),
        desc="Lowers volume"),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("amixer set Master 5%+ unmute"),
        desc="Raises volume"),
    Key([], 'XF86MonBrightnessDown',   lazy.spawn("brightnessctl -q s 10%-"),
        desc=("Decreases brightness")),
    Key([], 'XF86MonBrightnessUp',   lazy.spawn("brightnessctl -q s +10%"),
        desc=("Increases brightness")),

    # Display Manager
    Key([mod], "o", lazy.spawn("dm-tool lock"),
        desc="Locks the screen"),
    Key([mod], "m",
        lazy.spawn(ranp), desc="Ensures external monitor usage"),

    # Session control
    Key([mod, "shift"], "x", lazy.spawn("shutdown now"),
        desc="Shutdown the box"),
    Key([mod, "shift"], "BackSpace", lazy.spawn("reboot"),
        desc="Reboot the box"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Window control
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(),
        desc="Move window focus to the next window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),
        desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Layouts control
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
]

# Define groups (workspaces)

groups = [Group("dev", layout='monadtall'),
          Group("tty", layout='monadtall'),
          Group("doc", layout='monadtall'),
          Group("www", layout='monadtall',
                matches=[Match(wm_class=["firefox"])]),
          Group("msg", layout='monadtall',
                matches=[Match(wm_class=["Mattermost",
                                         "Slack",
                                         "TelegramDesktop"])]),
          Group("com", layout='monadtall',
                matches=[Match(wm_class=["Skype",
                                         "zoom"])]),
          Group("rnd", layout='monadtall'),
          Group("art", layout='floating',
                matches=[Match(wm_class=["gimp-2.10"])])
          ]

# Layouts

layout_theme = {
    "border_width": 1,
    "margin": 6,
    "border_focus": "#8f3d3d",
    "border_normal": "#267CB9"
}

layouts = [
    # No need more than this
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme, single_border_width=0,
                     single_margin=0, new_client_position='bottom'),
    layout.Columns(**layout_theme),
    layout.Floating(**layout_theme)
]

# Widgets configuration

widget_defaults = dict(
    font='Fira Code',
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

# Status bar configuration

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename="~/.config/qtile/python_icon.png",
                    scale="True",
                    mouse_callbacks={
                        'Button1':
                        lambda: qtile.cmd_spawn("alacritty -e ipython")}
                ),
                widget.Sep(linewidth=0, padding=6),
                widget.TextBox("|", foreground='#ffe873'),
                widget.GroupBox(
                    fontsize=15,
                    margin_y=3,
                    margin_x=0,
                    padding_y=5,
                    padding_x=3,
                    active=cl_pal["cazure"],
                    inactive=cl_pal["sunglow"],
                    highlight_method="block",
                    block_highlight_text_color=cl_pal["amag"],
                    borderwidth=3,
                    rounded=True
                ),
                widget.TextBox("|", foreground='#ffe873'),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentLayout(
                    padding=5,
                    foreground=cl_pal["sunglow"]
                ),
                widget.TextBox("|", foreground='#ffe873'),
                widget.Volume(
                    fmt='Vol: {}',
                    padding=5
                ),
                widget.TextBox("|", foreground='#ffe873'),
                widget.CPU(
                    format="CPU {load_percent}%",
                    mouse_callbacks={
                        'Button1':
                        lambda: qtile.cmd_spawn("alacritty -e htop")
                    }
                ),
                widget.TextBox("|", foreground='#ffe873'),
                widget.Systray(),
                widget.TextBox("|", foreground='#ffe873'),
                widget.Clock(format='%d.%m %a %I:%M %p',
                             mouse_callbacks={
                                 'Button1':
                                 lambda: qtile.cmd_spawn(
                                     "alacritty -e calcurse")
                             })
            ],
            25,
        ),
    ),
]

# Floating window control

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Internal Qtile options

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = True
cursor_warp = True

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(title='guake'),  # A drop-down terminal
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# Startup processes


@hook.subscribe.startup_once
def start_once():
    """Startup processes."""
    subprocess.call([f"{Path.home()}/.config/scripts/qtile_autostart.sh"])


# Dirty Java hack

wmname = "LG3D"
