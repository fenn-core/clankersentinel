from config import SETTINGS


def create_wallets_table(conn) -> None:
    conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        balance INTEGER NOT NULL CHECK (balance >= 0),        
        PRIMARY KEY (guild_id, user_id)    
    )""")
    conn.commit()


def ensure_wallet(conn, guild_id: int, user_id: id) -> bool:
    """
    Ensure that the user has an entry in the database table, creating one if necessary.

    """

    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT OR IGNORE INTO wallets
    (guild_id, user_id, balance)
    VALUES (?, ?, ?)
    """,
        guild_id,
        user_id,
        SETTINGS["wallet"]["default_balance"],
    )
    conn.commit()

    return cursor.rowcount > 0  # return False if user already exists


def reset_wallet(conn, guild_id: int, user_id: int) -> None:
    """
    Resets the users balance to the default value.

    """

    conn.cursor.execute(
        """
    UPDATE wallets 
    SET balance = ?
    WHERE guild_id = ?
        AND user_id = ?;
    """,
        (SETTINGS["wallet"]["default_balance"], guild_id, user_id),
    )
    conn.commit()


def update_balance(conn, guild_id: int, user_id: int, amount: int) -> None:
    """
    Updates the balance of the specified user in the database.

    Use negative values for deducting balance.

    """

    conn.cursor().execute(
        """
    UPDATE wallets 
    SET balance = balance + ?
    WHERE guild_id = ?
        AND user_id = ?; 
    """,
        (amount, guild_id, user_id),
    )
    conn.commit()


def query_wallet_balance(conn, guild_id: int, user_id: int):
    """
    Query and return the balance for the specified wallet.

    """

    cursor = conn.cursor()
    cursor.execute(
        """
    SELECT balance 
    FROM wallets
    WHERE guild_id = ? AND user_id = ?;  
    """,
        guild_id,
        user_id,
    )

    return cursor.fetchone()
