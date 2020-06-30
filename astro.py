## CREATE LOCAL APP
import requests
import json
import math
import os
import skyfield as sky
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from skyfield import api, almanac

# zip_code = input("Please provide your 5-digit zip code: ")
# zip_code = str(zip_code)

# ## CREATE API CALLS
# # Lat Long API Call:
# load_dotenv()
# google_key = os.environ.get("GOOGLE_API_KEY")
# request_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + zip_code + "&key=" + google_key
# response = requests.get(request_url)
# parsed_response = json.loads(response.text)
# lat = parsed_response["results"][0]["geometry"]["location"]["lat"]
# if lat < 0:
#     lat_card = "S"
# else:
#     lat_card = "N"
# lon = parsed_response["results"][0]["geometry"]["location"]["lng"]
# if lon < 0:
#     lon_card = "W"
# else:
#     lon_card = "E"
# location = str(lat) + "," + str(lon)

# # # # Elevation API Call:
# request_url = "https://maps.googleapis.com/maps/api/elevation/json?locations=" + location + "&key=" + google_key
# response = requests.get(request_url)
# parsed_response = json.loads(response.text)
# elevation = parsed_response["results"][0]["elevation"]
# elevation_km = round((elevation / 1000), 2) 

# # ## Find Sunrise / Sunset of requested date:
# date = input("What date do plan to conduct your observation? (yyyy mm dd): ")
# y = int(date[0:4])
# m = int(date[5:7])
# d = int(date[8:10])

# request_url = "https://maps.googleapis.com/maps/api/timezone/json?location=" + location + "&timestamp=1458000000&key=" + google_key
# response = requests.get(request_url)
# parsed_response = json.loads(response.text)
# raw_offset = parsed_response["rawOffset"] / 3600
# dst_offset = parsed_response["dstOffset"] / 3600
# tot_offset = raw_offset + dst_offset

# ts = api.load.timescale(builtin=True)
# eph = api.load('de421.bsp')
# obs_city = api.Topos(str(abs(lat)) + " " + lat_card, str(abs(lon)) + " " + lon_card)

# t0 = ts.utc(y, m, d, 12 - tot_offset)
# t1 = ts.utc(y, m, d + 1, 12 - tot_offset)
# t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, obs_city))

# adjust = (tot_offset * 60) / 24 / 60
# sunset_sunrise = ts.tt_jd(t.tt + adjust)
# sunset_sunrise = sunset_sunrise.utc_iso()
# sunset_raw = sunset_sunrise[0]
# sunrise_raw = sunset_sunrise[1]

# sunset_hour = int(sunset_raw[11:13] + "00")
# sunrise_hour = int(sunrise_raw[11:13] + "00")

## IMPORT INITIAL DATA FILE AND CONVERT TO Multi-Indexed DATAFRAME
df = pd.read_csv("./data/sample_program.csv")
df = df.set_index('Object')
time_range = ['1900', '2000', '2100', '2200', '2300', '0000', '0100', '0200', '0300', '0400', '0500']
object_list = df.index.tolist()
breakpoint()
iterables = [time_range, object_list]

sub_index = pd.MultiIndex.from_product(iterables, names=['Local Time', 'Object'])
df_x = pd.DataFrame(np.random.randint(10, 25, len(time_range)*len(object_list)), sub_index)

df = pd.concat([df]*len(time_range), keys=df_x.index.levels[0])
breakpoint()

# ## CREATE SCORING ALGORITHM

# # Variables:
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
# ## UPDATE DATAFRAME FOR SCORING CALCULATIONS AND SORT

# ## RETURN HUMAN READABLE ITINERARY