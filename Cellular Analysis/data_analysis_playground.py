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

# Extracting only the hospital name and coords
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]
print(hospital_lat_long_df)

hospital_coords = hospital_lat_long_df[['Latitude', 'Longitude']].values
hospital_coords_df = pd.DataFrame(hospital_coords, columns=['Latitude', 'Longitude'])
hospital_names = hospital_lat_long_df['Hospital Name'].values
print(hospital_names)
print(hospital_names[5765])
print(hospital_coords[5765][0])


# Convert the columns to numeric (floats)
# hospital_coords_df['Latitude'] = pd.to_numeric(hospital_coords_df['Latitude'])
# hospital_coords_df['Longitude'] = pd.to_numeric(hospital_coords_df['Longitude'], errors='coerce')


hospital_coords_df = hospital_coords_df.apply(pd.to_numeric)
hospital_coords_df_cleaned = hospital_coords_df.dropna(subset=['Latitude', 'Longitude'])
print(len(hospital_coords_df_cleaned))




# Extracting OpenCellID Data (7 different files for 310-316 MCC)
column_names = ['Radio Gen.', 'MCC', 'MNC', 'LAC', 'CID', 'X', 'Longitude', 'Latitude', 'Range', 'Samples', 'Changeable', 'Created', 'Updated', 'Average Signal']
celldata310 = pd.read_csv('310.csv.gz', compression='gzip', header=None, names=column_names)
celldata311 = pd.read_csv('311.csv.gz', compression='gzip', header=None, names=column_names)
celldata312 = pd.read_csv('312.csv.gz', compression='gzip', header=None, names=column_names)
celldata313 = pd.read_csv('313.csv.gz', compression='gzip', header=None, names=column_names)
celldata314 = pd.read_csv('314.csv.gz', compression='gzip', header=None, names=column_names)
celldata315 = pd.read_csv('315.csv.gz', compression='gzip', header=None, names=column_names)
celldata316 = pd.read_csv('316.csv.gz', compression='gzip', header=None, names=column_names)

# worldwidecelldata = pd.read_csv('cell_towers.csv.gz', compression='gzip', header=None, names=column_names)
# match_worldwide = worldwidecelldata[worldwidecelldata['CID'] == 63087362]
# print(match_worldwide)
print(celldata310)
print(len(celldata311))
print(len(celldata312))
print(len(celldata313))
print(len(celldata314))
print(len(celldata315))
print(len(celldata316))

match_311 = celldata311[celldata311['CID'] == 63087362]
print(len(celldata310)+len(celldata311)+len(celldata312)+len(celldata313)+len(celldata314)+len(celldata315)+len(celldata316))

combined_celldata = [celldata310, celldata311, celldata312, celldata313, celldata314, celldata315, celldata316]
celldata = pd.concat(combined_celldata, ignore_index=True)
# print(celldata[15])
celldata_coords = celldata.iloc[:, [7, 6]].values

print(match_311)

# x = geodesic((hospital_coords[5765][0], hospital_coords[5765][1]), (38.681831, -121.157913)).kilometers
# print(x * 1000)
filtered_by_range_df = celldata[celldata.iloc[:, 8] <= 15000]
print(len(filtered_by_range_df))
fin_celldata = filtered_by_range_df[filtered_by_range_df.iloc[:, 9] > 2]
print(len(fin_celldata))


print(fin_celldata)

# Creating a map centered at a specific latitude and longitude for all hospitals
# my_map = folium.Map(location=[39.8097, 98.5556], zoom_start=1)

# looprun = 0
# for idx, hospital_coord in enumerate(hospital_coords_df_cleaned.iterrows()):
#     # print(hospital_coord[1]['Latitude'])
#     # print(hospital_coord[1]['Longitude'])
#     if idx == 0:  # Skip the first row
#         continue
#     # Add a marker for each valid coordinate
#     folium.Marker([hospital_coord[1]['Latitude'], hospital_coord[1]['Longitude']], popup=hospital_names[looprun]).add_to(my_map)
#     looprun += 1

# Display the map
x = 1
for i in range(10):
    if i > 5:
        x = 100
    print(i)
    print(x)

# df = pd.read_csv('preliminary_AHA_OpenCellID_analysis', index_col=0)

# Optionally, you can rename columns explicitly if needed:
# df.columns = ['Hospital Name', 'Nearby Cell Towers 10m', 'Nearby Cell Towers 100m', 'Nearby Cell Towers 1000m']

# # Display cleaned DataFrame
# # print(df.head())

# filtered_df = df[(df['Nearby Cell Towers 10m'] != 0) | 
#                  (df['Nearby Cell Towers 100m'] != 0) | 
#                  (df['Nearby Cell Towers 1000m'] != 0)]

# print(filtered_df.head())

# # merged_df = pd.merge(filtered_df, hospital_lat_long_df, on='Hospital Name', how='inner')
# merged_df = pd.merge(df, hospital_lat_long_df, on='Hospital Name', how='inner')
# # print(merged_df.head())
# # print(len(merged_df))

# # second_map = folium.Map(location=[39.8097, 98.5556], zoom_start=1)

# merged_df['Latitude'] = pd.to_numeric(merged_df['Latitude'])
# merged_df['Longitude'] = pd.to_numeric(merged_df['Longitude'])
# merged_df_cleaned = merged_df.dropna(subset=['Latitude', 'Longitude'])
# # print(len(merged_df_cleaned))
# # print(merged_df_cleaned.tail())
# for _, row in merged_df_cleaned.iterrows():
#     # print(row['Latitude'])
#     # print(row['Longitude'])
#     if (row['Nearby Cell Towers 10m'] != 0 or row['Nearby Cell Towers 100m'] != 0 or row['Nearby Cell Towers 1000m'] != 0):
#         blue_icon = BeautifyIcon(
#             icon_shape='marker',  # Pin shape
#             border_color='blue',  # Color for the pin border
#             text_color='blue',  # Color for the pin text
#             icon_size=[15, 15]  # Set the size of the pin
#         )
#         folium.Marker([row['Latitude'], row['Longitude']], popup={row['Hospital Name']}, icon=blue_icon).add_to(my_map)

#     else:
#         red_icon = BeautifyIcon(
#             icon_shape='marker',  # Pin shape
#             border_color='red',  # Color for the pin border
#             text_color='red',  # Color for the pin text
#             icon_size=[15, 15]  # Set the size of the pin
#         )
#         folium.Marker([row['Latitude'], row['Longitude']], popup={row['Hospital Name']}, icon=red_icon).add_to(my_map)


# # Display the map
# my_map.save("Comparison.html")
# # second_map.save("HospitalsMapWithNonZeroCellTowers.html")
