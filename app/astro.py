## CREATE LOCAL APP
import requests
import json
import math
import os
import skyfield as sky
import pandas as pd
from dotenv import load_dotenv

zip_code = input("Please provide your 5-digit zip code: ")
zip_code = str(zip_code)

## CREATE API CALLS
# Lat Long API Call:
load_dotenv()
google_key = os.environ.get("GOOGLE_API_KEY")
request_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + zip_code + "&key=" + google_key
response = requests.get(request_url)
parsed_response = json.loads(response.text)
lat = parsed_response["results"][0]["geometry"]["location"]["lat"]
lon = parsed_response["results"][0]["geometry"]["location"]["lng"]
location = str(lat) + "," + str(lon)

# Elevation API Call:
request_url = "https://maps.googleapis.com/maps/api/elevation/json?locations=" + location + "&key=" + google_key
response = requests.get(request_url)
parsed_response = json.loads(response.text)
elevation = parsed_response["results"][0]["elevation"]
elevation_km = round((elevation / 1000), 2) 
breakpoint()

# Weather API Call:

## IMPORT INITIAL DATA FILE AND CONVERT TO DATAFRAME

## CREATE SCORING ALGORITHM

# Variables:
tel_app = int(input("Please input the aperature (in mm) of your telescope: "))
tel_foc_len = input("Please input the focal length (in mm) of your telescope: ")
geo_loc = input("Please input your current lat/long using the following fomrat (): ")

tel_lim_vis = round(5*math.log((tel_app/6.5), 10), 2)
landscape = input("What type of environment is your observatory in? Please enter [r] for rural, [s] for suburb, or [c] for city: ")
if landscape == "r":
    nelm_max = 7.5
    nelm_min = 6.6
elif landscape == "s":
    nelm_max = 6.0
    nelm_min = 5.5
elif landscape == "c":
    nelm_max = 5.0
    nelm_min = 4.0

lim_vis_max = tel_lim_vis + nelm_max
lim_vis_min = tel_lim_vis + nelm_min
breakpoint()
## UPDATE DATAFRAME FOR SCORING CALCULATIONS AND SORT

## RETURN HUMAN READABLE ITINERARY