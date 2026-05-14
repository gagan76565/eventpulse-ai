import sqlite3
import json


DATABASE_PATH = "database/eventpulse.db"


def init_db():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            total_feedback INTEGER,

            positive_percent INTEGER,

            negative_percent INTEGER,

            neutral_percent INTEGER,

            event_score INTEGER,

            themes TEXT,

            complaints TEXT,

            suggestions TEXT

        )

    """)

    conn.commit()

    conn.close()


def save_analysis(data):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO analyses (

            total_feedback,
            positive_percent,
            negative_percent,
            neutral_percent,
            event_score,
            themes,
            complaints,
            suggestions

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data["total_feedback"],

        data["positive_percent"],

        data["negative_percent"],

        data["neutral_percent"],

        data["event_score"],

        json.dumps(data["top_themes"]),

        json.dumps(data["complaints"]),

        json.dumps(data["suggestions"])

    ))

    conn.commit()

    conn.close()