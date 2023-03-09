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
     
    # Brightness doesn't working for me (probably working only for laptop users)
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]

# USING COLORS FROM CATPPUCCIN MOCHA
colors_catppuccin = {
    "rosewater": "#F5E0DC",
    "flamingo": "#F2CDCD",
    "pink": "#F5C2E7",
    "mauve": "#CBA6F7",
    "red": "#F38BA8",
    "maroon": "#EBA0AC",
    "peach": "#FAB387",
    "yellow": "#F9E2AF",
    "green": "#A6E3A1",
    "teal": "#94E2D5",
    "sky": "#89DCEB",
    "sapphire": "#74C7EC",
    "blue": "#89B4FA",
    "darkblue": "#545AA7",
    "lavender": "#B4BEFE",
    "text": "#CDD6F4",
    "subtext1": "#BAC2DE",
    "subtext0": "#A6ADC8",
    "overlay2": "#9399b2",
    "overlay1": "#7F849C",
    "surface2": "#585B70",
    "surface1": "#45475A",
    "surface0": "#313244",
    "base": "#1E1E2E",
    "mantle": "#181825",
    "crust": "#11111B",
    "transparent": "#00000000",
}

## Groups - Workspaces, tags or desktops (call them what you want),
# also open discord and spotify only on the second group. 
# I added layouts to second group to change order in which they are there
groups = [
    Group("1", label="1"),
    Group("2", label="2",
     layouts = [layout.Columns(
        border_focus = colors_catppuccin["red"],
        border_normal = colors_catppuccin["base"],
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
                border_focus = colors_catppuccin["red"],
                border_normal = colors_catppuccin["base"],
                border_on_single =False,
                fair = True,
                margin = 3,     # GAPS
            ),
            # In order to change aspects of floating windows in other layouts,
            # see floating_layout at the Advanced section at the bottom
            layout.floating.Floating(
                border_focus = colors_catppuccin["red"],
                border_normal = colors_catppuccin["base"],
            ),
]


## Screens - Two different bars for two monitors (screen = monitor),
# get multihead (multimonitor) support working yourself, I configured Xrandr with Arandr

# default for widgets
widget_defaults = dict(
    font = "JetBrainsMono Nerd Font Mono Medium",
    fontsize = 14,
    padding = 0,
    margin = 0,
    background = colors_catppuccin["surface0"],
    foreground = colors_catppuccin["surface0"],
)

screens = [
    Screen(
        top=bar.Bar([
            widget.Systray(
                background = colors_catppuccin["surface1"],
                icon_size = 20,
                padding = 2,
            ),
            widget.Sep(
                linewidth = 4,
                background = colors_catppuccin["surface1"],
                foreground = colors_catppuccin["surface1"],
            ),
            widget.Spacer(length = 10),
            widget.GroupBox(
                hide_unused = True,
                disable_drag = True,
                toggle = False,
                highlight_method = "block",
                borderwidth = 4,
                this_current_screen_border = colors_catppuccin["blue"],         # block fill color
                block_highlight_text_color = colors_catppuccin["surface0"],     # block text color
                active = colors_catppuccin["crust"],                            # text color
                other_screen_border = colors_catppuccin["flamingo"],            # block fill color other groups
                inactive = colors_catppuccin["rosewater"],
                urgent_alert_method = "block",
                urgent_border = colors_catppuccin["lavender"],
                urgent_text = colors_catppuccin["red"],
                spacing = 4,
                margin_x = 6,
                margin_y = 3,                                                   # push labels down
                padding_x = 2,
                padding_y = 2,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["rosewater"],
                        radius = 2,
                        filled = True,
                        padding = 4,
                        # group=True
                    )
                ],
            ),  
            widget.Spacer(length = 10),
            widget.TaskList(
                theme_path = "/usr/share/icons/Papirus/index.theme",
                theme_mode = "preferred",
                highlight_method = 'block',
                icon_size = 18,
                max_title_width = 150,
                margin = 2.1,           # match to center
                padding = 6.5,          # size of a block
                fontsize = 13,
                border = colors_catppuccin["base"],
                foreground = "#ffffff",
                borderwidth = 3,        # icon position
                urgent_border = colors_catppuccin["red"],
                txt_floating = '🗗 ',
                txt_minimized = '_ ',
            ),
            # RIGHT SIDE
            widget.Image(
                filename = '~/.config/qtile/assets/music.png',
                margin = 7,
                #padding = 6,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["yellow"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
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
                        colour = colors_catppuccin["yellow"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.Spacer(length = 10),
            widget.Image(
                filename = '~/.config/qtile/assets/update.png',
                margin = 7,
                #padding = 6,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["green"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.CheckUpdates(
                padding = 8,
                display_format = "{updates}",
                no_update_string = "0",
                colour_have_updates = colors_catppuccin["surface0"],
                colour_no_updates = colors_catppuccin["surface0"],
                mouse_callbacks = {'Button1': lazy.spawn("alacritty -e sudo pacman -Syu")},
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["green"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.Spacer(length = 10),
            widget.Volume(
                theme_path = '~/.config/qtile/assets/volume/',
                scroll_interval = 1.5,
                margin = 3,
                #padding = 6,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["red"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.PulseVolume(
                padding = 10,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["red"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.Spacer(length = 10),
            widget.Image(
                filename = '~/.config/qtile/assets/keyboard.png',
                margin = 7,
                #padding = 6,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["blue"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.KeyboardKbdd(
                configured_keyboards = ["PL", "US", "ES"],
                padding = 8,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["blue"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            #widget.Spacer(length = 10),
            #widget.Image(
            #    filename = '~/.config/qtile/assets/memory.png',
            #    margin = 3,
            #    padding = 6,
            #    decorations = [
            #        RectDecoration(
            #            colour = colors_catppuccin["lavender"],
            #            radius = 2,
            #            filled = True,
            #            group = True,
            #            padding = 4,
            #        )
            #    ],
            #),
            #widget.Memory(
            #    padding = 1,
            #    format = "{MemUsed: .0f}{mm} ",
            #    mouse_callbacks = {
            #        'Button1': lazy.spawn(terminal + " --hold -e htop"),                    # left click
            #        'Button3': lazy.spawn(terminal + " --hold -e watch -n 2 free -th"),     # right click
            #    },
            #    decorations = [
            #        RectDecoration(
            #            colour = colors_catppuccin["lavender"],
            #            radius = 2,
            #            filled = True,
            #            group = True,
            #            padding = 4,
            #        )
            #    ],
            #),
            #widget.Spacer(length = 10),
            #widget.WiFiIcon(
            #    interface = "enp2s0f0u1",
            #    wifi_arc = 75,
            #    active_colour = colors_catppuccin["blue"],
            #    inactive_colour = colors_catppuccin["crust"],
            #    padding = 10,
            #    expanded_timeout = 3,
            #    decorations = [
            #        RectDecoration(
            #            colour = colors_catppuccin["peach"],
            #            radius = 2,
            #            filled = True,
            #            group = True,
            #            padding = 4,
            #        )
            #    ],
            #),
            widget.Spacer(length = 10),
            widget.Image(
                filename = '~/.config/qtile/assets/clock.png',
                margin = 7,
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["peach"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.Clock(
                padding = 8,
                format = "%A, %d %b %H:%M",
                mouse_callbacks = {'Button1': lazy.spawn("gsimplecal")},
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["peach"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.Spacer(length = 10),
            widget.CurrentLayoutIcon(
                padding = 0,
                scale = 0.6,
                custom_icon_paths = [
                    os.path.expanduser("~/.config/qtile/assets/layout/"),
                ],
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["rosewater"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.Image(
                filename = '~/.config/qtile/assets/reboot.png',
                margin = 7,
                mouse_callbacks = {'Button1': lazy.spawn("sudo reboot now")},
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["rosewater"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            widget.Image(
                filename = '~/.config/qtile/assets/shutdown.png',
                margin = 7,
                mouse_callbacks = {'Button1': lazy.spawn("sudo shutdown now")},
                decorations = [
                    RectDecoration(
                        colour = colors_catppuccin["rosewater"],
                        radius = 2,
                        filled = True,
                        group = True,
                        padding = 4,
                    )
                ],
            ),
            ],
            35, # WIDTH
            margin = 4,
        ),
    ),
    #Screen(
    #    top=bar.Bar([
    #        widget.CurrentLayoutIcon(
    #            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
    #            foreground=colors[0],
    #            background=colors[0],
    #            padding=0,
    #            scale=0.6,
    #        ),
    #        widget.GroupBox(
    #            font="Ubuntu Bold",
    #            fontsize=12,
    #            margin_y=2,
    #            margin_x=0,
    #            padding_y=5,
    #            padding_x=3,
    #            borderwidth=3,
    #            active=colors[2],
    #            inactive=colors[1],
    #            rounded=False,
    #            # highlight_color=self.colors[9],
    #            # highlight_method="line",
    #            highlight_method='block',
    #            urgent_alert_method='block',
    #            # urgent_border=self.colors[9],
    #            this_current_screen_border=colors[9],
    #            this_screen_border=colors[4],
    #            other_current_screen_border=colors[0],
    #            other_screen_border=colors[0],
    #            foreground=colors[2],
    #            background=colors[0],
    #            disable_drag=True,
    #        ),
    #        widget.Sep(
    #            linewidth=0,
    #            padding=10,
    #            foreground=colors[2],
    #            background=colors[0],
    #        ),
    #        widget.TaskList(
    #            theme_path="/usr/share/icons/Papirus/index.theme",
    #            theme_mode="preferred",
    #            highlight_method = 'block',
    #            icon_size=14,
    #            max_title_width=100,
    #            rounded=False,
    #            margin=0,
    #            padding=3,
    #            fontsize=10,
    #            border=colors[9],
    #            foreground=colors[2],
    #            borderwidth = 0,
    #            background=colors[0],
    #            urgent_border=colors[2],
    #            txt_floating='🗗 ',
    #            txt_minimized='_ ',
    #        ),
    #    ], 20, opacity=1),
    #),
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
    border_focus = colors_catppuccin["red"],
    border_normal = colors_catppuccin["base"],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
