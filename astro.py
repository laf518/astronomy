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

print()
print("Welcome to Astronomy Scheduler!")
print("------------------------------")
print()
print("Please provide the following information to help us maximize your experience:")
print()
# Validate user input:
while True:
    try:
        zip_code = int(input("Please input your 5-digit zip code: "))
        if len(str(zip_code)) == 5:
            zip_code = str(zip_code)
            break
        else:
            print("Hmmm...Looks like we don't have the correct number of characters.  Let's try again!")
            print()
    except ValueError:
        print("Input contained non-numeric characters.  Please try again...")
        print()

# ## CREATE API CALLS
# # Lat Long API Call:
load_dotenv()
google_key = os.environ.get("GOOGLE_API_KEY")
request_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + zip_code + "&key=" + google_key
response = requests.get(request_url)
parsed_response = json.loads(response.text)
lat = parsed_response["results"][0]["geometry"]["location"]["lat"]
if lat < 0:
    lat_card = "S"
else:
    lat_card = "N"
lon = parsed_response["results"][0]["geometry"]["location"]["lng"]
if lon < 0:
    lon_card = "W"
else:
    lon_card = "E"
location = str(lat) + "," + str(lon)

# Elevation API Call:
request_url = "https://maps.googleapis.com/maps/api/elevation/json?locations=" + location + "&key=" + google_key
response = requests.get(request_url)
parsed_response = json.loads(response.text)
elevation = parsed_response["results"][0]["elevation"]
elevation_km = round((elevation / 1000), 2) 

## Find Sunrise / Sunset of requested date:
# Validate input:

while True:
    try:
        date = input("When do plan to conduct your observation? (yyyy mm dd): ")
        test = date.split()
        test = [int(i) for i in  test]
        if len(str(test[0])) == 4 and len(str(test[1])) <= 2 and len(str(test[2])) <= 2 and len(test) == 3:
            break
        else:
            print("Hmmm...there appears to be something wrong with your formatting.  Please try again.")
            print()
    except ValueError:
        print("Non-numeric characters detected. Please try again")
        print()
    
y = int(date[0:4])
m = int(date[5:7])
day = int(date[8:10])

request_url = "https://maps.googleapis.com/maps/api/timezone/json?location=" + location + "&timestamp=1458000000&key=" + google_key
response = requests.get(request_url)
parsed_response = json.loads(response.text)
raw_offset = parsed_response["rawOffset"] / 3600
dst_offset = parsed_response["dstOffset"] / 3600
tot_offset = raw_offset + dst_offset

ts = api.load.timescale(builtin=True)
eph = api.load('de421.bsp')
earth = eph['earth']
obs_city = api.Topos(str(abs(lat)) + " " + lat_card, str(abs(lon)) + " " + lon_card)

t0 = ts.utc(y, m, day, 12 - tot_offset) #>UTC Time
t1 = ts.utc(y, m, day + 1, 12 - tot_offset) #>UTC Time
t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, obs_city))

adjust = (tot_offset * 60) / 24 / 60
sunset_sunrise = ts.tt_jd(t.tt + adjust)
sunset_sunrise = sunset_sunrise.utc_iso()
sunset_raw = sunset_sunrise[0]
sunrise_raw = sunset_sunrise[1]

sunset_hour = int(sunset_raw[11:13] + "00")
sunrise_hour = int(sunrise_raw[11:13] + "00")

## IMPORT INITIAL DATA FILE AND CONVERT TO Multi-Indexed DATAFRAME
# CREDIT: https://stackoverflow.com/questions/53286882/how-to-reindex-a-multiindex-dataframe

df = pd.read_csv("./data/sample_program.csv")
df = df.set_index('Object')

x = t[0].tt + .042
c = t[1].tt - .042
z = np.arange(x, c, .042).tolist()


object_list = df.index.tolist()
iterables = [z, object_list]

sub_index = pd.MultiIndex.from_product(iterables, names=['Local Time', 'Object'])
df_x = pd.DataFrame(np.random.randint(10, 25, len(z)*len(object_list)), sub_index)

df = pd.concat([df]*len(z), keys=df_x.index.levels[0])
df = df.reset_index()

# Create new column to calculate z-angle:
new = df['Right Ascention'].str.split(" ", expand = True)
df['RA Hour'] = new[0].astype('int64')
df['RA Min'] = new[1].astype('int64')
df['RA Sec'] = new[2].astype('float')

new = df['Declination'].str.split(" ", expand = True)
df['DC Deg'] = new[0].astype('int64')
df['DC ArcM'] = new[1].astype('int64')
df['DC ArcS'] = new[2].astype('float')

city = earth + obs_city

# Conduct Additional Table Based Calculations
def star_x(row):
    return api.Star(ra_hours = (row['RA Hour'], row['RA Min'], row['RA Sec']), dec_degrees = (row['DC Deg'], row['DC ArcM'], row['DC ArcS']))

df['StarX'] = df.apply(star_x, axis=1)

def astro(row):
    return city.at(ts.tt_jd(row['Local Time'])).observe(row['StarX'])

df['Astro'] = df.apply(astro, axis =1)

def appar(row):
    return row['Astro'].apparent()

df['Apparent'] = df.apply(appar, axis =1)
# df['app'] = df['astro'].apparent()

def alt(row):
    alt, az, distance = row['Apparent'].altaz()
    return alt.dstr()

df['Alt'] = df.apply(alt, axis =1)

df['Z_Angle'] = df.apply(lambda row: 90 - int(row['Alt'][0:len(row['Alt'])-13]), axis =1)
df.drop(df[df.Z_Angle >= 90].index, inplace=True)

## CREATE SCORING ALGORITHM

# Variables:
# Validate user input:

while True:
    try:
        tel_app = int(input("Please input the aperature (in mm) of your telescope: "))
        if len(str(tel_app)) <= 4:
            break
        else:
            print("Let's check that number again...")
            print()
    except ValueError:
        print("Non-numeric characters detected. Try again.")
        print()

tel_lim_vis = round(5*math.log((tel_app/6.5), 10), 2)

# Validate user input:
while True:    
    landscape = input("Finally, what type of environment is your observatory in? Please enter [r] for rural, [s] for suburb, or [c] for city: ")
    if landscape.lower() == "r":
        nelm_max = 7.5
        nelm_min = 6.6
        break
    elif landscape.lower() == "s":
        nelm_max = 6.0
        nelm_min = 5.5
        break
    elif landscape.lower() == "c":
        nelm_max = 5.0
        nelm_min = 4.0
        break
    else:
        print("Invalid input.  Try again.")
        print()

    


lim_vis_max = tel_lim_vis + nelm_max
lim_vis_min = tel_lim_vis + nelm_min

ray_scatter = .1451 * math.exp(-elevation_km / 7.996)
aero = .12 * math.exp(-elevation_km / 1.5)

def score(row):
    air_mass = 1/(math.cos(row['Z_Angle'])+.025*math.exp(-11*math.cos(row['Z_Angle'])))
    lim_mag = lim_vis_min - air_mass * (ray_scatter + aero * 1.2)
    
    return float(row['Apparent Magnitude'] - lim_mag)
df['Score'] = df.apply(score, axis = 1)


# ## UPDATE DATAFRAME FOR SCORING CALCULATIONS AND SORT
df_score = df[['Local Time', 'Object', 'Z_Angle', 'Score']].copy()

def local_time(row):
    tx = ts.tt_jd(row['Local Time'])
    ty = (ts.tt_jd(tx.tt + tot_offset / 24)).utc.hour
    tz = (ts.tt_jd(tx.tt +tot_offset / 24)).utc.minute

    return str(ty) + ":" +str(tz)

df_score.drop(df_score[df_score.Score > lim_vis_max].index, inplace=True)
df_score = df_score.sort_values(by=['Score'])
df_score = df_score.drop_duplicates(subset='Local Time', keep='first')
df_score = df_score.sort_values(by=['Local Time'])
df_score['Local Time'] = df.apply(local_time, axis = 1)


df_score = df_score.drop_duplicates(subset='Object', keep='first')



# ## RETURN HUMAN READABLE ITINERARY
print()
print("Best Objects and Viewing Times:")
print("------------------------------")
print(df_score.to_string(index=False))
print()
print("Happy Viewing!")
print()

## CREDIT:  All formulas are from www.stjarnhimlen.se/comp/ppcomp.html
## Third Party Package: http://rhodesmill.org/skyfield/