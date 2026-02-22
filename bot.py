import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import logging
import os
from dotenv import load_dotenv

# ─── Logging Setup ───────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("SSRoleBot")

# ─── Load Environment Variables ──────────────────────────────────────────────
load_dotenv()

TOKEN          = os.getenv("DISCORD_TOKEN")
SS_CHANNEL_ID  = int(os.getenv("SS_CHANNEL_ID", 0))
ROLE_ID        = int(os.getenv("ROLE_ID", 0))
YOUTUBE_LINK   = os.getenv("YOUTUBE_LINK", "https://youtube.com")
GUILD_ID       = int(os.getenv("GUILD_ID", 0))

# ─── Bot Setup ───────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ─── Helper: Beautiful Role Given Embed ──────────────────────────────────────
def role_given_embed(member: discord.Member, role: discord.Role) -> discord.Embed:
    embed = discord.Embed(
        title="🥰 Thanks For Subscribing!",
        description=(
            f"**LoveU My Public Keep Supporting Me 😊**\n\n"
            f"You Have Been Granted The {role.mention} Role in Server.:\n"
            f"Yara Apni Profile Check Kr Loo! 🌟"
        ),
        color=discord.Color.gold()
    )
    embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="🎭 Role", value=role.mention, inline=True)
    embed.set_footer(text="BOT PROGRAMMED BY SUBHAN | SARAIKI PLAY")
    embed.timestamp = discord.utils.utcnow()
    return embed

# ─── Helper: Already Has Role Embed ──────────────────────────────────────────
def already_has_role_embed(member: discord.Member, role: discord.Role) -> discord.Embed:
    embed = discord.Embed(
        title="ℹ️ Already Subscribed!",
        description=(
            f"{member.mention}, you already have the {role.mention} role!\n\n"
            f"You are already a verified subscriber. 💙"
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="BOT PROGRAMMED BY SUBHAN | SARAIKI PLAY")
    embed.timestamp = discord.utils.utcnow()
    return embed

# ─── Helper: Warning Embed (Wrong Channel) ───────────────────────────────────
def warning_embed(member: discord.Member) -> discord.Embed:
    embed = discord.Embed(
        title="⚠️ Wrong Channel!",
        description=(
            f"{member.mention}, this channel is only for **Screenshot Submissions**!\n\n"
            f"📸 Only send your YouTube subscribe screenshot here.\n"
            f"💬 Please use <#1377200130880569435> channels for chatting."
        ),
        color=discord.Color.red()
    )
    embed.set_footer(text="BOT PROGRAMMED BY SUBHAN | SARAIKI PLAY")
    embed.timestamp = discord.utils.utcnow()
    return embed

# ─── Helper: Notify Embed ────────────────────────────────────────────────────
def notify_embed(guild: discord.Guild, yt_link: str) -> tuple[discord.Embed, discord.ui.View]:
    embed = discord.Embed(
        title="AoA Mari Piary Public.🤗",
        description=(
            "**Yara Subscribe My Channel SARAIKIPLAYS-S**\n"
            "And Get Special Role in Server\n\n"
            f"📺 **Channel:** [Click Here]({yt_link})\n\n"
            "📸 After subscribing, send your screenshot in this channel to get your role!"
        ),
        color=discord.Color.red()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.set_footer(text="SARAIKI PLAYS-S")
    embed.timestamp = discord.utils.utcnow()

    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(
            label="🔔 Subscribe Now",
            url=yt_link,
            style=discord.ButtonStyle.link
        )
    )
    return embed, view

# ─── Event: Bot Ready ─────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    logger.info(f"Bot is online: {bot.user} (ID: {bot.user.id})")
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await tree.sync(guild=guild)
        logger.info(f"Synced {len(synced)} slash commands to guild {GUILD_ID}")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="SARAIKI PLAY"
        )
    )

# ─── Event: Message (SS Channel Handler) ─────────────────────────────────────
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Only process messages in SS channel
    if message.channel.id != SS_CHANNEL_ID:
        await bot.process_commands(message)
        return

    # Check if message has an attachment (screenshot)
    if message.attachments:
        await handle_ss_submission(message)
    else:
        # No attachment = just chatting → delete + warn
        await handle_unwanted_message(message)

    await bot.process_commands(message)

# ─── Handler: Screenshot Submission ──────────────────────────────────────────
async def handle_ss_submission(message: discord.Message):
    member = message.author
    guild  = message.guild

    try:
        role = guild.get_role(ROLE_ID)
        if not role:
            logger.error(f"Role with ID {ROLE_ID} not found in guild!")
            await message.channel.send(
                embed=discord.Embed(
                    title="❌ Configuration Error",
                    description="Role not found. Please contact an admin.",
                    color=discord.Color.red()
                ),
                delete_after=10
            )
            return

        # Check if member already has the role
        if role in member.roles:
            await message.channel.send(
                embed=already_has_role_embed(member, role),
                delete_after=15
            )
            logger.info(f"{member} already has role {role.name}")
            return

        # Give the role
        await member.add_roles(role, reason="Subscribed to YouTube channel - SS verified")
        logger.info(f"Role '{role.name}' given to {member}")

        # Send beautiful success message
        await message.channel.send(embed=role_given_embed(member, role))

    except discord.Forbidden:
        logger.error(f"Missing permissions to assign role to {member}")
        await message.channel.send(
            embed=discord.Embed(
                title="❌ Permission Error",
                description="Bot doesn't have permission to assign roles. Please contact admin.",
                color=discord.Color.red()
            ),
            delete_after=10
        )
    except discord.HTTPException as e:
        logger.error(f"HTTP error while assigning role: {e}")

# ─── Handler: Unwanted Chat Message ──────────────────────────────────────────
async def handle_unwanted_message(message: discord.Message):
    member = message.author
    try:
        # Delete the message
        await message.delete()
        logger.info(f"Deleted chat message from {member} in SS channel")

        # Send warning (auto-delete after 8 seconds)
        await message.channel.send(
            embed=warning_embed(member),
            delete_after=8
        )
    except discord.Forbidden:
        logger.error(f"Missing permissions to delete message from {member}")
    except discord.NotFound:
        pass  # Message already deleted
    except discord.HTTPException as e:
        logger.error(f"HTTP error while handling message: {e}")

# ─── Slash Command: /notify ───────────────────────────────────────────────────
@tree.command(
    name="notify",
    description="Send a beautiful notification embed about YouTube subscription",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.checks.has_permissions(manage_messages=True)
async def notify_command(interaction: discord.Interaction):
    try:
        embed, view = notify_embed(interaction.guild, YOUTUBE_LINK)
        await interaction.response.send_message(embed=embed, view=view)
        logger.info(f"/notify used by {interaction.user} in #{interaction.channel}")
    except Exception as e:
        logger.error(f"Error in /notify command: {e}")
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Error",
                description="Something went wrong. Please try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )

@notify_command.error
async def notify_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🚫 No Permission",
                description="You need **Manage Messages** permission to use this command.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
    else:
        logger.error(f"Unexpected error in /notify: {error}")
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Error",
                description=f"An unexpected error occurred: `{error}`",
                color=discord.Color.red()
            ),
            ephemeral=True
        )

# ─── Run Bot ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not TOKEN:
        logger.critical("DISCORD_TOKEN not found in environment variables!")
        exit(1)
    if not SS_CHANNEL_ID or not ROLE_ID or not GUILD_ID:
        logger.critical("SS_CHANNEL_ID, ROLE_ID, or GUILD_ID not set in environment variables!")
        exit(1)

    try:
        bot.run(TOKEN, log_handler=None)
    except discord.LoginFailure:
        logger.critical("Invalid Discord token! Please check your DISCORD_TOKEN.")
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
