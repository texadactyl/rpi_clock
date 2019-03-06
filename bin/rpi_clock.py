"""
Raspberry Pi Clock & Weather Display (rpi_clock)
"""

import configparser
import os
import subprocess
import sys
import time
from tkinter import Button, Label, Tk

import requests
from rpi_clock_parameters import RpiClockParameters

parms = RpiClockParameters()
count_down = 0
flag_display_normal = False
str_condition = "No condition yet"
str_temp = "No temperature yet"

# ----------------------------------------------------------
# Miscellaneous parameters
URL_LEFT = "https://api.openweathermap.org/data/2.5/weather?APPID="
URL_MIDDLE_1 = "&"
URL_MIDDLE_2 = "&units="

# ----------------------------------------------------------
# Video display parameters
WINDOW_SIZE_ROOT = "480x320"
WINDOW_SIZE_POPUP = "320x200"
FONT_NAME = "helvetica"
FONT_SIZE = 40
FONT_POPUP_SIZE = 24
FONT_STYLE = "normal"
SPACER_SIZE = 20
BUTTON_WIDTH = 6
BUTTON_HEIGHT = 2
FG_COLOR_NORMAL = "green"
FG_COLOR_ABNORMAL = "red"
BG_COLOR_ROOT = "black"
BG_COLOR_POPUP = BG_COLOR_ROOT

def oops(arg_string):
    """
    Log an error-string and raise a UserWarning.
    This will cause an orderly exit to the O.S.
    """
    parms.logger = None
    parms.logging_init("OOPS", True)
    parms.logger.critical(arg_string)
    sys.exit(86)

def get_config_string(arg_config, arg_key):
    """
    get one STRING configuration parameter by key
    """
    parm_value = "?"
    try:
        parm_value = arg_config.get(parms.MYNAME, arg_key)
    except Exception as err:
        oops("get_config_string: Trouble with config file key {}, reason: {}"\
             .format(arg_key, repr(err)))
    parms.logger.info("get_config_string: {} = {}".format(arg_key, parm_value))
    return parm_value

def get_config_int(arg_config, arg_key):
    """
    get one INTEGER configuration parameter by key
    """
    parm_value = -1
    try:
        parm_value = arg_config.getint(parms.MYNAME, arg_key)
    except Exception as err:
        oops("get_config_int: Trouble with config file key {}, reason: {}"\
             .format(arg_key, repr(err)))
    parms.logger.info("get_config_int: {} = {}".format(arg_key, parm_value))
    return parm_value

def get_config_boolean(arg_config, arg_key):
    """
    get one BOOLEAN configuration parameter by key
    """
    parm_value = False
    try:
        parm_value = arg_config.getboolean(parms.MYNAME, arg_key)
    except Exception as err:
        oops("get_config_boolean: Trouble with config file key {}, reason: {}"\
             .format(arg_key, repr(err)))
    parms.logger.info("get_config_boolean: {} = {}".format(arg_key, parm_value))
    return parm_value

def get_config_all(arg_config_path):
    """
    get all of the configuration parameters and store them in the parms object
    """
    try:
        config = configparser.ConfigParser()
        config.read(arg_config_path)
        parms.logger.info("get_config_all: config file {} was loaded into memory"\
                          .format(arg_config_path))
        parms.FLAG_TRACING = get_config_boolean(config, "FLAG_TRACING")
        parms.FORMAT_DATE = get_config_string(config, "FORMAT_DATE")
        parms.FORMAT_TIME = get_config_string(config, "FORMAT_TIME")
        parms.LOCATION = get_config_string(config, "LOCATION")
        parms.TEMP_UNITS = get_config_string(config, "TEMP_UNITS")
        parms.FLAG_WINDOWED = get_config_boolean(config, "FLAG_WINDOWED")
        parms.OWM_API_KEY = get_config_string(config, "OWM_API_KEY")
        parms.COUNT_START = get_config_int(config, "COUNT_START")
        if parms.COUNT_START < 10:
            oops("COUNT_START invalid (< 10)")
        parms.REQUEST_TIMEOUT_SEC = get_config_int(config, "REQUEST_TIMEOUT_SEC")
        if parms.REQUEST_TIMEOUT_SEC < 10:
            oops("REQUEST_TIMEOUT_SEC invalid (< 10)")
        parms.SLEEP_TIME_MSEC = get_config_int(config, "SLEEP_TIME_MSEC")
        if parms.SLEEP_TIME_MSEC < 10:
            oops("SLEEP_TIME_MSEC invalid (< 10)")
        del config
    except Exception as err:
        oops("get_config: Trouble with config file {}, reason: {}"\
             .format(arg_config_path, repr(err)))
    parms.logger.info("get_config_all: done")

def initialize_the_process():
    """
    Initialize the rpi_clock process.
    1. Basic diagnosis
    2. Call get_config_all()
    """
    ### Must be a main program
    if __name__ != "__main__":
        oops("initialization: Must be a main program")

    ### Must be Python 3.x
    if sys.version_info[0] < 3:
        oops("initialization: Requires Python 3")

    ### Exit immediately if this is an SSH session
    if "SSH_CLIENT" in os.environ or "SSH_TTY" in os.environ:
        oops("initialization: Must not run in SSH session")

    ## Exit immediately if no configuration file was specified
    nargs = len(sys.argv)
    if nargs < 2: # then there is a command-line argument
        oops("initialization: Configuration file path is required")

    ### Process configuration file
    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        oops("initialization: Cannot access config file specified as {}".format(config_path))
    get_config_all(config_path)

    ### Done, return logger handle to caller
    parms.logger.info("intialization: done")

def proc_quit():
    """
    Operator selected Quit
    """
    if parms.FLAG_TRACING:
        parms.logger.debug("proc_quit: begin")
    sys.exit(0)

def proc_reboot():
    """
    Operator selected Reboot
    """
    if parms.FLAG_TRACING:
        parms.logger.debug("proc_reboot: begin")
    args = ["sudo", "shutdown", "-r", "now"]
    subprocess.run(args, stdout=subprocess.PIPE)

def proc_shutdown():
    """
    Operator selected Shutdown
    """
    if parms.FLAG_TRACING:
        parms.logger.debug("proc_shutdown: begin")
    args = ["sudo", "shutdown", "now"]
    subprocess.run(args, stdout=subprocess.PIPE)

def talk_to_operator(event):
    """
    Talk to the operator with a form (Go back, Reboot, or Shutdown?)
    """

    if parms.FLAG_TRACING:
        parms.logger.debug("talk_to_operator: begin")
    tk_popup = Tk()
    tk_popup.title("Go back, Quit, Reboot, or Shutdown?")
    tk_popup.attributes("-fullscreen", False)
    tk_popup.configure(background=BG_COLOR_POPUP)
    tk_popup.geometry(WINDOW_SIZE_POPUP)
    b_goback = Button(tk_popup, text="Go Back", command=tk_popup.destroy,
                      font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_goback.focus_set()
    b_goback.pack(fill="both", expand=True)
    b_quit = Button(tk_popup, text="Quit", command=proc_quit,
                    font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_quit.pack(fill="both", expand=True)
    b_reboot = Button(tk_popup, text="Reboot", command=proc_reboot,
                      font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_reboot.pack(fill="both", expand=True)
    b_shutdown = Button(tk_popup, text="Shutdown", command=proc_shutdown,
                        font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
    b_shutdown.pack(fill="both", expand=True)
    if parms.FLAG_TRACING:
        parms.logger.debug("talk_to_operator: before tk_popup.mainloop()")
    tk_popup.mainloop()
    if parms.FLAG_TRACING:
        parms.logger.debug("talk_to_operator: after tk_popup.mainloop()")

def get_refreshed_data(arg_url):
    '''
    Get JSON Data.  Possible outcomes:
    * Success --> True, temperature, condition
    * Network error --> False, "Network Failed", " "
    * JSON parse error --> False, "JSON Parse Failed", " "
    * Missing JSON element --> False, code value, descriptive message
    * Unrecognizable message --> False, "Response Rubbish", "See Log"
    '''
    response = ""
    try:
        if parms.FLAG_TRACING:
            parms.logger.debug("get_refreshed_data: Sending: " + arg_url)
        response = requests.get(arg_url, timeout=parms.REQUEST_TIMEOUT_SEC)
        if parms.FLAG_TRACING:
            parms.logger.debug("get_refreshed_data: Network response: {}".format(response))
    except:
        parms.logger.error("Oh-oh, requests.get() failed: {}, URL: {}".format(sys.exc_info()[0], arg_url))
        if response in (None, ""):
            response = "*NIL*"
        return False, "Network Failed", response

    # Successful retrieval.  Parse JSON data.
    if parms.FLAG_TRACING:
        parms.logger.debug("get_refreshed_data: requests.get() ok: {}".format(response))
    try:
        parsed_json = response.json()
        if parms.FLAG_TRACING:
            parms.logger.debug("get_refreshed_data: Received parsed JSON: {}".format(parsed_json))
    except:
        parms.logger.error("get_refreshed_data: Oh-oh, the last response.json() failed")
        return False, "JSON Parse Failed", " "

    # Fetch data we are interested in.
    try:
        main = parsed_json["main"]
        temp = main["temp"]
        weather = parsed_json["weather"]
        condition = weather[0]["description"]

    except:
        # Missing expected JSON elements
        try:
            str_code = parsed_json["cod"]
            str_msg = parsed_json["message"]
            # Got a standard error response message
            parms.logger.error("Oh-oh, in the last response, str_code={}, str_msg={}".format(str_code, str_msg))
            return False, str_code, str_msg
        except:
            parms.logger.error("Oh-oh, in the last response, 'cod' and/or 'message' is missing")
            return False, "Response Rubbish", "See Log"

    # Got the data that was expected
    if parms.FLAG_TRACING:
        parms.logger.debug("get_refreshed_data: weather access success")
        parms.logger.debug("get_refreshed_data: Data for display: temp={}, condition={}".format(temp, condition))
    return True, temp, condition

def get_display_data():
    """
    Get date, time, farenheit-temperature, celsius-temperature, and general condition
    if it is time to do so - governed by count_down.
    """
    global count_down, flag_display_normal, str_condition, str_temp
    FULL_URL = URL_LEFT + parms.OWM_API_KEY + URL_MIDDLE_1 + parms.LOCATION + URL_MIDDLE_2 + parms.TEMP_UNITS
    if parms.FLAG_TRACING:
        parms.logger.debug("get_display_data: begin, URL={}".format(FULL_URL))

    # If count_down is < 1, then it is time fetch new network data
    if count_down < 1:
        if parms.FLAG_TRACING:
            parms.logger.debug("get_display_data: count_down={}, time to refresh network data".format(count_down))
        # Reset count_down to start value
        count_down = parms.COUNT_START
        # Try to fetch current weather: temperature & general condition
        flag_display_normal, str_temp, str_condition = get_refreshed_data(FULL_URL)
        if not flag_display_normal:
            count_down = 0 # force retry

    # Successful retrieval and parse OR not, process what we have (even if stale)
    count_down = count_down - 1
    now = time.localtime()
    str_date = time.strftime(parms.FORMAT_DATE, now)
    str_time = time.strftime(parms.FORMAT_TIME, now)
    del now
    if parms.FLAG_TRACING:
        parms.logger.debug("Display date = %s, time = %s, temp = %s, cond = %s",
                           str_date, str_time, str_temp, str_condition)

    # Return strings for Tk display
    return(str_date, str_time, str_temp, str_condition)

def display_main_procedure():
    """
    Main display Loop

    Update display as needed.
    Then, reschedule myself SLEEP_TIME_MSEC milliseconds into the future.
    """
    global flag_display_normal, str_condition, str_temp
    if parms.FLAG_TRACING:
        parms.logger.debug("display_main_procedure begin")
    (str_date, str_time, str_temp, str_condition) = get_display_data()
    display_date.config(text=str_date)
    display_time.config(text=str_time)
    if flag_display_normal:
        display_cur_temp.config(fg=FG_COLOR_NORMAL)
        display_cur_cond.config(fg=FG_COLOR_NORMAL)
    else:
        display_cur_temp.config(fg=FG_COLOR_ABNORMAL)
        display_cur_cond.config(fg=FG_COLOR_ABNORMAL)
    display_cur_temp.config(text="%s" % str_temp)
    display_cur_cond.config(text="%s" % str_condition)
    if parms.FLAG_TRACING:
        parms.logger.debug("display_main_procedure going back to sleep")
    tk_root.after(parms.SLEEP_TIME_MSEC, display_main_procedure)

# ----------------------------------------------------------
### Call process initialization (initialize_process).
initialize_the_process()

# ----------------------------------------------------------
### Establish Tk root, configuration, geometry, and labels
tk_root = Tk()
tk_root.attributes("-fullscreen", not parms.FLAG_WINDOWED)
tk_root.configure(background=BG_COLOR_ROOT)
tk_root.geometry(WINDOW_SIZE_ROOT)
display_spacer1 = Label(tk_root, font=(FONT_NAME, SPACER_SIZE, FONT_STYLE), \
                        fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_spacer1.pack()
display_spacer1.config(text=" ")
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

# ----------------------------------------------------------
### Set up Tk for mainloop

tk_root.after(0, display_main_procedure)
tk_root.bind("<ButtonPress>", talk_to_operator)

# ----------------------------------------------------------
### Enter Tk mainloop
parms.logger.info("Will now enter tk_root mainloop")
tk_root.mainloop()

# ----------------------------------------------------------
### Left Tk mainloop
parms.logger.info("Just now exited tk_root mainloop")
