########################################### Set up the config ##############################################
import os
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from utils import battery_display

class Colors:
    BLACK: str = "000000"
    DARK: str = "1A1B26"
    WHITE: str = "ffffff"
    PRIMARY: str = "0074e4"
    SECONDARY: str = "3D59A1"

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
terminal = "alacritty"      # My terminal of choice
myBrowser = "firefox" # My browser of choice
palette = Colors()
home = os.path.expanduser('~')


########################################## Keybindings ###########################################################


keys = [
    # Move window focus
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.grow(),lazy.layout.increase_nmaster(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.grow(),lazy.layout.decrease_nmaster(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    #Suffle windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    #Change window size
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
   

    #WM related binding
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod],"f",lazy.spawn("rofi -show drun"), desc="Launch Rofi App Launcher"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "c", lazy.spawn("betterlockscreen -l"),desc="locks the damn screen"),
    Key([mod], "r", lazy.spawn("dmenu_run -l 10 -fn 'Fira Code Nerd Font-12' -p 'Run'"), desc="Launch Dmenu run prompt"),

    # Custom keybindings for screenshot, brightness and volume
    Key([mod], "s", lazy.spawn(str(home) + "/.local/bin/screenshot.sh all"),desc="Take a screenshot of entire screen"),
    Key([mod, "shift"], "s", lazy.spawn(str(home) + "/.local/bin/screenshot.sh window"),desc="Take a screenshot of active window"),
    Key([mod, "control"], "s", lazy.spawn(str(home) + "/.local/bin/screenshot.sh select"),desc="Take a screenshot of selected area"),
    Key([mod, "shift"], "v", lazy.spawn(str(home) + "/.local/bin/changevolume.sh down"),desc="Decrease volume"),
    Key([mod], "v", lazy.spawn(str(home) + "/.local/bin/changevolume.sh up"),desc="Increases volume"),
    Key([mod], "b", lazy.spawn(str(home) + "/.local/bin/changebrightness.sh up"),desc="Increases brightness"),
    Key([mod, "shift"], "b", lazy.spawn(str(home) + "/.local/bin/changebrightness.sh down"),desc="Decrease brightness"),
]


#############################################3 Screen Layouts #############################################


layout_theme = {
                "border_width": 2,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    #layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    #layout.Stack(num_stacks=2),
    #layout.RatioTile(**layout_theme),
    #layout.Floating(**layout_theme)
]



###################################### Workspaces #####################################################


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )



########################################## Bar and Widgets ####################################################

widget_defaults = dict(
    font='Fira Code Nerd Font',
    fontsize=15,
    padding=7,
)

extension_defaults = widget_defaults.copy()
separator = widget.TextBox(text=" ",padding=5)

screens = [
    Screen(
        top=bar.Bar(
            [
                #separator,
                widget.GroupBox(
                    fontsize=13,
                    padding_x=5,
                    borderwidth=0,
                    active=palette.WHITE,
                    inactive=palette.WHITE,
                    rounded=True,
                    highlight_method="block",
                    highlight_color=palette.DARK,
                    block_highlight_text_color=palette.WHITE,
                    this_current_screen_border=palette.SECONDARY,
                    foreground=palette.DARK,
                    background=palette.DARK,
                    hide_unused=True
                ),
                separator,
                #widget.Prompt(),
                #widget.WindowName(fontsize=15, format='{name}'),
                widget.Spacer(),
                widget.Systray(),
                separator,
                widget.Mpris2(name="spotify", stop_pause_text="???  {track}",playing_text="???  {track}",display_metadata=["xesam:title", "xesam:artist"], objname="org.mpris.MediaPlayer2.spotify"),
                separator,
                widget.TextBox(text="??? ",  padding=0, mouse_callbacks={"Button1":lazy.spawn(myBrowser + " -new-window github.com/A-J-Sarmah")}),
                separator,
                separator,
                widget.TextBox(text="??? ",  padding=0, mouse_callbacks={"Button1":lazy.spawn(str(home) + "/.local/bin/changevolume.sh mute"), "Button4":lazy.spawn(str(home) + "/.local/bin/changevolume.sh up"), "Button5":lazy.spawn(str(home) + "/.local/bin/changevolume.sh down")}),
                separator,
                separator,
                widget.Battery(format=battery_display(),padding=0,update_interval=1),
                separator,
                separator,
                widget.Wlan(format='???  {essid}',disconnected_message="???  Disconnected",padding=0), # The Wlan widget uses a library called iwlib as dependency so to use it we must install 'iwlib' via the pip package manager.
                separator,
                separator,
                widget.Clock(format='???  %I:%M %p', padding=0),
                separator,
                separator,
                widget.Clock(format = '???  %a %d/%m/%y',padding=0),
                separator,
            ],
            20,
            margin=[10, 10, 0, 10],
            background=palette.DARK,
            opacity=1,
        ),
    ),
]


################################################################# Autostart apps ###################################################################


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~')
    subprocess.run([home + '/.config/qtile/autostart.sh'])

