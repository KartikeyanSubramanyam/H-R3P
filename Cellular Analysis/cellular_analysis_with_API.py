import pandas as pd
import csv
from geopy.distance import geodesic
import numpy as np
import folium
from folium.plugins import BeautifyIcon
import math
import requests


def calculate_BBOX(lat, lon, distance_meters=500):
    # Constants
    delta_lat = distance_meters / 111320  # Latitude adjustment (1 degree latitude ~ 111.32 km)
    
    # Adjusting for latitude
    lat_min = lat - delta_lat
    lat_max = lat + delta_lat
    
    # Adjusting for longitude (longitude varies with latitude)
    delta_lon = distance_meters / (111320 * math.cos(math.radians(lat)))
    lon_min = lon - delta_lon
    lon_max = lon + delta_lon
    
    return lat_min, lat_max, lon_min, lon_max

def query_opencellid_and_save_csv(api_key, hospital_name, lat, lon, distance_meters=500):
    lat_min, lat_max, lon_min, lon_max = calculate_BBOX(lat, lon, distance_meters)
    
    # Format hospital name for file naming (remove spaces, special characters)
    hospital_name_clean = "".join(c if c.isalnum() else "_" for c in hospital_name)
    
    # Create a CSV filename based on the hospital name
    csv_filename = f"{hospital_name_clean}.csv"
    
    # OpenCelliD API endpoint and parameters (including format=csv)
    url = f"http://www.opencellid.org/cell/getInArea?key={api_key}&BBOX={lat_min},{lon_min},{lat_max},{lon_max}&format=csv"
    
    # Send GET request
    response = requests.get(url)
    
    if response.status_code == 200:
        # Write the response content (CSV) to a file
        with open(csv_filename, 'wb') as file:
            file.write(response.content)
        print(f"CSV file saved: {csv_filename}")
    else:
        print(f"Error: {response.status_code} for {hospital_name}")



# Reading AHA dataset for hospitals and their respective co-ordinates
# Depending on version of python; might need to run the below command as:
# with open('2024_05_UC_San_Diego_Health.csv', 'r', encoding='utf-8-sig') as f:
with open('2024_05_UC_San_Diego_Health.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extracting hospital name and coordinates
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]
print(len(hospital_lat_long_df))

# Clean and convert latitude/longitude to numeric
hospital_lat_long_df[['Latitude', 'Longitude']] = hospital_lat_long_df[['Latitude', 'Longitude']].apply(pd.to_numeric)
hospital_lat_long_df_cleaned = hospital_lat_long_df.dropna(subset=['Latitude', 'Longitude'])
print(len(hospital_lat_long_df_cleaned))


api_key = "pk.dbbe0c1c9071b2b428c86f62d8246dfa"
counter = 1
for _, row in hospital_lat_long_df_cleaned.iterrows():
    hospital_name = row['Hospital Name']
    latitude = row['Latitude']
    longitude = row['Longitude']
    print(f"Querying OpenCelliD for {hospital_name} at latitude {latitude}, longitude {longitude}...")

    # Query OpenCelliD and save the result as CSV
    query_opencellid_and_save_csv(api_key, hospital_name, latitude, longitude)
    if counter == 75:
        api_key = "pk.929ba4918140777ff0fee3a8bd532283"
    if counter == 150:
        api_key = "pk.a43267bcc74980475bbe50592e4ef781"
    if counter == 225:
        api_key = "pk.4644fdc16dd25203dc5b225d3b97fea1"
    if counter == 300:
        api_key = "pk.4e7a2c9626e45c4fdcfddde0b55fa338"
    if counter == 375: 
        api_key = "pk.57a82caf08b0555e8f58073e6b94e508"
    if counter == 450:
        api_key = "pk.48054a2b196287b93fba033641e2e869"
    if counter == 525:
        api_key = "pk.e130421224b6659d8d452b87084d7eac"
    if counter == 600:
        api_key = "pk.2c9ac7b6baf9752e8a8b82db88db80b3"
    if counter == 675:
        api_key = "pk.5e1f6108f5d5fc0b614a288a79959438"
    if counter == 750:
        break

    counter += 1

# csv_filename = "WellSpan_Surgery_and_Rehabilitation_Hospital.csv"
# lat = 39.9263
# lon = -76.719
# lat_min, lat_max, lon_min, lon_max = calculate_BBOX(lat, lon)
#     # OpenCelliD API endpoint and parameters (including format=csv)
# url = f"http://www.opencellid.org/cell/getInArea?key={api_key}&BBOX={lat_min},{lon_min},{lat_max},{lon_max}&format=csv"

# # Send GET request
# response = requests.get(url)

# if response.status_code == 200:
#     # Write the response content (CSV) to a file
#     with open(csv_filename, 'wb') as file:
#         file.write(response.content)
#     print(f"CSV file saved: {csv_filename}")
# else:
#     print(f"Error: {response.status_code} for WellSpan_Surgery_and_Rehabilitation_Hospital")
print("Process completed!")