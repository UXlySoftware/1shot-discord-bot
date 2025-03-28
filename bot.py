import discord
from discord.ext import commands
import os

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Ensure the user has admin permissions
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f"Bot is ready and logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()  # Sync slash commands with Discord
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Define a slash command
@bot.tree.command(name="echo", description="Echoes the provided message.")
async def echo(interaction: discord.Interaction, message: str):
    """Responds with the user's message."""
    await interaction.response.send_message(f"You said: {message}")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_BOT_TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)
