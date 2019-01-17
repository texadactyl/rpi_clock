OVERVIEW - updated 2019-01-17 (v3) - See VERSION file for update history.

This git project constitutes a Raspberry Pi Clock & Weather display (rpi_clock), based on https://github.com/goodtft/LCD-show and the Quimat 3.5" TFT Touch Screen with a 320x480 resolution.

I have used a Raspberry Pi 2 and 3 Model B.  It would not be terribly difficult to modify the rpi_clock.py Python 3 script to employ:

* Another touch-screen display which interfaces with the Raspberry Pi 2 or 3.
* Another Linux distribution or any O.S. which supports Python 3, JSON, and Tk.
* Run on MacOS or Windows.

In addition to the TFT environment, I have run this project with Xubuntu on Raspberry Pi 3 model B with a standard display connected with HDMI cable.  It currently hogs the entire screen but it works.  To exit, you have to either (1) Alt-Tab to another open window or (2) ssh from another computer and kill the full-screen rpi_clock task.  Not elegant!  It would not be difficult to modify the Python 3 program to use only a window instead of the whole screen.

LICENSING

This is *NOT* commercial software; instead, usage is covered by the GNU General Public License version 3 (2007).  In a nutshell, please feel free to use the project and share it as you will but please don't sell it.  Thanks!

See the LICENSE file for the GNU licensing information.

TECHNICAL CONTENTS

Subfolders:

* bin - rpi_clock.py (Python 3 source code)
* docs - project documentation (admittedly, skimpy at the moment)

GETTING STARTED

The starting point with this project is the docs/preparation_notes.txt file.  Just follow the instructions of this note. If you do this project on some other system base (E.g. MacOS or Windows), please let me know how the instructions changed and how is your project doing. 

AFTERTHOUGHTS

Admittedly, there seems to be other 3.5" TFT display products which claim to NOT require special drivers as of the latest Raspbian during 2017 (more desirable IMO).  In fact, the Quimat TFT might work this way too.  I just got caught in the middle!  Some time in the future, I might try it without the Quimat-supplied driver software.  If that effort is successful, I will update this project.

Will this work on a Pi Zero?  Probably.  Older Pi A or B?  Probably.  Please let me know if you do this.  Thanks.

Feel free to contact richard.elkins@gmail.com for inquiries and issues, especially if you find any bugs.  I'll respond as soon as I can.

Richard Elkins

Dallas, Texas, USA, 3rd Rock, Sol, ...
