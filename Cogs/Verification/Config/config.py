# Import external dependencies
import aiosqlite

# Import discord.py stuff
import discord
from discord.ext import commands

# Import DB creation function
from Events.on_guild_join import set_up_guild


# Command decorators
@commands.command(
    name="set_role",
    description=("Set the role which is given after verification.\n\n"
                 "Usage: Q/set_role @Verified-Role"),
    brief="Set verified role.",
)
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
# Command definition starts
async def set_role(self, ctx, role: discord.Role = None):

    if role is None:
        await ctx.send("Please mention the verified role while using cmd!")
        return

    await set_up_guild(ctx.guild)

    # Execute SQL

    SQL_CMD_CREATE = "INSERT OR IGNORE INTO settings VALUES (?, 0)"
    SQL_CMD_SET = "UPDATE settings SET value=? WHERE setting=?;"

    try:
        conn = await aiosqlite.connect(f"./Database/{ctx.guild.id}.db")
        await conn.execute(SQL_CMD_CREATE, ["access_role_id"])
        await conn.execute(SQL_CMD_SET, (role.id, "access_role_id"))
    except aiosqlite.Error as e:
        print(e)
        await ctx.send("Error in database! Reinvite the bot.")
    else:
        # Commit transaction and send confirmation
        await conn.commit()
        await ctx.send("Successfully set the verified role!")
    finally:
        await conn.close()
# End of set_role()


# End of file
