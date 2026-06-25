def create_auto_responses_table(conn) -> None:
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
    def __init__(self, guild_id, trigger, response, enabled) -> None:
        self.guild_id = guild_id
        self.trigger: str = trigger
        self.response: str = response
        self.enabled: bool = enabled


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
    VALUES (?, ?, ?, ?)
    """,
        trigger_data,
    )
    conn.commit()


def delete_trigger(conn, trigger) -> None:
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
    cursor = conn.cursor()
    cursor.execute(
        """
    UPDATE auto_responses 
    SET enabled = ? 
    WHERE guild_id = ? 
        AND trigger = ?
    """,
        (state, trigger.guild_id, trigger.trigger),
    )

    conn.commit()
    return cursor.rowcount != 0  # return False if no value gets deleted


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


def query_all_triggers(conn, guild_id):
    cursor = conn.cursor()
    cursor.execute(
        """
    SELECT trigger, response 
    FROM auto_responses 
    WHERE guild_id = ?
    """,
        (guild_id,),
    )

    return cursor.fetchall()


def delete_triggers(conn, trigger):
    cursor = conn.cursor()
    cursor.execute(
        """
    DELETE FROM auto_responses
    WHERE guild_id = ?
        AND trigger = ?;
        """,
        (trigger.guild_id, trigger.trigger),
    )

    conn.commit()
    return cursor.rowcount != 0  # return False if no value gets deleted
