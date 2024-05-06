import logging
import sys


def get_logger(name, std_out=True):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    if std_out:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
    return log
