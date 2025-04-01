import discord
import os
from pprint import pprint

from oneshot import get_bearer_token, get_endpoint, call_endpoint

# this is the endpoint id of the deployToken endpoint which will deploy ERC20 tokens
ENDPOINT_ID = os.getenv("ENDPOINT_ID", "deployToken_endpoint")

access_token = get_bearer_token()
endpoint = get_endpoint(access_token, ENDPOINT_ID)

bot = discord.Bot()

# example of how to create a command with a button
class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked

@bot.slash_command() # Create a slash command
async def button(ctx):
    await ctx.respond("This is a button!", view=MyView()) # Send a message with our View class that contains the button

# example of a simple command with no arguments
@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    print("Ping command called")
    await ctx.respond(f"Pong! Latency is {bot.latency}")

# example of a command with arguments that will call 1Shot API
@bot.command(description="Deploy a token.")
async def deploy_token(ctx, admin: str, name: str, symbol: str, supply: str):
    for param in endpoint.params:
        if param.name == "admin":
            param.value = admin
        elif param.name == "name":
            param.value = name
        elif param.name == "ticker":
            param.value = symbol
        elif param.name == "premint":
            param.value = supply + "000000000000000000"  # Assuming supply is in wei
    # Call the endpoint with the updated parameters
    execution = call_endpoint(access_token, endpoint)
    await ctx.respond(f"Deploying {name} owned by {admin} with {supply} amount of {symbol}. Transaction Hash: {execution.transactionHash}")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token or set DISCORD_BOT_TOKEN as an environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_BOT_TOKEN")

if __name__ == "__main__":
    print("Starting bot...")
    bot.run(TOKEN)