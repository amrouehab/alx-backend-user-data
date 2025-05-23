#!/usr/bin/env python3
"""
Module for filtering and logging personal data securely.
"""

import re
import logging
import os
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields: List of field names to redact.
        redaction: String to replace field values with.
        message: The original log message.
        separator: Character separating fields in the message.

    Returns:
        The obfuscated log message.
    """
    return re.sub(
        fr"({'|'.join(fields)})=.*?{separator}",
        lambda m: f"{m.group(1)}={redaction}{separator}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """
    Custom logging formatter that redacts specified sensitive fields.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the formatter with fields to redact.

        Args:
            fields: List of field names to redact.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, redacting specified fields.

        Args:
            record: The log record to format.

        Returns:
            The formatted and redacted log message.
        """
        original = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger with redaction capabilities.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        MySQLConnection object.
    """
    return mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main():
    """
    Main function that retrieves and logs user data with redacted sensitive fields.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        message = "; ".join(f"{field}={str(value)}" for field, value in zip(fields, row)) + ";"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

