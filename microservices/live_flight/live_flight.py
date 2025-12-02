import os
import json
import time
from datetime import datetime, timedelta
from ratelimit import limits
import logging
import requests

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPEN_SKY_URL = "https://opensky-network.org/api/states/all"
OPEN_SKY_AUTH_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
CLIENT_ID = os.getenv("OPEN_SKY_CLIENT_ID")
CLIENT_SECRET = os.getenv("OPEN_SKY_CLIENT_SECRET")
ONE_HOUR = 3600

# Token cache to avoid getting a new token for every request
_token_cache = {
    "access_token": None,
    "expires_at": None
}

def get_access_token():
    """Get a valid OAuth2 access token, using cache if still valid."""
    logger.info(f"Attempting to get token from {OPEN_SKY_AUTH_URL}")
    logger.info(f"CLIENT_ID set: {bool(CLIENT_ID)}")
    logger.info(f"CLIENT_SECRET set: {bool(CLIENT_SECRET)}")

    # Check if we have a valid cached token
    if _token_cache["access_token"] and _token_cache["expires_at"]:
        if datetime.now() < _token_cache["expires_at"]:
            logger.info("Using cached token")
            return _token_cache["access_token"]
        else:
            logger.info("Cached token expired")
    
    # Need to get a new token
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("OPEN_SKY_CLIENT_ID and OPEN_SKY_CLIENT_SECRET must be set in environment variables")
    
    logger.info(f"Getting token from: {OPEN_SKY_AUTH_URL}")
    try:
        response = requests.post(
            OPEN_SKY_AUTH_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            },
            timeout=30 # increased the timeout incase
        )
        logger.info(f"Auth response status code: {response.status_code}")
        logger.info(f"Auth response headers: {dict(response.headers)}")

        try:
            response_json = response.json()
            logger.info(f"Auth response body keys: {list(response_json.keys())}")
            if 'error' in response_json:
                logger.error(f"Auth error: {response_json.get('error')}")
                logger.error(f"Auth error description: {response_json.get('error_description')}")
        except Exception as e:
            logger.error(f"Could not parse response as JSON: {e}")
            logger.error(f"Response text: {response.text[:500]}")

        response.raise_for_status()
        
        token_data = response.json()

        if "access_token" not in token_data:
            raise ValueError(f"No access_token in response. Keys: {list(token_data.keys())}")

        access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 1800)  # Default 30 minutes
        
        logger.info(f"Successfully obtained token, expires in {expires_in} seconds")
        
        # Cache the token with a buffer
        _token_cache["access_token"] = access_token
        _token_cache["expires_at"] = datetime.now() + timedelta(seconds=expires_in - 60) # expire 1 minute early to be safe
        
        return access_token
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout connecting to auth server: {e}")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error to auth server: {e}")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error from auth server: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting token: {e}", exc_info=True)
        raise

@limits(50,ONE_HOUR)
def search_flight(flight_number: str):
    flight_number = flight_number.upper().strip()

    # Get valid access token
    access_token = get_access_token()

    # Make API request with Bearer token
    response = requests.get(
        OPEN_SKY_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10
    )
    response.raise_for_status()
    
    data = response.json()
    states = data.get("states", [])

    # Each state entry structure (indices):
    # 0: icao24 (aircraft ID)
    # 1: callsign (flight number)
    # 2: origin_country
    # 3: time_position
    # 4: last_contact
    # 5: longitude
    # 6: latitude
    # 7: baro_altitude
    # 8: on_ground
    # 9: velocity
    # 10: true_track (heading)
    # 11: vertical_rate

    matches = [s for s in states if s[1] and (flight_number.upper() or flight.number.lower()) in s[1].strip()]
    # matches = states[:10]

    result = {
        "query": flight_number,
        "results": matches,
        "count": len(matches),
    }

    return result