import logging

logger = logging.getLogger(__name__)

# http://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
# Very minimal direct copying so should be no license issues.

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored output.
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"

COLOR_MAP = {
    'CRITICAL': RED,
    'ERROR': RED,
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': WHITE,
}


class ColoredFormatter(logging.Formatter):

    def __init__(self, msg, monochrome):
        super(ColoredFormatter, self).__init__(msg)
        self.monochrome = monochrome

    def format(self, record):
        uncolored = super(ColoredFormatter, self).format(record)
        levelname = record.levelname
        if not self.monochrome and (levelname in COLOR_MAP):
            color_seq = COLOR_SEQ % (30 + COLOR_MAP[levelname])
            formatted = color_seq + uncolored + RESET_SEQ
        else:
            formatted = uncolored
        return formatted


def setup_logging(level, monchrome=False):
    '''
    Utility function for setting up logging.
    '''
    # Logging to file
    logging.basicConfig(filename='fusesoc.log',
                        filemode='w', level=logging.DEBUG)
    # Pretty color terminal logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = ColoredFormatter(
        "%(levelname)s: %(message)s", monochrome=monchrome)
    ch.setFormatter(formatter)
    # Which packages do we want to log from.
    packages = ('__main__', 'fondue',)
    for package in packages:
        logger = logging.getLogger(package)
        logger.addHandler(ch)
        logger.setLevel(level)
    # Warning only packages
    warning_only_packages = []
    for package in warning_only_packages:
        logger = logging.getLogger(package)
        logger.addHandler(ch)
        logger.setLevel(logging.WARNING)
    logger.debug('Setup logging at level {}.'.format(level))


def init_logging(verbose, monochrome):
    level = logging.DEBUG if verbose else logging.INFO

    setup_logging(level=level, monchrome=monochrome)

    if verbose:
        logger.debug("Verbose output")
    else:
        logger.debug("Concise output")

    if monochrome:
        logger.debug("Monochrome output")
    else:
        logger.debug("Colorful output")
