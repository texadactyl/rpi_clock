"""
rpi_clock Parameter Class
"""
import logging

MYNAME = "rpi_clock"

class RpiClockParameters:
    """
    Configuration Parameters and dynamic globals for rpi_clock process.
    """
    FORMAT_DATE = "" # Locality date format
    FORMAT_TIME = "" # Hours:Minutes + AM/PM for the USA
    LOCATION_JSON = "" # /STATE/CITY.json
    FLAG_WINDOWED = True # False ==> full screen (normal for TFT)
    WU_API_KEY = "" # Weatherunderground API key

    # Not recommended to change the following parameters
    COUNT_START = -1 # Fetch weather every 20th main loop execution
    FLAG_TRACING = False # verbose tracing
    REQUEST_TIMEOUT_SEC = -1 # Timeout if URL server does not respond in time
    SLEEP_TIME_MSEC = -1 # milliseconds, time between URL contact attempts

    # Name of project
    MYNAME = "rpi_clock"

    def logging_init(self, tag="", use_ts=False):
        """
        Initialize the logging object and return it to caller.
        """
        # Create logging object, logger
        self.logger = logging.getLogger(tag)
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level to 0
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)

        # Create formatter
        if use_ts:
            piece_ts = "[%(asctime)s]::"
        else:
            piece_ts = ""
        if tag != "":
            piece_name = "%(name)s::"
        else:
            piece_name = ""
        formatter = logging.Formatter(piece_ts + piece_name + "%(levelname)s::%(message)s")

         # Add formatter to console
        console.setFormatter(formatter)

        # Add console to logging object
        self.logger.addHandler(console)

    def __init__(self):
        self.logging_init(use_ts=True)
