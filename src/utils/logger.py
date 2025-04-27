from loguru import logger

logger.add(
    "insight-query_logs.log", rotation="1 MB", retention="7 days", compression="zip"
)
