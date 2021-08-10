# Import discord.py stuff
from discord.ext import commands

# Import the commands
from .Config.config import set_role
from .Verify.verify import verify


class Verification(commands.Cog):
    """Commands related to verifying social media accounts"""

    # Initialise the cog class
    def __init__(self, bot):
        self.bot = bot
    # End of __init__()

    # Bring functions into class scope by way of assignment
    verify = verify
    set_role = set_role
# End of Verification class


def setup(bot):
    bot.add_cog(Verification(bot))
# End of setup


# End of file
