# Astronomy Scheduler
This program provides a concise, optimized itinerary to help amateur astronomers explore deep colestial objects in the cosmos. 
## Getting Started
---
This program requires Python  version 3.7. Users are encouraged to create a virtual evnironment with the following code:
>`conda create -n astronomy_env python=3.7`

>`conda activate astronomy_env`

Required third party packages are provided below and are also listed in the *requirements.txt* document included in this repository.
### Prerequisites
* Required third party packages include:
    * *pandas*
    * *numpy*
    * *requests*
    * *math*
    * *skyfield*
    * *python-dotenv*
### Installingpi
* The user will be required to clone the repository located at the following hyperlink: https://github.com/laf518/astronomy. 
* Once the user has finished setting up their local repository, they must run the following code within their virtual Python environment to install the required third party packages:
>`pip install -r requirements.txt`
* Finally, users will need to create a .env file with the following API variables:
>`WEATHER_API_KEY = [insert API key]`

>`GOOGLE_API_KEY = [insert API key]`
## Deployment
---
* All data files are packaged within the reqpository, updates will be made frequently.  Users will be prompted to input basic information regarding site location and equipment specifications. The program will then print an itinerary of the best viewing times and opportunities for specific deep celestial objects. 

### Errors:
* User will be prompted to correct input errors.

## Author
---
* **Luke Fellin** - *Programming in Python and Fundamentals of Software Development: **NYU Stern School of Business**, Summer 2020