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




api_key = "pk.929ba4918140777ff0fee3a8bd532283"
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

counter = 0
for _, row in hospital_lat_long_df_cleaned.iterrows():
    hospital_name = row['Hospital Name']
    latitude = row['Latitude']
    longitude = row['Longitude']
    
    print(f"Querying OpenCelliD for {hospital_name} at latitude {latitude}, longitude {longitude}...")
    
    # Query OpenCelliD and save the result as CSV
    query_opencellid_and_save_csv(api_key, hospital_name, latitude, longitude)
    counter += 1
    if counter == 995:
        break
    


print("Process completed!")