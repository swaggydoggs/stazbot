import os
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import STAZOR_REALM_GUILD_ID, BOT_PREFIX
from database import init_database
from setup import setup_command


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN is missing. Add it to your .env file."
    )

if not STAZOR_REALM_GUILD_ID:
    raise RuntimeError(
        "STAZOR_REALM_GUILD_ID is missing. Add your Stazor Realm server ID "
        "to the .env file."
    )


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("StazBot")


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True


class StazBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=BOT_PREFIX,
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        init_database()

        self.tree.add_command(
            setup_command,
            guild=discord.Object(id=STAZOR_REALM_GUILD_ID),
        )

        guild = discord.Object(id=STAZOR_REALM_GUILD_ID)

        try:
            synced = await self.tree.sync(guild=guild)
            logger.info(
                "Synced %s slash command(s) to Stazor Realm.",
                len(synced),
            )
        except Exception:
            logger.exception("Failed to sync slash commands.")

    async def on_ready(self):
        logger.info(
            "Logged in as %s (%s)",
            self.user,
            self.user.id,
        )

        logger.info(
            "Connected to %s guild(s).",
            len(self.guilds),
        )


bot = StazBot()


@bot.event
async def on_guild_join(guild: discord.Guild):
    logger.info(
        "Joined guild: %s (%s)",
        guild.name,
        guild.id,
    )


bot.run(TOKEN)
