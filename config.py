import os

from dotenv import load_dotenv


load_dotenv()


BOT_PREFIX = "-"

STAZOR_REALM_GUILD_ID = int(
    os.getenv("STAZOR_REALM_GUILD_ID", "0")
)


DATABASE_FILE = "stazbot.db"


SETUP_CATEGORY_NAME = "│「🤖」│STAZBOT"

SETUP_CHANNELS = [
    ("│「🤖」│bot-commands", "bot"),
    ("│「📈」│leveling", "leveling"),
    ("│「💰」│stazbux", "stazbux"),
    ("│「❓」│qotd", "qotd"),
    ("│「😀」│guess-the-word", "guess-word"),
    ("│「🌎」│guess-the-flag", "guess-flag"),
    ("│「🎨」│fan-art", "fan-art"),
    ("│「💡」│suggestions", "suggestions"),
    ("│「✨」│custom-roles", "custom-roles"),
]
