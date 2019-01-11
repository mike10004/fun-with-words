import os
import logging

_log = logging.getLogger(__name__)
_logging_configured = False


def configure_logging():
    global _logging_configured
    if not _logging_configured:
        level_str = os.getenv('UNIT_TEST_LOG_LEVEL') or 'INFO'
        level = logging.__dict__.get(level_str, 'INFO')
        logging.basicConfig(level=level)
        _log.debug("logging configured at level %s (%s)", level, level_str)
        logging_configured = True
