from ..utils.logger import getLogger

logger = getLogger(__name__)

def func():
    a = 3
    logger.debug(f"a:{a}")

