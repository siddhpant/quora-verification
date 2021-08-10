# Import standard library dependencies
from urllib.parse import urlparse

# Import external dependencies
import aiosqlite


async def already_verified(ctx, profile) -> bool:
    """Check if a discord user or quora profile already exists."""

    profile_path = urlparse(profile).path

    SQL_CMD_DISCORD = "SELECT count(*) FROM users WHERE discord_uid=?"
    SQL_CMD_QUORA = "SELECT count(*) FROM users WHERE quora_profile=?"

    already_verified = False

    # Open database and execute query
    try:
        conn = await aiosqlite.connect(f"./Database/{ctx.guild.id}.db")
        discord_cursor = await conn.execute(SQL_CMD_DISCORD, [ctx.author.id])
        quora_cursor = await conn.execute(SQL_CMD_QUORA, [profile_path])
    except aiosqlite.OperationalError:
        await ctx.send("There's a problem with this server setting's database."
                       "\nPlease use the `set_role` command to fix it.")
        raise
    else:
        if (await discord_cursor.fetchone())[0] != 0:
            await ctx.send("You have already verified here!")
            already_verified = True
        elif (await quora_cursor.fetchone())[0] != 0:
            await ctx.send("This Quora profile is already verified by "
                           "another user.")
            already_verified = True
    finally:
        await discord_cursor.close()
        await quora_cursor.close()
        await conn.close()

    return already_verified
# End of already_verified()


# End of file
