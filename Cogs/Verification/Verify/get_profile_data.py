# Import standard library dependencies
import json

# Import external dependencies
import aiohttp
from bs4 import BeautifulSoup


async def get_profile_data(ctx, profile, header) -> dict:
    """Return the user's data dict from a profile."""

    try:
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(profile) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), "lxml")
                else:
                    await ctx.send("Cannot fetch data from the supplied URL."
                                   f"\n({response.status} {response.reason})")
                    return
    except Exception as e:
        await ctx.send(f"An error occured!\n```{e}```")
        raise

    # Profile's HTML has a json/dict in a variable in one of the js script.
    # Thus, we will extract the data from that dict.
    # Single quotes delimitation here as double quotes in string.
    valid_line = (
        'window.ansFrontendGlobals.data.inlineQueryResults.results["',
        # Actually it's like win....results["<some_id_here>"] = "{\\"data...
        '"] = "{\\"data\\":{\\"user\\":{\\"id\\":'
    )

    user_data = None

    for line in soup.prettify().split('\n'):
        # len(valid_line[0] == 59, and len(valid_line[1]) == 34
        # There's a 64 character key (for the js var) between the two strings.
        # 59 + 64 = 123
        if line[:59] == valid_line[0] and line[123:][:34] == valid_line[1]:
            # The '"] = ' are extra 5 characters before the dict; 123 + 5 = 128
            # -1 to remove the statement terminating semicolon of js.
            user_data = json.loads(json.loads((line[128:-1])))
            break

    return user_data["data"]["user"]
# End of get_profile_data()


# End of file
