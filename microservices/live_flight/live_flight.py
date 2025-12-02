import os
import json
import time
import logging
import requests
from ratelimit import limits

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ADSB_API_BASE = "https://api.adsb.lol/v2"
ONE_HOUR = 3600

# Western University coordinates
WESTERN_U_LAT = 43.008701
WESTERN_U_LON = -81.263496
RADIUS_KM = 50  # 50km radius

@limits(50, ONE_HOUR)
def get_nearby_flights():
    """Get all flights within 50km of Western University using lat/lon/dist endpoint"""
    try:
        logger.info(f"Fetching flights near Western University (lat={WESTERN_U_LAT}, lon={WESTERN_U_LON}, radius={RADIUS_KM}km)")
        
        # ADSB.lol API endpoint: /v2/lat/{lat}/lon/{lon}/dist/{dist}
        url = f"{ADSB_API_BASE}/lat/{WESTERN_U_LAT}/lon/{WESTERN_U_LON}/dist/{RADIUS_KM}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract aircraft list from response
        aircraft = data.get("ac", [])
        
        result = {
            "query": f"Within {RADIUS_KM}km of Western University",
            "results": aircraft,
            "count": len(aircraft),
            "location": {
                "lat": WESTERN_U_LAT,
                "lon": WESTERN_U_LON,
                "radius_km": RADIUS_KM
            }
        }
        
        logger.info(f"Found {len(aircraft)} flights near Western University")
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching nearby flights: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching nearby flights: {str(e)}")
        raise

@limits(50, ONE_HOUR)
def search_flight(callsign: str):
    """Search for a specific flight by callsign using ADSB.lol API"""
    callsign = callsign.upper().strip()
    
    try:
        logger.info(f"Searching for flight: {callsign}")
        
        # ADSB.lol API endpoint: /v2/callsign/{callsign}
        url = f"{ADSB_API_BASE}/callsign/{callsign}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract aircraft list from response
        aircraft = data.get("ac", [])
        
        if not aircraft:
            logger.warning(f"No flights found for callsign: {callsign}")
            return {
                "query": callsign,
                "results": [],
                "count": 0,
                "error": f"No flights found matching callsign '{callsign}'"
            }
        
        result = {
            "query": callsign,
            "results": aircraft,
            "count": len(aircraft)
        }
        
        logger.info(f"Found {len(aircraft)} flight(s) for callsign: {callsign}")
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching for flight {callsign}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error searching for flight {callsign}: {str(e)}")
        raise