import logging
import sys
from pathlib import Path
from typing import Union


def setup_logger(log_file_path: Union[Path, str]) -> logging.Logger:
    logger = logging.getLogger("lgr")
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    # create file handler and set level to debug
    fh = logging.FileHandler(log_file_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-8s - %(filename)-20s - %(funcName)-20s - %(message)-s"
    )

    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


logger = setup_logger("logs.log")
