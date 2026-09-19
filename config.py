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


XP_MIN = 10
XP_MAX = 20
XP_COOLDOWN = 60

CHAT_STAZBUX_MIN = 2
CHAT_STAZBUX_MAX = 5

DAILY_COOLDOWN = 86400

GUESS_COOLDOWN = 30
GUESS_REWARD = 25

QOTD_REWARD = 15

STARTING_LEVEL = 1

DAILY_REWARDS = {
    1: 30,
    2: 30,
    3: 30,
    4: 30,
    5: 30,
    6: 30,
    7: 30,
}

MAX_LEVEL = 100
