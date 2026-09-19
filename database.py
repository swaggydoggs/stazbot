import sqlite3

from config import DATABASE_FILE


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    return connection


def init_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            level INTEGER NOT NULL DEFAULT 1,
            xp INTEGER NOT NULL DEFAULT 0,

            stazbux INTEGER NOT NULL DEFAULT 0,

            last_daily INTEGER NOT NULL DEFAULT 0,
            last_xp INTEGER NOT NULL DEFAULT 0,

            PRIMARY KEY (guild_id, user_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            amount INTEGER NOT NULL,
            balance_after INTEGER NOT NULL,

            transaction_type TEXT NOT NULL,
            description TEXT,

            created_at INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qotd_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,

            created_at INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qotd_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,

            channel_id INTEGER,
            thread_id INTEGER,

            created_at INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qotd_rewards (
            qotd_id INTEGER NOT NULL,
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            PRIMARY KEY (qotd_id, user_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS guess_word_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            clues TEXT NOT NULL,
            answer TEXT NOT NULL,

            active INTEGER NOT NULL DEFAULT 1,
            created_at INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS guess_flag_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            country TEXT NOT NULL,
            flag TEXT NOT NULL,

            active INTEGER NOT NULL DEFAULT 1,
            created_at INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS approved_rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            reward_type TEXT NOT NULL,
            amount INTEGER NOT NULL,

            approved_by INTEGER NOT NULL,
            created_at INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS custom_roles (
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            role_id INTEGER NOT NULL,

            color_one TEXT NOT NULL,
            color_two TEXT NOT NULL,
            image_url TEXT NOT NULL,

            created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL,

            PRIMARY KEY (guild_id, user_id)
        )
        """
    )

    connection.commit()
    connection.close()


def get_user(guild_id: int, user_id: int):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE guild_id = ?
        AND user_id = ?
        """,
        (guild_id, user_id),
    )

    user = cursor.fetchone()

    connection.close()

    return user


def create_user(guild_id: int, user_id: int):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users (
            guild_id,
            user_id
        )
        VALUES (?, ?)
        """,
        (guild_id, user_id),
    )

    connection.commit()
    connection.close()


def ensure_user(guild_id: int, user_id: int):
    create_user(guild_id, user_id)
    return get_user(guild_id, user_id)
