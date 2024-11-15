import logging


def create_logger(loggers_info_dict: dict) -> dict:
    loggers = {}
    for logger_name, logger_info in loggers_info_dict.items():
        file_handler = logging.FileHandler(logger_info["logging_file"], mode='w')
        stream_handler = logging.StreamHandler()
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger = logging.getLogger(logger_name)
        logger.setLevel(logger_info["level"])
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        loggers[logger_name] = logger
    return loggers
