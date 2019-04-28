import logging, datetime, os
sHandler = 0b01
fHandler = 0b10

today = datetime.date.today().isoformat()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
default_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
log_dir = os.path.join(default_dir, today)

def mylog(msg = "", level = "info", file = "log", handler = sHandler):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file = os.path.join(log_dir, file)
    check = 0b11
    logger = logging.getLogger("Log")
    if  sHandler & check == sHandler:
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)
    if  fHandler & check == fHandler:
        file_handler = logging.FileHandler(filename = file)
        logger.addHandler(file_handler)
    LEVELS = {
        "debug": (logging.DEBUG, logger.debug),
        "info": (logging.INFO, logger.info),
        "warning": (logging.WARNING, logger.warning),
        "error": (logging.ERROR, logger.error),
        "critical": (logging.CRITICAL, logger.critical)
    }  
    logger.setLevel(LEVELS[level][0])
    msg = msg + ' | ' + now
    LEVELS[level][1](msg)
    if sHandler & check == sHandler:
        logger.removeHandler(stream_handler)
    if fHandler & check == fHandler:
        logger.removeHandler(file_handler)