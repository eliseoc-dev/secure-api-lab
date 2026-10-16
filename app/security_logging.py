import logging


security_logger = logging.getLogger(
    "security"
)

security_logger.setLevel(
    logging.INFO
)


if not security_logger.handlers:
    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )

    handler.setFormatter(
        formatter
    )

    security_logger.addHandler(
        handler
    )