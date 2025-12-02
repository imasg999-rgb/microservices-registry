import os
import json
# do i need any other imports??

import requests


def forcast(city: str, country: str):

    # get coordingates of location
    coords = _get_coords(city, country)

    # check if no results were returned
    if coords is None:
        print(f"{city} was not found in {country}.")
        return None
        
    lat, lon = coords # seperate latitude and longitude from coords

    weather_url = "https://api.open-meteo.com/v1/forecast" # URL for forecast api endopoint
    
    # define parameters
    params = {
        "latitude": lat, 
        "longitude": lon, 
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum", # get the min and max temp for each day, aswell as the daily precipitation
        "forecast_days": 14, # get the forecast for 2 weeks
        "timezone": "auto"
    }

    resp = requests.get(weather_url, params=params) # get response from api, which should be the forecast
    resp.raise_for_status() # throw exception if HTTP fails

    return resp.json()



# helper function; Get coordinates (latitude and longitude) for a given city and country
def _get_coords(city: str, country: str):
    url = "https://geocoding-api.open-meteo.com/v1/search" # URL for coords api endpoint

    # set parameters city and country
    params = {
        "name": city,
        "country": country
    }
    
    response = requests.get(url, params=params) # get response from api, which should be the coordinates
    response.raise_for_status() # throw exception if HTTP fails

    results = response.json().get("results") # get the results from the returned JSON

    # check if result was empty
    if not results:
        return None
    
    top = results[0] # get the top result returned

    return top["latitude"], top["longitude"] # return coords
