##
## Raspberry Pi Clock & Weather Display (rpi_clock)
##

import os, time, sys, subprocess, json

MYNAME = 'rpi_clock'
flag_debugging = True
SLEEP_TIME_SEC = 60
SLEEP_TIME_MSEC = SLEEP_TIME_SEC*1000 # milliseconds

# ----------------------------------------------------------
# Weather Underground parameters
URL_LEFT = 'http://api.wunderground.com/api/'
URL_RIGHT = '/conditions/q/TX/Richardson.json'
WU_API_KEY = 'YOUR API KEY GOES HERE'
FULL_URL = URL_LEFT + WU_API_KEY + URL_RIGHT
URL_REQUEST_TIMEOUT_SEC = 60
COUNT_START = 20 # Fetch weather every 20th main loop execution
count_down = 0 # Fetch weather data from URL_LEFT when =0
flag_url = False
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

# ----------------------------------------------------------
# Images in current directory
PHOTO_REBOOT = 'system_REBOOT.png'
PHOTO_SHUTDOWN = 'system_shutdown.png'

# ----------------------------------------------------------
# Time-stamp logger; API is like C-language printf
def logger(arg_format, *arg_list):
	now = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
	fmt = "{nstr} {fstr}".format(nstr=now, fstr=arg_format)
	print(fmt % arg_list)
	sys.stdout.flush()

# ----------------------------------------------------------
# Exit immediately if this is an SSH session
if 'SSH_CLIENT' in os.environ or 'SSH_TTY' in os.environ:
	logger("%s: Running in SSH session; exiting", MYNAME)
	exit(0)

# ----------------------------------------------------------
# Must be Python 3.x
if sys.version_info[0] < 3:
	logger("%s: *** Requires Python 3", MYNAME)
	exit(86)

# ----------------------------------------------------------
# Import Python 3 libraries
from tkinter import *
import urllib.request

#-------------------------------------------------------------------
# Talk to operator

def proc_reboot():
	if flag_debugging:
		logger("%s: DEBUG proc_reboot begin", MYNAME)
	args = ['sudo', 'shutdown', '-r', 'now']
	cp = subprocess.run(args, stdout=subprocess.PIPE)

def proc_shutdown():
	if flag_debugging:
		logger("%s: DEBUG proc_shutdown begin", MYNAME)
	args = ['sudo', 'shutdown', 'now']
	cp = subprocess.run(args, stdout=subprocess.PIPE)

def talk_to_operator(event):
	if flag_debugging:
		logger("%s: DEBUG talk_to_operator begin", MYNAME)
	tk_popup = Tk()
	tk_popup.title("Go back, Reboot, or Shutdown?")
	tk_popup.attributes("-fullscreen", False) 
	tk_popup.configure(background=BG_COLOR_POPUP)
	tk_popup.geometry(WINDOW_SIZE_POPUP)
	b_goback = Button(tk_popup, text="Go Back", command=tk_popup.destroy,
		 font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
	b_goback.focus_set()
	b_goback.pack(fill="both", expand=True)
	b_REBOOT = Button(tk_popup, text='Reboot', command=proc_reboot,
					font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
	b_shutdown = Button(tk_popup, text='Shutdown', command=proc_shutdown,
					font=(FONT_NAME, FONT_POPUP_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL)
	b_REBOOT.pack(fill="both", expand=True)
	b_shutdown.pack(fill="both", expand=True)
	if flag_debugging:
		logger("%s: DEBUG talk_to_operator going back to tk_popup.mainloop", MYNAME)
	tk_popup.mainloop()
	logger("%s: tk_popup left mainloop", MYNAME)

# ----------------------------------------------------------
# Initialize Tk
tk_root = Tk()
tk_root.attributes("-fullscreen", True) 
tk_root.configure(background=BG_COLOR_ROOT)
tk_root.geometry(WINDOW_SIZE_ROOT)
display_spacer1 = Label(tk_root, font=(FONT_NAME, SPACER_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL,bg=BG_COLOR_ROOT)
display_spacer1.pack()
display_spacer1.config(text=" ") 

# ----------------------------------------------------------
# Build display lines
display_date = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_date.pack()
 
display_time = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_time.pack()
 
display_cur_temp = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_cur_temp.pack()
 
display_cur_cond = Label(tk_root, font=(FONT_NAME, FONT_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_cur_cond.pack()
 
display_spacer2 = Label(tk_root, font=(FONT_NAME, SPACER_SIZE, FONT_STYLE), fg=FG_COLOR_NORMAL, bg=BG_COLOR_ROOT)
display_spacer2.pack()
display_spacer2.config(text=" ") 

# ----------------------------------------------------------
# Procedure: Get date, time, farenheit-temperature, and celsius-temperature
def get_display_data():
	global count_down, str_temp, str_condition, flag_url
	if flag_debugging:
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
			flag_url = True
			if flag_debugging:
				logger("%s: DEBUG weather access success", MYNAME)
		except:
			# Something went wrong.  Force a retry on next tk_root.mainloop cycle.
			if flag_debugging:
				logger("%s: DEBUG Oops, weather access failed", MYNAME)
			count_down = 0
			flag_url = False
	count_down = count_down - 1
	now = time.localtime()
	str_date = time.strftime(FORMAT_DATE, now)
	str_time = time.strftime(FORMAT_TIME, now)
	if flag_debugging:
		logger("%s: DEBUG Display date = %s, time = %s, temp = %s - %s", 
				MYNAME, str_date, str_time, str_temp, str_condition)
	return( str_date, str_time, str_temp, str_condition )

# ----------------------------------------------------------
# Procedure: Main Loop
def display_main_procedure():
	if flag_debugging:
		logger("%s: DEBUG display_main_procedure begin", MYNAME)
	( str_date, str_time, str_temp, str_condition ) = get_display_data()
	display_date.config(text=str_date)
	display_time.config(text=str_time)
	if flag_url:
		display_cur_temp.config(fg=FG_COLOR_NORMAL)
		display_cur_cond.config(fg=FG_COLOR_NORMAL)
	else:
		display_cur_temp.config(fg=FG_COLOR_ABNORMAL)
		display_cur_cond.config(fg=FG_COLOR_ABNORMAL)
	display_cur_temp.config(text="%s" % str_temp)
	display_cur_cond.config(text="%s" % str_condition)
	if flag_debugging:
		logger("%s: DEBUG display_main_procedure going back to sleep", MYNAME)
	tk_root.after(SLEEP_TIME_MSEC, display_main_procedure)

# ----------------------------------------------------------
# Enter Tk mainloop
tk_root.after(0, display_main_procedure)
tk_root.bind('<ButtonPress>', talk_to_operator)
tk_root.mainloop()

logger("%s: tk_root left mainloop", MYNAME)
