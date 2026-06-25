import sqlite3
from bot.config import DATABASE_PATH
from .users import create_user_stats_table
from .triggers import create_auto_responses_table


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def initialize():
    conn = connect()
    create_user_stats_table(conn)
    create_auto_responses_table(conn)

    return conn


def shutdown(conn) -> None:
    conn.commit()
    conn.close()
