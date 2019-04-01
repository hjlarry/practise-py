import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
bf = logging.Formatter("{asctime} {name} [{levelname:^11s}] {message}", style="{")
handler.setFormatter(bf)
root.addHandler(handler)
logger = logging.getLogger()
logger.debug("This is a DEBUG message")
logger.info("This is a INFO message")
logger.warning("This is a WARNING message")

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
logging.debug("it works")  # DEBUG it works
logging.addLevelName(logging.DEBUG, " [DEBUG] ")
logging.debug("it works")  # [my debug name]{BLANK PADDINGS} it works
