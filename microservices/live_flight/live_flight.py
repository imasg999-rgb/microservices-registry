import os
import json
import time
from datetime import datetime, timedelta
from ratelimit import limits
import requests


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
    # Check if we have a valid cached token
    if _token_cache["access_token"] and _token_cache["expires_at"]:
        if datetime.now() < _token_cache["expires_at"]:
            return _token_cache["access_token"]
    
    # Need to get a new token
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("OPEN_SKY_CLIENT_ID and OPEN_SKY_CLIENT_SECRET must be set in environment variables")
    
    response = requests.post(
        OPEN_SKY_AUTH_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        },
        timeout=10
    )
    response.raise_for_status()
    
    token_data = response.json()
    access_token = token_data["access_token"]
    expires_in = token_data.get("expires_in", 1800)  # Default 30 minutes
    
    # Cache the token with a buffer (expire 1 minute early to be safe)
    _token_cache["access_token"] = access_token
    _token_cache["expires_at"] = datetime.now() + timedelta(seconds=expires_in - 60)
    
    return access_token

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