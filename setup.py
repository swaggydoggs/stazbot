import discord
from discord import app_commands

from config import (
    STAZOR_REALM_GUILD_ID,
    SETUP_CATEGORY_NAME,
    SETUP_CHANNELS,
)


async def find_category(
    guild: discord.Guild,
    name: str,
):
    for category in guild.categories:
        if category.name == name:
            return category

    return None


async def find_text_channel(
    guild: discord.Guild,
    name: str,
):
    for channel in guild.text_channels:
        if channel.name == name:
            return channel

    return None


@app_commands.command(
    name="setup",
    description="Set up StazBot channels for Stazor Realm.",
)
@app_commands.guild_only()
async def setup_command(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "This command can only be used inside a server.",
            ephemeral=True,
        )
        return

    if guild.id != STAZOR_REALM_GUILD_ID:
        await interaction.response.send_message(
            "StazBot setup is only available in Stazor Realm.",
            ephemeral=True,
        )
        return

    if not (
        guild.owner_id == interaction.user.id
        or interaction.user.guild_permissions.administrator
    ):
        await interaction.response.send_message(
            "You must be the server owner or have Administrator permission "
            "to use `/setup`.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True)

    category = await find_category(
        guild,
        SETUP_CATEGORY_NAME,
    )

    if category is None:
        category = await guild.create_category(
            SETUP_CATEGORY_NAME,
            reason="StazBot automatic server setup",
        )

    created_channels = []
    existing_channels = []

    for channel_name, _channel_type in SETUP_CHANNELS:
        channel = await find_text_channel(
            guild,
            channel_name,
        )

        if channel is not None:
            existing_channels.append(channel_name)

            if channel.category != category:
                try:
                    await channel.edit(
                        category=category,
                        reason="StazBot setup organization",
                    )
                except discord.Forbidden:
                    pass

            continue

        await guild.create_text_channel(
            channel_name,
            category=category,
            reason="StazBot automatic server setup",
        )

        created_channels.append(channel_name)

    embed = discord.Embed(
        title="StazBot Setup",
        description="The StazBot setup has been completed.",
    )

    if created_channels:
        embed.add_field(
            name="Created",
            value="\n".join(
                f"• `{name}`"
                for name in created_channels
            ),
            inline=False,
        )
    else:
        embed.add_field(
            name="Created",
            value="No new channels were needed.",
            inline=False,
        )

    if existing_channels:
        embed.add_field(
            name="Already Existing",
            value="\n".join(
                f"• `{name}`"
                for name in existing_channels
            ),
            inline=False,
        )

    await interaction.followup.send(
        embed=embed,
        ephemeral=True,
    )
