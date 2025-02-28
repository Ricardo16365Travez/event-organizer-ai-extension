import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)
