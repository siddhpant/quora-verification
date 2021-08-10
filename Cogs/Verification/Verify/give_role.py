# Import external dependencies
import aiosqlite

# Import discord.py stuff
import discord


async def give_role(ctx):
    """Give the access role (set by guild admin) on verification."""

    SQL_CMD_ROLE = "SELECT value FROM settings where setting=?;"

    # Open database and execute query
    try:
        conn = await aiosqlite.connect(f"./Database/{ctx.guild.id}.db")
        cursor = await conn.execute(SQL_CMD_ROLE, ["access_role_id"])
    except aiosqlite.OperationalError as e:
        print(e)
        await ctx.send("There's a problem with this server's database."
                       "\nPlease use `set_role` command to fix it.")
        raise
    else:
        # Get the amount & close connection; fetchall() returns list of tuples
        role_id = (await cursor.fetchall())[0][0]    # Here it's like [(<id>,)]
        await cursor.close()
        await conn.close()

    try:
        role = discord.utils.get(ctx.guild.roles, id=role_id)
    except Exception as e:
        await ctx.send(f"Oh no! Problem getting role {role_id}\n{e}")
        raise
    else:
        if ctx.me.top_role > role:
            await ctx.author.add_roles(role, reason="Verified profile.")
            await ctx.send("Role given! Hope you enjoy your stay!")
        else:
            await ctx.send("I can't add verified role. It needs to be "
                           "lower than my top role in the hierarchy!")
# End of give_role()


# End of file
