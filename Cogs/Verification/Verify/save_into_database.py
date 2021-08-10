# Import external dependencies
import aiosqlite


async def save_data(ctx, user_data):
    """Give the access role (set by guild) on verification."""

    SQL_CMD_INS = "INSERT OR IGNORE INTO users VALUES (?,?,?,?);"

    insert_tuple = (
        ctx.author.id,  # Discord user ID
        user_data["uid"],  # Quora user ID
        (user_data["names"][0]["givenName"] + " "
         + user_data["names"][0]["familyName"]),  # Name
        user_data["profileUrl"]  # Quora profile link (w/o domain)
    )

    # Open database and execute query
    try:
        conn = await aiosqlite.connect(f"./Database/{ctx.guild.id}.db")
        await conn.execute(SQL_CMD_INS, insert_tuple)
    except aiosqlite.OperationalError:
        await ctx.send("There's a problem with this server setting's database."
                       "\nPlease use `set_role` command to fix it.")
        raise
    else:
        await conn.commit()
    finally:
        await conn.close()
# End of save_data()


# End of file
