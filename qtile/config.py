## Import base Qtile functions
import os
import subprocess
import asyncio      # for spotify hook
from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras.widget.decorations import RectDecoration  # for decorations
from qtile_extras import widget

mod = "mod4"
terminal = "alacritty"

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
    Key([mod], "e", lazy.spawn("Thunar")),
    # Run "rofi-theme-selector" in terminal to select a theme
    Key([mod], "s", lazy.spawn("rofi -show drun")),
    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "g", lazy.spawn("pavucontrol")),

    # Screenshot
    Key([], "Print", lazy.spawn("flameshot gui")),
    
    # Use volume, audio and brigthness controls on your keyboard
    # Volume 
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Audio controls
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    #([], "XF86AudioPause", lazy.spawn("playerctl play-pause")),    # just in case
     
    # Brightness doesn't work for me (probably working only for laptop users)
    # Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    # Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]

# USING COLORS FROM TOKYO NIGHT, left are from Catppuccin
colors = {
    "white": "#b7c0ea",         # white-ish
    "grey": "#949cbe",          # grey-ish
    "pink": "#c099ff",          # pink
    "mauve": "#CBA6F7",
    "mint": "#70d4c5",          # mint
    "red": "#cf494a",           # red
    "maroon": "#EBA0AC",
    "orange": "#f49862",        # orange
    "yellow": "#d9aa66",        # yellow
    "green": "#9ac969",         # green
    "cyan": "#73daca",          # cyan
    "teal": "#94E2D5",
    "sky": "#89DCEB",
    "sapphire": "#74C7EC",
    "blue": "#759bed",          # blue
    "darkblue": "#545AA7",
    "purple": "#9577ce",        # purple
    "text": "#CDD6F4",          # black-ish
    "subtext1": "#BAC2DE",
    "subtext0": "#A6ADC8",
    "overlay2": "#9399b2",
    "overlay1": "#7F849C",
    "surface2": "#585B70",
    "systray": "#5d627d",       # systray
    "background": "#24283b",    # background
    "base": "#1E1E2E",
    "mantle": "#181825",
    "background_darker": "#1f2335", # background darker
    "transparent": "#00000000",
}

## Groups - Workspaces, tags or desktops (call them what you want),
# also open discord and spotify only on the second group. 
# I added layouts to second group to change order in which they are there
groups = [
    Group("1", label="1"),
    Group("2", label="2",
     layouts = [layout.Columns(
        border_focus = colors["red"],
        border_normal = colors["base"],
        border_on_single =False,
        fair = True,
     ), layout.Max()],
     matches=[Match(wm_class = "discord-canary"),
              Match(wm_class = "Spotify")]),
    Group("3", label = "3"),
    Group("4", label = "4"),
    Group("5", label = "5"),
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
        border_focus = colors["red"],
        border_normal = colors["base"],
        border_on_single =False,
        fair = True,
        margin = 3,     # GAPS
    ),
    # In order to change aspects of floating windows in other layouts,
    # see floating_layout at the Advanced section at the bottom
    layout.floating.Floating(
        border_focus = colors["red"],
        border_normal = colors["base"],
    ),
]


## Screens - Two different bars for two monitors (screen = monitor),
# get multihead (multimonitor) support working yourself (autostart.sh)

# default for widgets
widget_defaults = dict(
    font = "JetBrainsMono Nerd Font Mono Medium",
    fontsize = 14,
    padding = 0,
    margin = 0,
    # background = colors["background"],
    background = colors["transparent"],
    foreground = colors["background"],
)

# default decorations
decoration_defaults = dict(
    # colour = colors["white"],
    radius = 2,
    filled = True,
    group = True,
    padding = 4,
)

# bar settings
screens = [
    Screen(
        top = bar.Bar([
            widget.Systray(
                # background = colors["systray"],
                icon_size = 20,
                padding = 2,
            ),
            #widget.Sep(
            #   linewidth = 4,
            #   background = colors["systray"],
            #   foreground = colors["systray"],
            #),
            widget.Spacer(length = 5),
            widget.GroupBox(
                hide_unused = True,
                disable_drag = True,
                toggle = False,
                highlight_method = "block",
                borderwidth = 4,
                this_current_screen_border = colors["blue"],            # block fill color
                block_highlight_text_color = colors["background"],      # block text color
                active = colors["background_darker"],                   # text color
                other_screen_border = colors["grey"],                   # block fill color other screens
                inactive = colors["white"],
                urgent_alert_method = "block",
                urgent_border = colors["purple"],
                urgent_text = colors["red"],
                spacing = 4,
                margin_x = 6,
                margin_y = 3,                                           # push labels down
                padding_x = 2,
                padding_y = 2,
                decorations = [
                    RectDecoration(
                        colour = colors["white"],
                        **decoration_defaults,
                    )
                ],
            ),  
            widget.CurrentLayoutIcon(
                scale = 0.6,
                custom_icon_paths = [
                    os.path.expanduser("~/.config/qtile/assets/layout/"),
                ],
                decorations = [
                    RectDecoration(
                        colour = colors["white"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.TaskList(
                theme_path = "/usr/share/icons/Papirus/index.theme",
                theme_mode = "preferred",
                highlight_method = 'block',
                icon_size = 18,
                max_title_width = 150,
                margin = 1.9,                   # match to center
                padding = 6.5,                  # size of a block
                fontsize = 13,
                font = "JetBrainsMono",
                border = colors["background"],  # fill current window
                foreground = "#ffffff",         # text colors
                borderwidth = 3,                # icon position
                urgent_border = colors["red"],
                txt_floating = ' ',
                txt_minimized = '_ ',
            ),
            # RIGHT SIDE
            widget.Image(
                filename = '~/.config/qtile/assets/music.png',
                margin = 7,
                mouse_callbacks = {'Button3': lazy.spawn("spotify")},
                decorations = [
                    RectDecoration(
                        colour = colors["mint"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.Mpris2(
                name = "Spotify",
                objname = "org.mpris.MediaPlayer2.spotify",
                padding = 5,
                display_metadata = ["xesam:title", "xesam:artist"],
                playing_text = "{track}",
                paused_text  = "{track}",
                width = 150,
                scroll_interval = 0.1,
                mouse_callbacks = {'Button3': lazy.spawn("spotify")},
                decorations = [
                    RectDecoration(
                        colour = colors["mint"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.Image(
                filename = '~/.config/qtile/assets/update.png',
                margin = 7,
                mouse_callbacks = {'Button1': lazy.spawn("alacritty -e sudo pacman -Syu")},
                decorations = [
                    RectDecoration(
                        colour = colors["green"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.CheckUpdates(
                padding = 8,
                display_format = "{updates}",
                no_update_string = "0",
                colour_have_updates = colors["background"],
                colour_no_updates = colors["background"],
                mouse_callbacks = {'Button1': lazy.spawn("alacritty -e sudo pacman -Syu")},
                decorations = [
                    RectDecoration(
                        colour = colors["green"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.Volume(
                theme_path = '~/.config/qtile/assets/volume/',
                scroll_interval = 1.5,
                margin = 3,
                mouse_callbacks = {'Button3': lazy.spawn("pavucontrol")},
                decorations = [
                    RectDecoration(
                        colour = colors["red"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.PulseVolume(
                padding = 10,
                mouse_callbacks = {'Button3': lazy.spawn("pavucontrol")},
                decorations = [
                    RectDecoration(
                        colour = colors["red"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.Image(
                filename = '~/.config/qtile/assets/clock.png',
                margin = 7,
                mouse_callbacks = {'Button1': lazy.spawn("gsimplecal")},
                decorations = [
                    RectDecoration(
                        colour = colors["orange"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.Clock(
                padding = 8,
                format = "%A, %d %b %H:%M",
                mouse_callbacks = {'Button1': lazy.spawn("gsimplecal")},
                decorations = [
                    RectDecoration(
                        colour = colors["orange"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.Image(
                filename = '~/.config/qtile/assets/reboot.png',
                margin = 7,
                mouse_callbacks = {'Button1': lazy.spawn("sudo reboot now")},
                decorations = [
                    RectDecoration(
                        colour = colors["white"],
                        **decoration_defaults,
                    )
                ],
            ),
            widget.Image(
                filename = '~/.config/qtile/assets/shutdown.png',
                margin = 7,
                mouse_callbacks = {'Button1': lazy.spawn("sudo shutdown now")},
                decorations = [
                    RectDecoration(
                        colour = colors["white"],
                        **decoration_defaults,
                    )
                ],
            ),
            ],
            35, # WIDTH
            # margin = 4,
            margin = 2,
            background = colors["transparent"],
        ),
    ),
]

# Mouse
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
     start = lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
     start = lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

## Autostart (start only once - on boot)
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

## Advanced
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

## Spotify
@hook.subscribe.client_new
async def client_new(client):
  await asyncio.sleep(0.5)
  if client.name == 'Spotify':
    client.togroup("2")

floating_layout = layout.Floating(
    float_rules = [
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
    border_width = 1,
    border_focus = colors["red"],
    border_normal = colors["base"],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None

# for volume icon to appear
lazy.reload_config()
