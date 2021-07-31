import logging


class Logger:

    _logger: logging.Logger

    def __init__(self) -> None:
        self._logger = None


# https://github.com/PabloLec/RecoverPy/blob/main/recoverpy/logger.py
