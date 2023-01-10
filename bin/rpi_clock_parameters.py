"""
rpi_clock Parameter Class
"""
import logging
import version

class RpiClockParameters:
    """
    Configuration Parameters and dynamic globals for rpi_clock process.
    """
    FORMAT_DATE = "" # Locality date format
    FORMAT_TIME = "" # Hours:Minutes + AM/PM for the USA
    LOCATION = "" # E.g. zip=75248,us
    TEMP_UNITS = "" # metric, imperial, or kelvin
    TEMP_SUFFIX = "" # C, F, or K
    FLAG_WINDOWED = False # False ==> full screen (normal for TFT)
    OWM_API_KEY = "" # OpenWeatherMap API key
    COUNT_START = -1 # Fetch weather after this many main loop executions
    FLAG_TRACING = False # Verbose tracing
    REQUEST_TIMEOUT_SEC = -1 # Timeout in seconds if URL server does not respond in time
    SLEEP_TIME_MSEC = -1 # The amount of time between URL contact attempts in milliseconds

    # Name of project
    MYNAME = "rpi_clock"
    VERSION = version.VERSION

    def  __init__(self):
        """
        Initialize the logging object and return it to caller.
        """
        # Create logging object, logger
        logging.basicConfig(encoding='utf-8',
                            format="%(asctime)s %(message)s",
                            level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.info("===== rpi_clock begins =====")
        msg = "Version " + version.VERSION
        self.logger.info(msg)
