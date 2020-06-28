## CREATE LOCAL APP
import math
## CREATE API CALLS
#CELESTIAL_COORD_API

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