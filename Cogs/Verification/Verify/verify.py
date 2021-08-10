# Import discord.py stuff
from discord.ext import commands

# Import the helper functions
from .already_verified import already_verified
from .check_description import is_verification_successful
from .get_profile_data import get_profile_data
from .give_role import give_role
from .valid_profile_link import valid_profile_link
from .save_into_database import save_data
from .send_uuid import send_uuid


# Command decorators
# @commands.cooldown(1, 300, commands.BucketType.user)  # 5 mins per user
@commands.command(
    name="verify",
    description=("Start the verification process of your Quora profile.\n\n"
                 "Usage: q/verify <Your profile link here>"),
    brief="Verify your profile",
)
@commands.guild_only()
# Command definition starts
async def verify(self, ctx, profile: str = None):

    if profile is None:
        await ctx.send("Where is the profile to verify?")
        return

    if await already_verified(ctx, profile):
        return

    useragent = "quora-profile-verifier/1.0 (Unshortening qr.ae link) "
    useragent += "A discord bot which verifies Quora profile on voluntary "
    useragent += "request of a human user on Discord. Only the public info as "
    useragent += "seen w/o login is used."
    header = {'User-Agent': useragent}

    if not await valid_profile_link(profile, header):
        await ctx.send("Invalid form of URL. URL must be of the type:\n"
                       "```https://www.quora.com/profile/Gumnaam-Praani```"
                       "If you used `qr.ae` link, make sure it points "
                       "to a profile. All links must be `https`.")
        return

    random_uuid = await send_uuid(self, ctx)

    user_data = await get_profile_data(ctx, profile, header)

    if user_data is None:
        await ctx.send("Unable to verify profile! Please ping a moderator "
                       "or an administrator, *but only if required*, i.e.,"
                       " the problem is with the bot and not on your or "
                       "Quora's end.")
        return

    if (await is_verification_successful(ctx, user_data, random_uuid)):
        await save_data(ctx, user_data)
        await give_role(ctx)
# End of verify()
