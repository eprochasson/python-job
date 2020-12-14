import logging
import datetime

logger = logging.getLogger(__name__)


def fn():
    logger.info("I entered this function at {}".format(datetime.datetime.now().isoformat()))