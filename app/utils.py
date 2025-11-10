import logging
import os
from enum import Enum
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import jwt


"""_summary_
    LogSevice Class to handling logging in the App
"""


class LogServiceType(str, Enum):
    DATABASE = "database"
    ENDPOINT = "endpoint"
    SERVICE = "service"
    LOGS = "logs"


class LogType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class LoggingService:
    """A logging service"""

    def __init__(self):
        """Create all needed log file(s) when class is instantiated"""
        # Log config
        self._base_dir = "./app/logs/"
        self.file_extention = ".txt"
        self._log_paths = []

        # ensure base directory exist
        if not os.path.exists(self._base_dir):
            os.mkdir(self._base_dir)

        # Create log path based on LogServiceTypes
        for service in LogServiceType:
            self._log_paths.append(
                f"{self._base_dir}{service.value}{self.file_extention}"
            )

        # create log files is not present
        self._create_log_file_if_not_exist()

    def set_log(
        self,
        message: str,
        log_service_type: LogServiceType | None = None,
        log_type: LogType = LogType.INFO,
    ):
        """Create a log by accepting the LogServiceType and the LogType"""

        # Default filename
        filename = f"{self._base_dir}{LogServiceType.LOGS.value}{self.file_extention}"

        # Determines the log file to use based on the service_type
        for service in LogServiceType:
            if service.value == log_service_type:
                filename = f"{self._base_dir}{service.value}{self.file_extention}"

        # log config to use
        logger = logging.getLogger(log_service_type or "logs")

        if not logger.handlers:
            file_handler = logging.FileHandler(filename)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.setLevel(logging.INFO)

        # log_type is set for the log
        log_func = getattr(logger, log_type.value)
        log_func(message)

    # checks if the log file exists
    def _check_if_file_exist(self, path: str) -> bool:
        return True if os.path.exists(path) else False

    # create log file if not present
    def _create_log_file_if_not_exist(self):
        for path in self._log_paths:
            if not self._check_if_file_exist(path):
                with open(path, "w") as f:  # noqa
                    pass


# create an instance of the LoggingServiceß
logging_service = LoggingService()


"""_summary_
    JWT OAuth2 Authentication functions to handling user authentication
"""


# generate encoded JWT
def generate__jwt_token(user_data: dict, expiry=timedelta(minutes=30)):
    from app.config import security_settings

    try:
        return jwt.encode(
            payload={
                "user": user_data,
                "exp": datetime.now(timezone.utc) + expiry,
                "jti": str(uuid4()),
            },
            key=security_settings.JWT_SECRET,
            algorithm=security_settings.JWT_ALGORITHM,
        )
    except Exception as e:
        logging_service.set_log(
            message=f"{e}", log_service_type=LogServiceType.LOGS, log_type=LogType.ERROR
        )
        return None


# decode encoded JWT
def decode_encoded_jwt_token(token: str):
    from app.config import security_settings

    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )

    except Exception as e:
        logging_service.set_log(
            message=f"{e}", log_service_type=LogServiceType.LOGS, log_type=LogType.ERROR
        )
        return None
