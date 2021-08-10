# Import standard library dependencies
import json


async def is_verification_successful(ctx, user_data, random_uuid) -> bool:
    """
    Check the first line of description.
    If the first line has random_uuid, it is verified.
    """

    # The description is also a json
    description = json.loads(user_data["description"])
    first_line = description["sections"][0]["spans"][0]["text"].strip(" ")

    if first_line == random_uuid:
        await ctx.send("Successfully verified!")
        return True
    else:
        await ctx.send("Code not found. Verification failed!")
        await ctx.send("The first line of your description is:\n"
                       f"```{first_line}```")
        return False
# End of is_verification_successful()


# End of file
