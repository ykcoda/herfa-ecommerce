import logging


loglevel = "error"
log_func = getattr(logging, loglevel)
log_func("Info logging")
