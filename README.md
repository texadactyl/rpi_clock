See HISTORY.txt file for update history.

This git project constitutes a Raspberry Pi Clock & Weather display (rpi_clock), based on https://github.com/goodtft/LCD-show and the Quimat 3.5" TFT Touch Screen with a 320x480 resolution and it uses the Open Weather Map API (https://openweathermap.org/api).

************* 
2023-01-10: 
* My Quimat TFT died.  The installation of that product was less than satisfactory so I will not repeat that headache.
* Having a devil of a time finding a replacement.  My preferred replacement product is either of the following:
-- https://www.adafruit.com/product/2441
-- https://www.adafruit.com/product/2097 
************* 

I have used a Raspberry Pi 2 and 3 Model B.  It would not be terribly difficult to modify the rpi_clock.py Python 3 script to employ:

* Another touch-screen display which interfaces with the Raspberry Pi 2 or 3.
* Another Linux distribution or any O.S. which supports Python 3, JSON, and Tk.
* Run on MacOS or Windows.

In addition to the TFT environment, I have run this project with Xubuntu on Raspberry Pi 3 model B with a standard display connected with HDMI cable.  See the configuration file for controlling whether or not rpi_clock uses the full screen or a windowed display.

Package Dependencies
--------------------

- Requests (available at pypi)
- tkinter (included with Python 3)

Licensing
---------

This is *NOT* commercial software; instead, usage is covered by the GNU General Public License version 3 (2007).  In a nutshell, please feel free to use the project and share it as you will but please don't sell it.  Thanks!

See the LICENSE file for the GNU licensing information.

Technical Contents
------------------

Subfolders:

* bin - *.py (Python 3 source code) and a sample configuration file
* docs - project installation documentation

Getting Started
---------------

The starting point with this project is the docs/preparation_notes.txt file.  Just follow the instructions of this note. If you do this project on some other system base (E.g. MacOS or Windows), please let me know how the instructions changed and how is your project doing. 

Afterthoughts
-------------

Admittedly, there seems to be other 3.5" TFT display products which claim to NOT require special drivers as of the latest Raspbian during 2017 (more desirable IMO).  In fact, the Quimat TFT might work this way too.  I just got caught in the middle!  Some time in the future, I might try it without the Quimat-supplied driver software.  If that effort is successful, I will update this project.

Will this work on a Pi Zero?  Probably.  Older Pi A or B?  Probably.  Please let me know if you do this.  Thanks.

Feel free to raise an issue for inquiries, especially if you find any bugs.  I'll respond as soon as I can.

Richard Elkins

Dallas, Texas, USA, 3rd Rock, Sol, ...
