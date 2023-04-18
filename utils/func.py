from logger import getLogger

logger = getLogger(__name__)

def func():
    a = 3
    logger.debug(f"a:{a}")
    print(logger)
    print(666)


if __name__ == "__main__":
    print( func())

