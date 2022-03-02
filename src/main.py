import logging
from triple import Triple

logging.basicConfig(level=logging.NOTSET,
                    format="%(asctime)s - %(name)-5s - %(levelname)-7s - %(message)s")

tr = Triple()


if __name__ == '__main__':
    tr.run()
