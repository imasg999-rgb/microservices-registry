import logging
import requests

logger = logging.getLogger(__name__)

WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"


class DestinationError(Exception):
    pass


def get_destination_description(name: str, country: str | None = None) -> dict:
    if not name:
        raise ValueError("Destination name is required.")

    title = name.strip()
    url = WIKI_SUMMARY_URL.format(title=title)

    logger.info("Requesting Wikipedia summary for URL: %s", url)

    # Required by Wikimedia API
    headers = {
        "User-Agent": "TravelWishlistApp/1.0 (student project; contact@example.com)"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        logger.info("API status=%s", resp.status_code)
        logger.debug("API response preview: %s", resp.text[:200])
    except requests.RequestException as e:
        logger.exception("Network error calling Wikipedia")
        raise DestinationError("Failed to contact destination provider.") from e

    if resp.status_code != 200:
        logger.error("API returned status %s for %s", resp.status_code, title)
        raise DestinationError("Destination not found.")

    data = resp.json()

    description = data.get("extract") or data.get("description")
    if not description:
        logger.warning("No description fields in Wikipedia response: %s", data)
        description = f"Information about {title}."

    image_url = None

    thumbnail = data.get("thumbnail")
    if isinstance(thumbnail, dict):
        image_url = thumbnail.get("source")

    if not image_url:
        originalimage = data.get("originalimage")
        if isinstance(originalimage, dict):
            image_url = originalimage.get("source")

    return {
        "name": name,
        "country": country,
        "description": description,
        "image_url": image_url,
    }
