import logging

# define logger callable by module name
stdlogger = logging.getLogger(__name__)

# log level DEBUG
def debug_logger(request_user, log_text):
    stdlogger.debug(
        request_user +
        log_text
    )

# log level INFO
def info_logger(request_user, log_text):
    stdlogger.info(
        request_user +
        log_text
    )

# log level WARNING
def warning_logger(request_user, log_text):
    stdlogger.warning(
        request_user +
        log_text
    )

# log level ERROR
def error_logger(request_user, log_text):
    stdlogger.error(
        request_user +
        log_text
    )

# log level CRITICAL
def critical_logger(request_user, log_text):
    stdlogger.critical(
        request_user +
        log_text
    )
