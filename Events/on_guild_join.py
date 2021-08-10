# Import external dependencies
import aiosqlite

# Import discord.py stuff
import discord


async def set_up_guild(guild: discord.Guild):
    """Create DB on join"""

    SQL_CMD_USERS = """
        CREATE TABLE IF NOT EXISTS users (
            discord_uid         INTEGER    NOT NULL,
            quora_uid           INTEGER    NOT NULL,
            quora_name          TEXT       NOT NULL    DEFAULT "Gumnaam",
            quora_profile       TEXT       NOT NULL    DEFAULT "no-profile",
            PRIMARY KEY (discord_uid, quora_uid)
        );
    """

    SQL_CMD_SETTINGS = """
        CREATE TABLE IF NOT EXISTS settings (
            setting    TEXT       NOT NULL   PRIMARY KEY,
            value      INTEGER    NOT NULL   DEFAULT 0
        );
    """

    # Connection will make new db if not already existing
    conn = await aiosqlite.connect(f"./Database/{guild.id}.db")
    await conn.execute(SQL_CMD_USERS)
    await conn.execute(SQL_CMD_SETTINGS)
    await conn.commit()    # Commit the transaction

    # Close connection
    await conn.close()
# End of set_up_guild()


# End of file
