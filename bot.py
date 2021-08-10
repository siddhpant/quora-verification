# Import standard library dependencies
import os

# Import external dependencies
import pendulum

# Import discord.py stuff
from discord.ext import commands

# Import events
from Events.on_guild_join import set_up_guild


# Initialise bot
bot = commands.Bot(command_prefix="q/")

# Cogs or extensions or categories
extensions = [
    "Cogs.Verification.verification_cog"
]

# Load cogs
for cog in extensions:
    bot.load_extension(cog)


# Print bot details
@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("--------------------------------")
# End of on_ready()


@bot.event
async def on_command_error(ctx, error):

    mention = ctx.author.mention

    # If user uses command before cooldown gets over
    if isinstance(error, commands.CommandOnCooldown):
        retry = pendulum.duration(seconds=error.retry_after).in_words()
        await ctx.send(f"Retry after {retry}! Have patience, {mention}!")

    # If missing permissions for executing commands
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You are not allowed to do that, {mention}.")
# End of on_command_error()


@bot.event
async def on_guild_join(guild):
    await set_up_guild(guild)
# End of on_guild_join()


@bot.command
async def invite(self, ctx):
    perms = 268438528
    params = f"client_id={bot.user.id}&permissions={perms}"
    link = f"https://discordapp.com/oauth2/authorize?scope=bot&{params}"
    await ctx.send(link)
# End of invite


# Run the bot with token
bot.run(os.environ["TOKEN_BOT"])

# bot.run ends when bot logs out
print("Logged out.")


# End of file
