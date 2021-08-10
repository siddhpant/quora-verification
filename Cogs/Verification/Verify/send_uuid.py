# Import standard library dependencies
from uuid import uuid4

# Import external dependencies
import asyncio

# Import discord.py stuff
from discord import Message


async def send_uuid(self, ctx):
    """To send the random string (a random UUID) for verifying the profile."""

    random_uuid = str(uuid4())

    await ctx.send("Please add the following string to the first line of your "
                   "profile's *description*.")
    await ctx.send(f"```{random_uuid}```")
    await ctx.send("You have 5 minutes to do so. Once you enter it on your "
                   "profile, come back here and type `q/continue` to verify.")

    def check(message: Message) -> bool:
        return message.author == ctx.author and message.content == "q/continue"

    try:
        await self.bot.wait_for("message", check=check, timeout=300)
    except asyncio.TimeoutError:
        await ctx.send(f"Time up, {ctx.author.mention}!")
        return
    else:
        await ctx.send("Okay! Just a moment...")
        return random_uuid
# End of send_uuid()


# End of file
