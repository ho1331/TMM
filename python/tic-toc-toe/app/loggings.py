"""logging of game"""
import logging


class Loging:
    """class Loging"""

    @staticmethod
    def log_win(name):
        """write logfile of winners"""
        logging.basicConfig(
            format="%(asctime)s - %(message)s", level=logging.INFO, filename="xolog.log"
        )
        logger = logging.getLogger()
        logger.info(f"{name} победил!")
