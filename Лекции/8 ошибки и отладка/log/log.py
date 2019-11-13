# логгирование в файл
import logging
import sys
from datetime import datetime

def create_logger(logger_name, file_name=None, level="WARNING"):

    logger_levels = {
                'CRITICAL': logging.CRITICAL,  # 50
                'ERROR': logging.ERROR,  # 40
                'WARNING': logging.WARNING,  # 30
                'INFO': logging.INFO,  # 20
                'DEBUG': logging.DEBUG,  # 10
            }

    level = logger_levels.get(level, logging.WARNING)

    file_name = file_name if file_name is not None else logger_name + '_' + str(datetime.date(datetime.now()).today()) + '.log'

    formatter = logging.Formatter('[%(asctime)s] - %(name)-20s - %(module)-20s - %(threadName)-20s - [%(levelname)-8s] - %(message)s')

    created_logger = logging.getLogger(logger_name)
    created_logger.setLevel(level)

    # File handler
    fh = logging.FileHandler(file_name, 'a', 'utf-8')
    fh.setLevel(level)
    fh.setFormatter(formatter)
    created_logger.addHandler(fh)

    # Stream handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    created_logger.addHandler(ch)

    return created_logger

if __name__ == '__main__':
    logger = create_logger(logger_name="MyCustomLoggerForLearning", file_name="main.log", level="INFO")

    logger.info("info LOG")
    logger.error("error LOG")
    logger.debug("debug LOG")

    try:
        a = 1 / 0
    except Exception as e:
        logger.error(e)
