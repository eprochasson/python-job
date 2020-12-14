import logging
import sys


if __name__ == '__main__':

    logging.basicConfig(level='DEBUG', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Testing external dependency")
    try:
        import requests
    except ModuleNotFoundError as e:
        logger.fatal("Dependency module not found")

    logger.info("Loading external file")
    f = open('data/test.csv').readlines()
    logger.info("{} lines found in f".format(len(f)))

    logger.info("Loading local module")
    try:
        from lib.nothing import fn
        fn()
    except ModuleNotFoundError as e:
        logger.fatal("Local module not found")


    arguments = sys.argv[1:]
    if len(arguments) == 0:
        logger.info("No arguments passed")
    else:
        logger.info("Arguments: {}".format(' '.join(arguments)))