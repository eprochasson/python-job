import logging
import sys


if __name__ == '__main__':

    logging.basicConfig(level='DEBUG', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Testing external dependency")
    try:
        import requests
        logger.info("\tPassed!")
    except ModuleNotFoundError as e:
        logger.fatal("Dependency module not found")

    try:
        logger.info("Loading external file")
        f = open('data/test.csv').readlines()
        logger.info("\t{} lines found in f".format(len(f)))
    except FileNotFoundError as e:
        logger.fatal("Missing external file!")

    logger.info("Loading local module")
    try:
        from lib.nothing import fn
        fn()
        logging.info("\tPassed")
    except ModuleNotFoundError as e:
        logger.fatal("Local module not found")


    logging.info("Scanning arguments...")
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        logger.info("No arguments passed")
    else:
        logger.info("Arguments: {}".format(' '.join(arguments)))