import pandas as pd
import csv
from geopy.distance import geodesic
import numpy as np
import folium
from folium.plugins import BeautifyIcon




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
print(hospital_lat_long_df)
# Clean and convert latitude/longitude to numeric
hospital_lat_long_df[['Latitude', 'Longitude']] = hospital_lat_long_df[['Latitude', 'Longitude']].apply(pd.to_numeric)

with open('unfounded.txt', 'r') as file:
    hospital_names = [line.strip() for line in file.readlines()]
print(hospital_names)


for index, row in hospital_lat_long_df.iterrows():
    if row['Hospital Name'] in hospital_names:
        print(f"Hospital: {row['Hospital Name']}, Latitude: {row['Latitude']}, Longitude: {row['Longitude']}")


hospital_lat_long_df_cleaned = hospital_lat_long_df.dropna(subset=['Latitude', 'Longitude'])
print(len(hospital_lat_long_df_cleaned))
# Extracting only the hospital name and coords
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]
print(hospital_lat_long_df)

# hospital_coords = hospital_lat_long_df[['Latitude', 'Longitude']].values
# hospital_coords_df = pd.DataFrame(hospital_coords, columns=['Latitude', 'Longitude'])
# hospital_names = hospital_lat_long_df['Hospital Name'].values
# print(hospital_names)
# print(hospital_names[5765])
# print(hospital_coords[5765][0])


# Convert the columns to numeric (floats)
# hospital_coords_df['Latitude'] = pd.to_numeric(hospital_coords_df['Latitude'])
# hospital_coords_df['Longitude'] = pd.to_numeric(hospital_coords_df['Longitude'], errors='coerce')


# # Extracting OpenCellID Data (7 different files for 310-316 MCC)
# column_names = ['Radio Gen.', 'MCC', 'MNC', 'LAC', 'CID', 'X', 'Longitude', 'Latitude', 'Range', 'Samples', 'Changeable', 'Created', 'Updated', 'Average Signal']
# celldata310 = pd.read_csv('310.csv.gz', compression='gzip', header=None, names=column_names)
# celldata311 = pd.read_csv('311.csv.gz', compression='gzip', header=None, names=column_names)
# celldata312 = pd.read_csv('312.csv.gz', compression='gzip', header=None, names=column_names)
# celldata313 = pd.read_csv('313.csv.gz', compression='gzip', header=None, names=column_names)
# celldata314 = pd.read_csv('314.csv.gz', compression='gzip', header=None, names=column_names)
# celldata315 = pd.read_csv('315.csv.gz', compression='gzip', header=None, names=column_names)
# celldata316 = pd.read_csv('316.csv.gz', compression='gzip', header=None, names=column_names)

# # worldwidecelldata = pd.read_csv('cell_towers.csv.gz', compression='gzip', header=None, names=column_names)
# # match_worldwide = worldwidecelldata[worldwidecelldata['CID'] == 63087362]
# # print(match_worldwide)
# print(celldata310)
# print(len(celldata311))
# print(len(celldata312))
# print(len(celldata313))
# print(len(celldata314))
# print(len(celldata315))
# print(len(celldata316))

# match_311 = celldata311[celldata311['CID'] == 63087362]
# print(len(celldata310)+len(celldata311)+len(celldata312)+len(celldata313)+len(celldata314)+len(celldata315)+len(celldata316))

# combined_celldata = [celldata310, celldata311, celldata312, celldata313, celldata314, celldata315, celldata316]
# celldata = pd.concat(combined_celldata, ignore_index=True)
# # print(celldata[15])
# celldata_coords = celldata.iloc[:, [7, 6]].values

# print(match_311)

# # x = geodesic((hospital_coords[5765][0], hospital_coords[5765][1]), (38.681831, -121.157913)).kilometers
# # print(x * 1000)
# filtered_by_range_df = celldata[celldata.iloc[:, 8] <= 15000]
# print(len(filtered_by_range_df))
# fin_celldata = filtered_by_range_df[filtered_by_range_df.iloc[:, 9] > 2]
# print(len(fin_celldata))
