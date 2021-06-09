import os
import logging
import logging.handlers
import sys

def setup(debug: bool = False):
    """Initial setup of logging. This is global to entire module, only call once

    :param debug: Sets log level to debug, more verbose if True, defaults to False
    :type debug: bool, optional
    """
    fileBackupCount = 14
    print("logging")
    logDirPath = "logs"
    os.makedirs(logDirPath, exist_ok=True)
    debugLogFilePath = os.path.join(logDirPath, "debug.log")
    errorLogFilePath = os.path.join(logDirPath, "error.log")

    logFormat = logging.Formatter(
        "[%(asctime)s] %(levelname)s: {%(filename)s:%(lineno)d} : %(message)s"
    )

    # sets up a stream to stdout
    logStreamHandler = logging.StreamHandler(stream=sys.stdout)
    logStreamHandler.setFormatter(logFormat)
    if debug:
        logStreamHandler.setLevel(logging.DEBUG)
    else:
        logStreamHandler.setLevel(logging.INFO)

    # sets up a log to file, rotates at midnight utc
    debugLogFileHandler = logging.handlers.TimedRotatingFileHandler(
        filename=debugLogFilePath,
        when="midnight",
        utc=True,
        backupCount=fileBackupCount,
    )
    debugLogFileHandler.setFormatter(logFormat)
    debugLogFileHandler.setLevel(logging.DEBUG)

    # only logs error and greater, also rotates
    errorLogFileHandler = logging.handlers.TimedRotatingFileHandler(
        filename=errorLogFilePath,
        when="midnight",
        utc=True,
        backupCount=fileBackupCount,
    )
    errorLogFileHandler.setFormatter(logFormat)
    errorLogFileHandler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.DEBUG,  # minimum required for any logging
        handlers=[logStreamHandler, debugLogFileHandler, errorLogFileHandler],
    )

    logging.info("starting")
    logging.info(f"Logging DEBUG to {debugLogFilePath}, INFO to std.out. ")
    logging.debug(f"Debug logging")

