import pandas as pd
import csv
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

# Clean and convert latitude/longitude to numeric
hospital_lat_long_df[['Latitude', 'Longitude']] = hospital_lat_long_df[['Latitude', 'Longitude']].apply(pd.to_numeric)
hospital_lat_long_df_cleaned = hospital_lat_long_df.dropna(subset=['Latitude', 'Longitude'])
# print(len(hospital_lat_long_df_cleaned))

# Creating a map centered at a specific latitude and longitude for all hospitals
my_map = folium.Map(location=[44.967243, -103.771556], zoom_start=4)

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

# df = pd.read_csv('../Analysis_Results/api_results.csv', index_col=0)

# # Optionally, you can rename columns explicitly if needed:
# # df.columns = ['Hospital Name', 'Nearby Cell Towers']

# # Display cleaned DataFrame
# print(df.head())

# filtered_df = df[(df['Nearby Cell Towers'] != 0)]

# print(filtered_df.head())
# print(len(filtered_df))

# # merged_df = pd.merge(filtered_df, hospital_lat_long_df, on='Hospital Name', how='inner')
# merged_df = pd.merge(df, hospital_lat_long_df, on='Hospital Name', how='inner')
# # print(merged_df.head())
# # print(len(merged_df))

# # second_map = folium.Map(location=[39.8097, 98.5556], zoom_start=1)

# merged_df['Latitude'] = pd.to_numeric(merged_df['Latitude'])
# merged_df['Longitude'] = pd.to_numeric(merged_df['Longitude'])
# merged_df_cleaned = merged_df.dropna(subset=['Latitude', 'Longitude'])
# print(len(merged_df_cleaned))
# print(merged_df_cleaned.tail())
# count = 0
# for _, row in merged_df_cleaned.iterrows():
#     # print(row['Latitude'])
#     # print(row['Longitude'])
#     if (row['Nearby Cell Towers'] != 0):
#         blue_icon = BeautifyIcon(
#             icon_shape='marker',  # Pin shape
#             border_color='blue',  # Color for the pin border
#             text_color='blue',  # Color for the pin text
#             icon_size=[15, 15]  # Set the size of the pin
#         )
#         folium.Marker([row['Latitude'], row['Longitude']], popup={row['Hospital Name']}, icon=blue_icon).add_to(my_map)
#         count += 1

#     else:
#         red_icon = BeautifyIcon(
#             icon_shape='marker',  # Pin shape
#             border_color='red',  # Color for the pin border
#             text_color='red',  # Color for the pin text
#             icon_size=[15, 15]  # Set the size of the pin
#         )
#         folium.Marker([row['Latitude'], row['Longitude']], popup={row['Hospital Name']}, icon=red_icon).add_to(my_map)


# # Display the map
# my_map.save("../Maps/API_Result_Comparison.html")
# print(count)

df = pd.read_csv('../Analysis_Results/AT&T+FirstNet_Count_List.csv', index_col=0)
print(df.head())
print(len(df))

# merged_df = pd.merge(filtered_df, hospital_lat_long_df, on='Hospital Name', how='inner')
merged_df = pd.merge(df, hospital_lat_long_df, on='Hospital Name', how='inner')
# print(merged_df.head())
print(len(merged_df))

# second_map = folium.Map(location=[39.8097, 98.5556], zoom_start=1)

merged_df['Latitude'] = pd.to_numeric(merged_df['Latitude'])
merged_df['Longitude'] = pd.to_numeric(merged_df['Longitude'])
merged_df_cleaned = merged_df.dropna(subset=['Latitude', 'Longitude'])
# print(len(merged_df_cleaned))
# print(merged_df_cleaned.tail())
attcount = 0
fncount = 0
nocount = 0



for _, row in merged_df_cleaned.iterrows():
    # print(row['Latitude'])
    # print(row['Longitude'])
    if (row['FirstNet'] > 0):
        red_icon = BeautifyIcon(
            icon_shape='marker',  # Pin shape
            border_color='red',  # Color for the pin border
            text_color='red',  # Color for the pin text
            icon_size=[15, 15]  # Set the size of the pin
        )
        folium.Marker([row['Latitude'], row['Longitude']], popup={row['Hospital Name']}, icon=red_icon).add_to(my_map)
        fncount += 1
        # print()
        # print(row['FirstNet'])
        continue
        
    if (row['AT&T'] > 0):
        blue_icon = BeautifyIcon(
            icon_shape='marker',  # Pin shape
            border_color='blue',  # Color for the pin border
            text_color='blue',  # Color for the pin text
            icon_size=[15, 15]  # Set the size of the pin
        )
        folium.Marker([row['Latitude'], row['Longitude']], popup={row['Hospital Name']}, icon=blue_icon).add_to(my_map)
        attcount += 1
        continue

    if (row['AT&T'] == 0) and (row['FirstNet'] == 0):
        green_icon = BeautifyIcon(
            icon_shape='marker',  # Pin shape
            border_color='green',  # Color for the pin border
            text_color='green',  # Color for the pin text
            icon_size=[15, 15]  # Set the size of the pin
        )
        folium.Marker([row['Latitude'], row['Longitude']], popup={row['Hospital Name']}, icon=green_icon).add_to(my_map)
        nocount += 1
        # print(row['Hospital Name'] + "," + str(row['AT&T']) + "" + str(row['FirstNet']))
        continue


# Display the map
my_map.save("../Maps/AT&T_Map.html")
print(attcount)
print(fncount)
print(nocount)
