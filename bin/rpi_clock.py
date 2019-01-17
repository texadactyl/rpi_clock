"""
    Raspberry Pi Clock & Weather Display (rpi_clock)
"""

import os, time, sys, subprocess, json

MYNAME = 'rpi_clock'

### Must be a main program
if __name__ != "__main__":
    print("{}: *** Must be a main program ***".format(MYNAME))
    sys.exit(86)

### Must be Python 3.x
if sys.version_info[0] < 3:
    print("{}: *** Requires Python 3 ***".format(MYNAME))
    exit(86)

### Exit immediately if this is an SSH session
if 'SSH_CLIENT' in os.environ or 'SSH_TTY' in os.environ:
    print("{}: *** Must not run in SSH session ***".format(MYNAME))
    exit(86)

# ----------------------------------------------------------
# Import Python 3 libraries
from tkinter import Tk, Button, Label
import urllib.request

TRACING = False
SLEEP_TIME_SEC = 60
SLEEP_TIME_MSEC = SLEEP_TIME_SEC*1000 # milliseconds

# ----------------------------------------------------------
# Weather Underground parameters
URL_LEFT = 'http://api.wunderground.com/api/'
URL_RIGHT = '/conditions/q/TX/Richardson.json' # YOUR LOCATION json GOES HERE
WU_API_KEY = 'YOUR API KEY GOES HERE'
FULL_URL = URL_LEFT + WU_API_KEY + URL_RIGHT
URL_REQUEST_TIMEOUT_SEC = 60
COUNT_START = 20 # Fetch weather every 20th main loop execution
count_down = 0 # Fetch weather data from FULL_URL when = 0
flag_display_green = False
str_temp = 'No temperature yet'
str_condition = 'No condition yet'

# ----------------------------------------------------------
# Video display parameters
WINDOW_SIZE_ROOT = "480x320"
WINDOW_SIZE_POPUP = "320x200"
FONT_NAME = 'helvetica'
FONT_SIZE = 40
FONT_POPUP_SIZE = 24
FONT_STYLE = 'normal'
SPACER_SIZE = 20
BUTTON_WIDTH = 6
BUTTON_HEIGHT = 2
FG_COLOR_NORMAL = 'green'
FG_COLOR_ABNORMAL = 'red'
BG_COLOR_ROOT = 'black'
BG_COLOR_POPUP = BG_COLOR_ROOT
FORMAT_DATE = "%b %d, %Y" # USA date format
FORMAT_TIME = "%I:%M %p %Z" # Hours:Minutes + AM/PM for the USA

def logger(arg_format, *arg_list):
    """
    Time-stamp logger; API is like C-language printf
    """
    now = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    fmt = "{nstr} {fstr}".format(nstr=now, fstr=arg_format)
    print(fmt % arg_list)
    sys.stdout.flush()

def proc_quit():
    """
    Operator selected Quit
    """
    if TRACING:
        logger("%s: DEBUG proc_quit begin", MYNAME)
    sys.exit(0)

def proc_reboot():
    """
    Operator selected Reboot
    """
    if TRACING:
        logger("%s: DEBUG proc_reboot begin", MYNAME)
    args = ['sudo', 'shutdown', '-r', 'now']
    subprocess.run(args, stdout=subprocess.PIPE)

def proc_shutdown():
    """
    Operator selected Shutdown
    """
    if TRACING:
        logger("%s: DEBUG proc_shutdown begin", MYNAME)
    args = ['sudo', 'shutdown', 'now']
    subprocess.run(args, stdout=subprocess.PIPE)

def talk_to_operator(event):
    """
    Talk to the operator with a form (Go back, Reboot, or Shutdown?)
    """
    if TRACING:
        logger("%s: DEBUG talk_to_operator begin", MYNAME)
    tk_popup = Tk()
    tk_popup.title("Go back, Quit, Reboot, or Shutdown?")
    tk_popup.attributes("-fullscreen", False)
    tk_popup.configure(background=BG_COLOR_POPUP)
    tk_popup.geometry(WINDOW_SIZE_POPUP)
    b_goback = Button(tk_popup, text="Go Back", command=tk_popup.destroy,
                      font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_goback.focus_set()
    b_goback.pack(fill="both", expand=True)
    b_quit = Button(tk_popup, text='Quit', command=proc_quit,
                    font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_quit.pack(fill="both", expand=True)
    b_reboot = Button(tk_popup, text='Reboot', command=proc_reboot,
                      font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_reboot.pack(fill="both", expand=True)
    b_shutdown = Button(tk_popup, text='Shutdown', command=proc_shutdown,
                        font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_shutdown.pack(fill="both", expand=True)
    if TRACING:
        logger("%s: DEBUG talk_to_operator going back to tk_popup.mainloop", MYNAME)
    tk_popup.mainloop()
    logger("%s: tk_popup left mainloop", MYNAME)

def get_display_data():
    """
    Get date, time, farenheit-temperature, celsius-temperature, and general condition
    """
    global count_down, str_temp, str_condition, flag_display_green
    if TRACING:
        logger("%s: DEBUG get_display_data begin", MYNAME)
    if count_down < 1:
        # Time to go geat new weather data
        count_down = COUNT_START
        try:
            url_handle = urllib.request.urlopen(FULL_URL, None, URL_REQUEST_TIMEOUT_SEC)
            data = url_handle.read()
            encoding = url_handle.info().get_content_charset('utf-8')
            parsed_json = json.loads(data.decode(encoding))
            str_temp = parsed_json['current_observation']['temperature_string']
            str_condition = parsed_json['current_observation']['icon']
            url_handle.close()
            flag_display_green = True
            if TRACING:
                logger("%s: DEBUG weather access success", MYNAME)
        except Exception:
            # Something went wrong.  Force a retry on next tk_root.mainloop cycle.
            if TRACING:
                logger("%s: DEBUG Oops, weather access failed", MYNAME)
            count_down = 0
            flag_display_green = False
    count_down = count_down - 1
    now = time.localtime()
    str_date = time.strftime(FORMAT_DATE, now)
    str_time = time.strftime(FORMAT_TIME, now)
    if TRACING:
        logger("%s: DEBUG Display date = %s, time = %s, temp = %s - %s",
               MYNAME, str_date, str_time, str_temp, str_condition)
    return(str_date, str_time, str_temp, str_condition)

def display_main_procedure():
    """
    Main display Loop

    Update display as needed.
    Then, reschedule myself SLEEP_TIME_MSEC milliseconds in the future.
    """
    global count_down, str_temp, str_condition, flag_display_green
    if TRACING:
        logger("%s: DEBUG display_main_procedure begin", MYNAME)
    (str_date, str_time, str_temp, str_condition) = get_display_data()
    display_date.config(text=str_date)
    display_time.config(text=str_time)
    if flag_display_green:
        display_cur_temp.config(fg=FG_COLOR_NORMAL)
        display_cur_cond.config(fg=FG_COLOR_NORMAL)
    else:
        display_cur_temp.config(fg=FG_COLOR_ABNORMAL)
        display_cur_cond.config(fg=FG_COLOR_ABNORMAL)
    display_cur_temp.config(text="%s" % str_temp)
    display_cur_cond.config(text="%s" % str_condition)
    if TRACING:
        logger("%s: DEBUG display_main_procedure going back to sleep", MYNAME)
    tk_root.after(SLEEP_TIME_MSEC, display_main_procedure)

"""
Initialize Tk and begin main display loop
"""

flag_full_screen = True # Assume full-screen execution
nargs = len(sys.argv)
if nargs != 1: # then there is a command-line argument
    flag_window = sys.argv[1]
    if flag_window == "w": # windowed execution requested?
        flag_full_screen = False # Yes

tk_root = Tk()
tk_root.attributes("-fullscreen", flag_full_screen)
tk_root.configure(background=BG_COLOR_ROOT)
tk_root.geometry(WINDOW_SIZE_ROOT)
display_spacer1 = Label(tk_root, font=(FONT_NAME, SPACER_SIZE, FONT_STYLE), \
                        fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_spacer1.pack()
display_spacer1.config(text=" ")

# ----------------------------------------------------------
# Build display lines
display_date = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), \
                     fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_date.pack()

display_time = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), \
                     fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_time.pack()

display_cur_temp = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), \
                         fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_cur_temp.pack()

display_cur_cond = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), \
                         fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_cur_cond.pack()

display_spacer2 = Label(tk_root, font=(FONT_NAME, SPACER_SIZE, FONT_STYLE), \
                        fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_spacer2.pack()
display_spacer2.config(text=" ")

tk_root.after(0, display_main_procedure)
tk_root.bind('<ButtonPress>', talk_to_operator)

# ----------------------------------------------------------
# Enter Tk mainloop
tk_root.mainloop()

logger("%s: tk_root left mainloop", MYNAME)
