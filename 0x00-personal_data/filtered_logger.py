#!/usr/bin/env python3
"""This module handles logging and data privacy."""

import logging
import re
import mysql.connector
import os
from typing import List


class RedactingFormatter(logging.Formatter):
    """Formatter that redacts sensitive information."""

    RED = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEP = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Redacts sensitive data in log records."""

        record.msg = filter_datum(self.fields, self.RED,
                                  record.getMessage(), self.SEP)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Redacts sensitive fields in a log message.
    
    Args:
        fields: Fields to redact.
        redaction: Redaction text.
        message: Log message.
        separator: Separator for fields in the log.
    
    Returns:
        Redacted log message.
    """

    pattern = "|".join([f"{field}=([^{separator}]*)" for field in fields])
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)


def get_logger() -> logging.Logger:
    """Creates and configures a logger."""

    lgr = logging.getLogger("user_data")
    lgr.setLevel(logging.INFO)
    lgr.propagate = False
    st_hand = logging.StreamHandler()
    st_hand.setFormatter(RedactingFormatter(["name", "email", "phone", "ssn", "password"]))
    lgr.addHandler(st_hand)
    return lgr


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to the database."""
    return mysql.connector.connect(
        user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.environ.get("PERSONAL_DATA_DB_NAME")
    )


def main():
    """Fetches and logs user data from the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [desc[0] for desc in cursor.description]

    lgr = get_logger()

    for row in cursor:
        str_row = ''.join(f'{field}={str(value)}; ' for value, field in zip(row, field_names))
        lgr.info(str_row.strip())

    cursor.close()
    db.close()
