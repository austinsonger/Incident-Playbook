import sys

from loguru import logger

from beagle.config import Config

logger.remove(0)
logger.add(
    sys.stdout,
    colorize=True,
    level=Config.get("general", "log_level").upper(),
    format="<green>{time:YYYY-MM-DDTHH:mm:ss}</green> | "
    + "<red>{name}.{function}:{line}</red> | "
    + "<cyan>{level}</cyan> | <level>{message}</level>",
)
