import pandas as pd
import csv
from geopy.distance import geodesic
import numpy as np
import folium



# Reading AHA dataset for hospitals and their respective co-ordinates
# Depending on version of python; might need to run the below command as:
# with open('2024_05_UC_San_Diego_Health.csv', 'r', encoding='utf-8-sig') as f:
with open('2024_05_UC_San_Diego_Health.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extracting only the hospital name and coords
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]
print(hospital_lat_long_df)

hospital_coords = hospital_lat_long_df[['Latitude', 'Longitude']].values
hospital_coords_df = pd.DataFrame(hospital_coords, columns=['Latitude', 'Longitude'])
hospital_names = hospital_lat_long_df['Hospital Name'].values
print(hospital_names)
print(hospital_names[1])

# Convert the columns to numeric (floats)
# hospital_coords_df['Latitude'] = pd.to_numeric(hospital_coords_df['Latitude'])
# hospital_coords_df['Longitude'] = pd.to_numeric(hospital_coords_df['Longitude'], errors='coerce')


hospital_coords_df = hospital_coords_df.apply(pd.to_numeric)
hospital_coords_df_cleaned = hospital_coords_df.dropna(subset=['Latitude', 'Longitude'])
print(len(hospital_coords_df_cleaned))
# Split the DataFrame into 4 parts
df_split = np.array_split(hospital_lat_long_df, 4)

# Access each part
df1 = df_split[0]
df2 = df_split[1]
df3 = df_split[2]
df4 = df_split[3]

# Print the individual DataFrames
# print("DataFrame 1:\n", df1)
# print("DataFrame 2:\n", df2)
# print("DataFrame 3:\n", df3)
# print("DataFrame 4:\n", df4)


# Extracting OpenCellID Data (7 different files for 310-316 MCC)
column_names = ['Radio Gen.', 'MCC', 'MNC', 'LAC', 'CID', 'X', 'Longitude', 'Latitude', 'Range', 'Samples', 'Changeable', 'Created', 'Updated', 'Average Signal']
celldata310 = pd.read_csv('310.csv.gz', compression='gzip', header=None, names=column_names)
celldata311 = pd.read_csv('311.csv.gz', compression='gzip', header=None, names=column_names)
celldata312 = pd.read_csv('312.csv.gz', compression='gzip', header=None, names=column_names)
celldata313 = pd.read_csv('313.csv.gz', compression='gzip', header=None, names=column_names)
celldata314 = pd.read_csv('314.csv.gz', compression='gzip', header=None, names=column_names)
celldata315 = pd.read_csv('315.csv.gz', compression='gzip', header=None, names=column_names)
celldata316 = pd.read_csv('316.csv.gz', compression='gzip', header=None, names=column_names)


# print(celldata310)
# print(len(celldata311))
# print(len(celldata312))
# print(len(celldata313))
# print(len(celldata314))
# print(len(celldata315))
# print(len(celldata316))

print(len(celldata310)+len(celldata311)+len(celldata312)+len(celldata313)+len(celldata314)+len(celldata315)+len(celldata316))

combined_celldata = [celldata310, celldata311, celldata312, celldata313, celldata314, celldata315, celldata316]
celldata = pd.concat(combined_celldata, ignore_index=True)

# print(celldata)
# lengths for separate and concatenated match
print(len(celldata))

filtered_by_range_df = celldata[celldata.iloc[:, 8] <= 15000]
print(len(filtered_by_range_df))
fin_celldata = filtered_by_range_df[filtered_by_range_df.iloc[:, 9] > 2]
print(len(fin_celldata))
# print(fin_celldata)

# Create a map centered at a specific latitude and longitude
my_map = folium.Map(location=[39.8097, 98.5556], zoom_start=1)

looprun = 0
for idx, hospital_coord in enumerate(hospital_coords_df_cleaned.iterrows()):
    print(hospital_coord[1]['Latitude'])
    print(hospital_coord[1]['Longitude'])
    if idx == 0:  # Skip the first row
        continue
    # Add a marker for each valid coordinate
    folium.Marker([hospital_coord[1]['Latitude'], hospital_coord[1]['Longitude']], popup=hospital_names[looprun]).add_to(my_map)
    looprun += 1

# # Display the map
my_map.save("HospitalsMap.html")


