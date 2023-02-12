## Import base Qtile functions
import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = "alacritty"
# If your terminal is alacritty or has support for options --hold and -e (which is unlikely) don't change it here.
# Otherwise go and change these widgets one by one to work with your terminal:
# CheckUpdates
# Mpris2
# NvidiaSensors
# CPU
# Memory
# Net
# Clock - using gsimplecal, remember to have custom config, in order to open below date and time

## Keybindings - Custom keybindings are below defaults
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    # Controls for Max layout ("a" and "d") to change focus windows
    Key([mod], "a", lazy.layout.up().when(layout="max")),
    Key([mod], "d", lazy.layout.down().when(layout="max")),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),

    ## CUSTOM
    # Spawn apps
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "e", lazy.spawn("pcmanfm")),
    # Run "rofi-theme-selector" in terminal to select a theme
    Key([mod], "s", lazy.spawn("rofi -show drun")),
    Key([mod], "c", lazy.spawn("vscodium")),
    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "g", lazy.spawn("pavucontrol")),

    # Screenshot
    Key([], "Print", lazy.spawn("flameshot gui")),
    
    # Use volume, audio and brigthness controls on your keyboard
    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Audio controls
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    #([], "XF86AudioPause", lazy.spawn("playerctl play-pause")),    # just in case
     
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]

## Colors
colors = [
    ["#292d3e", "#292d3e"],  # 0 - panel background
    ["#434758", "#434758"],  # 1 - lighter background
    ["#ffffff", "#ffffff"],  # 2 - white - font color for group names
    ["#464cd6", "#464cd6"],  # 3 - blue darker
    ["#8d62a9", "#8d62a9"],  # 4 - purple normal - color for other tab and odd widgets
    ["#668bd7", "#668bd7"],  # 5 - blue
    ["#e1acff", "#e1acff"],  # 6 - pink
    ["#000000", "#000000"],  # 7 - black
    ["#AD343E", "#AD343E"],  # 8 - red
    ["#db5d4d", "#db5d4d"],  # 9 - orange - current tab color
    ["#DA8C10", "#DA8C10"],  # 10 - yellow/gold
    ["#F7DC6F", "#F7DC6F"],  # 11 - yellow bright
    ["#f1ffff", "#f1ffff"],  # 12 - almost white
    ["#4c566a", "#4c566a"],  # 13 - greyish
    ["#387741", "#387741"],  # 14 - green
]

## Groups - Workspaces, tags or desktops (call them what you want),
# also open discord only on the second group 
groups = [
    Group("1", label=" "),
    Group("2", label=" "),
    Group("3", label=" "),
    Group("4", label=" "),
    Group("5", label=" "),
]

# Magic behind groups
for i in groups:
    keys.extend([
            # mod1 + letter of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True))
        ]
    )

## Layouts - Max as main, floating as layout not floating rules to windows
layouts = [
            layout.Max(),
            layout.Columns(
                border_focus=colors[6],
                border_normal=colors[1],
                border_on_single=False,
                fair=True,
            ),
            # In order to change aspects of floating windows in other layouts,
            # see floating_layout at the Advanced section at the bottom
            layout.floating.Floating(
                border_focus=colors[6],
                border_normal=colors[1],
            ),
            layout.TreeTab(
                font="Ubuntu",
                fontsize=10,
                border_width=2,
                bg_color=colors[0],
                active_bg=colors[9],
                active_fg=colors[12],
                inactive_bg=colors[1],
                inactive_fg=colors[12],
                padding_left=0,
                panel_width=175,
                vspace=2,
            ),
            layout.RatioTile(
                border_focus=colors[6],
                border_normal=colors[1],
            ),
]

## Screens - Two different bars for two monitors (screen = monitor),
# get multihead (multimonitor) support working yourself, I configured Xrandr with Arandr
screens = [
    Screen(
        top=bar.Bar([
            widget.CurrentLayoutIcon(
                foreground=colors[0],
                background=colors[0],
                padding=0,
                scale=0.6,
            ),
            widget.GroupBox(
                fontsize=12,
                margin_y=2,
                margin_x=0,
                padding_y=5,
                padding_x=3,
                borderwidth=3,
                active=colors[2],
                inactive=colors[1],
                rounded=False,
                highlight_method='block',
                urgent_alert_method='block',
                this_current_screen_border=colors[9],
                this_screen_border=colors[4],
                other_current_screen_border=colors[0],
                other_screen_border=colors[0],
                foreground=colors[2],
                background=colors[0],
                disable_drag=True,
            ),
            widget.Sep(
                linewidth=0,
                padding=10,
                foreground=colors[2],
                background=colors[0],
            ),
            widget.TaskList(
                theme_path="/usr/share/icons/Papirus/index.theme",
                theme_mode="preferred",
                highlight_method = 'block',
                icon_size=14,
                max_title_width=100,
                rounded=False,
                margin=0,
                padding=3,
                fontsize=10,
                border=colors[9],
                foreground=colors[2],
                borderwidth = 0,
                background=colors[0],
                urgent_border=colors[2],
                txt_floating='🗗 ',
                txt_minimized='_ ',
            ),

            # POWERLINE:
            widget.Sep(
                linewidth=0,
                padding=10,
                foreground=colors[1],
                background=colors[0],
            ),
            widget.TextBox(
                text='',
                background=colors[0],
                foreground=colors[1],
                padding=-6,
                fontsize=37,
            ),
            widget.Systray(
                background=colors[1],
                icon_size=15,
                padding=5
            ),
            widget.Sep(
                linewidth=0,
                padding=5,
                foreground=colors[2],
                background=colors[1],
            ),
            widget.TextBox(
                text='',
                background=colors[1],
                foreground=colors[10],
                padding=-6,
                fontsize=37,
            ),
            widget.Mpris2(
                foreground=colors[2],
                background=colors[10],
                padding=5,
                name="spotify",
                display_metadata=["xesam:title", "xesam:artist"],
                objname="org.mpris.MediaPlayer2.spotify",
                #playing_text = "契 {track}",
                paused_text  = " {track}",
                width=150,
                mouse_callbacks={'Button3': lazy.spawn("spotify")},
            ),
            widget.TextBox(
                text='',
                background=colors[10],
                foreground=colors[4],
                padding=-6,
                fontsize=37,
            ),
            widget.CheckUpdates(
                execute="alacritty -e sudo pacman -Syu",
                background=colors[4],
                foreground=colors[3],
                colour_no_updates=colors[2],
                colour_have_updates=colors[12],
                padding=5,
                no_update_string='No updates',
                mouse_callbacks={'Button1': lazy.spawn("alacritty -e sudo pacman -Syu")},
            ),
            widget.TextBox(
                text='',
                foreground=colors[3],
                background=colors[4],
                padding=-6,
                fontsize=37,
            ),
            widget.NvidiaSensors(
                foreground=colors[2],
                background=colors[3],
                format="🌡  {temp}°C  {fan_speed}",
                mouse_callbacks={'Button1': lazy.spawn(terminal + " --hold -e watch -n 2 nvidia-smi")},
            ),
            widget.TextBox(
                text='',
                foreground=colors[8],
                background=colors[3],
                padding=-6,
                fontsize=37,
            ),
            widget.CPU(
                foreground=colors[2],
                background=colors[8],
                format="▣  {freq_current} Ghz {load_percent}%",
                mouse_callbacks={'Button1': lazy.spawn(terminal + " --hold -e watch -n 2 sensors")},
            ),
            widget.TextBox(
                text='',
                foreground=colors[13],
                background=colors[8],
                padding=-6,
                fontsize=37,
            ),
            widget.Memory(
                foreground=colors[2],
                background=colors[13],
                format="▥▥  {MemUsed: .0f}{mm} ",
                mouse_callbacks={
                    'Button1': lazy.spawn(terminal + " --hold -e htop"),                    # left click
                    'Button3': lazy.spawn(terminal + " --hold -e watch -n 2 free -th"),     # right click
                },
            ),
            widget.TextBox(
                text='',
                foreground=colors[14],
                background=colors[13],
                padding=-6,
                fontsize=37,
            ),
            widget.Net(
                foreground=colors[2],
                background=colors[14],
                prefix='M',
                format="🌐  {down} 🠟🠝{up}",
                mouse_callbacks={'Button1': lazy.spawn(terminal + " --hold -e ip addr")},
            ),
            widget.TextBox(
                text='',
                foreground=colors[5],
                background=colors[14],
                padding=-6,
                fontsize=37,
            ),
            widget.Clock(
                foreground=colors[2],
                background=colors[5],
                padding=4,
                format="⏲   %b %d %H:%M",
                mouse_callbacks={'Button1': lazy.spawn("gsimplecal")},
            ),
            widget.TextBox(
                text='',
                foreground=colors[9],
                background=colors[5],
                padding=-6,
                fontsize=37,
            ),
            widget.LaunchBar(
                progs=[
                    ("🗘", "reboot", "reboot"),
                    ("⏼ ", "shutdown now", "shutdown"),
                ],
                background=colors[9],
                padding = 1,
            )
            ], 20,
        ),
    ),
    Screen(
        top=bar.Bar([
            widget.CurrentLayoutIcon(
                custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                foreground=colors[0],
                background=colors[0],
                padding=0,
                scale=0.6,
            ),
            widget.GroupBox(
                font="Ubuntu Bold",
                fontsize=12,
                margin_y=2,
                margin_x=0,
                padding_y=5,
                padding_x=3,
                borderwidth=3,
                active=colors[2],
                inactive=colors[1],
                rounded=False,
                # highlight_color=self.colors[9],
                # highlight_method="line",
                highlight_method='block',
                urgent_alert_method='block',
                # urgent_border=self.colors[9],
                this_current_screen_border=colors[9],
                this_screen_border=colors[4],
                other_current_screen_border=colors[0],
                other_screen_border=colors[0],
                foreground=colors[2],
                background=colors[0],
                disable_drag=True,
            ),
            widget.Sep(
                linewidth=0,
                padding=10,
                foreground=colors[2],
                background=colors[0],
            ),
            widget.TaskList(
                theme_path="/usr/share/icons/Papirus/index.theme",
                theme_mode="preferred",
                highlight_method = 'block',
                icon_size=14,
                max_title_width=100,
                rounded=False,
                margin=0,
                padding=3,
                fontsize=10,
                border=colors[9],
                foreground=colors[2],
                borderwidth = 0,
                background=colors[0],
                urgent_border=colors[2],
                txt_floating='🗗 ',
                txt_minimized='_ ',
            ),
        ], 20, opacity=1),
    ),
]

# Mouse
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
     start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
     start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

## Autostart (start only once - on boot)
@hook.subscribe.startup_once
def autostart():
    home=os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

## Advanced
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    # Change aspects of floating windows in every layout
    border_width=1,
    border_focus=colors[6],
    border_normal=colors[7],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
