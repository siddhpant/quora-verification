# Import standard library dependencies
from urllib.parse import urlparse

# Import external dependencies
import aiohttp


async def valid_profile_link(profile, header) -> bool:
    """Check if the URL is of the correct form."""

    parsed_url = urlparse(profile)

    if parsed_url.scheme != "https":
        if not parsed_url.scheme:  # Empty string
            parsed_url = parsed_url._replace(scheme='https')
        else:
            return False

    if parsed_url.netloc not in ("www.quora.com", "qr.ae"):
        return False

    if parsed_url.netloc == "qr.ae":
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(profile) as response:
                if response.status == 200:
                    parsed_url = urlparse(response.url)
                else:
                    return False

    # Now check the quora.com link. Valid path is "/quora/<name>"

    path_components = parsed_url.path.split("/")

    return len(path_components) == 3 and path_components[1] == "profile"
# End of valid_profile_link()


# End of file
