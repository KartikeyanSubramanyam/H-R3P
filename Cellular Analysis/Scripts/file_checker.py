import os
import csv
import pandas as pd
from geopy.distance import geodesic
import numpy as np
import folium
from folium.plugins import BeautifyIcon

# Reading AHA dataset for hospitals and their respective co-ordinates
# Depending on version of python; might need to run the below command as:
# with open('2024_05_UC_San_Diego_Health.csv', 'r', encoding='utf-8-sig') as f:
with open('../Databases/2024_05_UC_San_Diego_Health.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extracting hospital name and coordinates
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]
# print(len(hospital_lat_long_df))
# print(hospital_lat_long_df)
# Clean and convert latitude/longitude to numeric
hospital_lat_long_df[['Latitude', 'Longitude']] = hospital_lat_long_df[['Latitude', 'Longitude']].apply(pd.to_numeric)
hospital_lat_long_df_cleaned = hospital_lat_long_df.dropna(subset=['Latitude', 'Longitude'])
hospital_names = df['Hospital Name'].tolist()  # Extract hospital names
# Replace spaces with underscores to match the file naming convention
hospital_names_normalized = ["".join(c if c.isalnum() else "_" for c in name) for name in hospital_names]
# print(hospital_names_normalized)


directory_path = '../Hospital_Results/'
list_of_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

missing_hospitals = []
for _, row in hospital_lat_long_df_cleaned.iterrows():
    hospital_name = row['Hospital Name']
    latitude = row['Latitude']
    longitude = row['Longitude']
    # Generate a corresponding file name based on the hospital name (adjust as needed)
    hospital_name_clean = "".join(c if c.isalnum() else "_" for c in hospital_name)
    hospital_name_clean = hospital_name_clean + ".csv"
    if hospital_name_clean not in list_of_files:
        missing_hospitals.append(hospital_name)


if missing_hospitals:
    print(f"Number of hospitals missing files: {len(missing_hospitals)}")
    for hospital in missing_hospitals:
        print(f"Missing file for hospital: {hospital}")
else:
    print("All hospitals have corresponding files.")

# Deleting extra files
# extra_files = []
# for file in list_of_files:
#     # Remove file extension (assuming it's a .csv file)
#     hospital_name_from_file = os.path.splitext(file)[0]
#     if hospital_name_from_file not in hospital_names_normalized:
#         extra_files.append(file)
#         file_path = os.path.join(directory_path, file)
#         os.remove(file_path)  # Deletes the file
#         print(f"Deleted file: {file_path}")


# if extra_files:
#     print(f"Number of files without matching hospitals: {len(extra_files)}")
#     for file in extra_files:
#         print(f"Extra file: {file}")
# else:
#     print("All files have corresponding hospitals.")