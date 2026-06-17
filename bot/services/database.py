from bot.config import DATABASE_PATH
import sqlite3


def create_user_stats_table(conn):
    conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS user_stats (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message_count INTEGER NOT NULL DEFAULT 0,
        voice_seconds INTEGER NOT NULL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP, 
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (guild_id, user_id)
    )
               
    """)
    conn.commit()


class User:
    def __init__(self, guild_id, user_id):

        self.guild_id = guild_id
        self.user_id = user_id
        self.message_count = 0
        self.voice_seconds = 0

    @property
    def text_xp(self):
        return self.message_count * 20

    @property
    def voice_xp(self):
        return round(self.voice_seconds * 0.006)

    @property
    def total_xp(self):
        return self.text_xp + self.voice_xp

    @property
    def text_level(self):
        return (self.text_xp // 500) + 1

    @property
    def voice_level(self):
        return (self.voice_xp // 500) + 1

    @property
    def level(self):
        return (self.total_xp // 1000) + 1


def ensure_user(conn, user):
    cursor = conn.cursor()
    user_data = (
        user.guild_id,
        user.user_id,
        user.message_count,
        user.voice_seconds,
    )

    cursor.execute(
        """                  
    INSERT OR IGNORE INTO user_stats 
    (guild_id, user_id, message_count, voice_seconds)
    VALUES (?, ?, ?, ?)
    """,
        user_data,
    )

    conn.commit()

    return cursor.rowcount > 0  # return False if user already exists


def increment_message_count(conn, user):
    conn.cursor().execute(
        """
        UPDATE user_stats
        SET message_count = message_count + 1, 
            updated_at = CURRENT_TIMESTAMP
        WHERE guild_id = ? AND user_id = ?;
    """,
        (user.guild_id, user.user_id),
    )
    conn.commit()


def record_voice_session(conn, user, session_duration):
    conn.cursor().execute(
        """
    UPDATE user_stats 
    SET voice_seconds = voice_seconds + ?, 
        updated_at = CURRENT_TIMESTAMP
    WHERE guild_id = ? AND user_id = ?; 
    """,
        (session_duration, user.guild_id, user.user_id),
    )
    conn.commit()


def query_user_stats(conn, user):
    cursor = conn.cursor()
    cursor.execute(
        """
    SELECT message_count, voice_seconds
    FROM user_stats
    WHERE guild_id = ? AND user_id = ?;
    """,
        (user.guild_id, user.user_id),
    )

    return cursor.fetchone()


def create_auto_responses_table(conn):
    conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS auto_responses (
        guild_id INTEGER NOT NULL,
        trigger TEXT NOT NULL,
        response TEXT NOT NULL, 
        enabled BOOL NOT NULL CHECK (enabled IN (0, 1)),
        PRIMARY KEY (guild_id, trigger)
    )
                        
    """)
    conn.commit()


class Trigger:
    def __init__(self, guild_id, trigger, response, enabled):
        self.guild_id = guild_id
        self.trigger = trigger
        self.response = response
        self.enabled = enabled


def add_trigger(conn, trigger):
    trigger_data = (
        trigger.guild_id,
        trigger.trigger.casefold().strip(),
        trigger.response,
        trigger.enabled,
    )

    conn.cursor().execute(
        """ 
    INSERT OR IGNORE INTO auto_responses 
    (guild_id, trigger, response, enabled)
    (?, ?, ?, ?)
    """,
        trigger_data,
    )
    conn.commit()


def delete_trigger(conn, trigger):
    conn.cursor().execute(
        """
    DELETE FROM auto_responses 
    WHERE guild_id = ? 
    AND trigger = ?;
    """,
        (trigger.guild_id, trigger.trigger),
    )
    conn.commit()


def change_trigger_state(conn, trigger, state):
    conn.cursor().execute(
        """
    UPDATE auto_responses 
    SET enable = ? 
    WHERE guild_id = ? 
        AND trigger = ?
    """,
        (state, trigger.guild_id, trigger.trigger),
    )

    conn.commit()


def query_triggers(conn, trigger):
    cursor = conn.cursor()
    cursor.execute(
        """
    SELECT response 
    FROM auto_responses 
    WHERE guild_id = ?
        AND trigger = ?
        AND enabled = 1;
    """,
        (trigger.guild_id, trigger.trigger),
    )

    return cursor.fetchone()


def connect():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def initialize():
    conn = connect()
    create_user_stats_table(conn)
    create_auto_responses_table(conn)

    return conn


def shutdown(conn):
    conn.commit()
    conn.close()
