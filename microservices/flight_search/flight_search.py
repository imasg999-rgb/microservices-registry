import os
import json
from datetime import datetime, timedelta
from serpapi import GoogleSearch
from typing import Optional, Tuple
from ratelimit import limits

FLIGHT_SEARCH_API_KEY = os.getenv("FLIGHT_SEARCH_API_KEY")


ONE_HOUR = 3600
@limits(5,ONE_HOUR)
def search_flight_serp(origin_code: str, destination_code: str, departure_date: str, return_date: str):
  params = {
    "api_key": FLIGHT_SEARCH_API_KEY,
    "engine": "google_flights",
    "hl": "en",
    "gl": "ca",
    "departure_id": origin_code,
    "arrival_id": destination_code,
    "outbound_date": departure_date,
    "return_date": return_date,
    "currency": "CAD"
  }
  search = GoogleSearch(params)
  results = search.get_dict()
  return results

def is_valid_date(date_str):
  try:
    datetime.strptime(date_str, "%Y-%m-%d")
    return True
  except ValueError:
    return False
  
def are_dates_in_order(date_a, date_b):
    fmt = "%Y-%m-%d"
    try:
        a = datetime.strptime(date_a, fmt)
        b = datetime.strptime(date_b, fmt)
    except ValueError:
        return False
    return b >= a

def search_flight(
    origin_code: str, 
    destination_code: str, 
    departure_date: str | None = None, 
    return_date: str | None = None):
  if origin_code == "TEST" or (origin_code == "YYZ" and destination_code == "AUS"):
    # Just serve a dummy API response
    with open("microservices/flight_search/data/example_data3.json") as f:
      contents = json.load(f)
    return contents
  # Check if API key and dates are valid
  if not FLIGHT_SEARCH_API_KEY:
    raise ValueError("Flight Search API key is not set")
  if not departure_date:
    departure_datetime = datetime.now()
    departure_date = departure_datetime.strftime("%Y-%m-%d")
  if not return_date:
    return_datetime = departure_datetime + timedelta(weeks=1)
    return_date = return_datetime.strftime("%Y-%m-%d")
  if departure_date and not is_valid_date(departure_date):
    raise ValueError("Invalid departure date")
  if return_date and not is_valid_date(return_date):
    raise ValueError("Invalid return date")
  if not are_dates_in_order(departure_date, return_date):
    raise ValueError("Return date is before the departure date")
  return search_flight_serp(origin_code, destination_code, departure_date, return_date)

