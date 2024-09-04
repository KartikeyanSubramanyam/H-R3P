import pandas as pd
import csv
from geopy.distance import geodesic
import numpy as np


# Reading AHA dataset for hospitals and their respective co-ordinates
# Depending on version of python; might need to run the below command as:
# with open('2024_05_UC_San_Diego_Health.csv', 'r', encoding='utf-8-sig') as f:
with open('2024_05_UC_San_Diego_Health.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extracting only the hospital name and coords
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]

# Split the DataFrame into 4 parts
hospital_df_split = np.array_split(hospital_lat_long_df, 4)

# Access each part
df1 = hospital_df_split[0]
df2 = hospital_df_split[1]
df3 = hospital_df_split[2]
df4 = hospital_df_split[3]

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
combined_celldata = [celldata310, celldata311, celldata312, celldata313, celldata314, celldata315, celldata316]
prelim_celldata = pd.concat(combined_celldata, ignore_index=True)


# Filter the OpenCelliD Data by Range <= 15000 meters and Samples > 2
filtered_by_range_df = prelim_celldata[prelim_celldata.iloc[:, 8] <= 15000]
print(len(filtered_by_range_df))
celldata = filtered_by_range_df[filtered_by_range_df.iloc[:, 9] > 2]
print(len(celldata))

# Extracting only the co-ordinates for cellular samples
celldata_coords = celldata.iloc[:, [7, 6]].values


hospital_names = df1['Hospital Name'].values
hospital_coords = df1[['Latitude', 'Longitude']].values

# Custom DataFrame to help record various distance metric requirements
hospital_proximity = pd.DataFrame({
    'Hospital Name': hospital_names,
    'Nearby Cell Towers 10m': 0,
    'Nearby Cell Towers 100m': 0,
    'Nearby Cell Towers 1000m': 0
})


# TODO (Maybe): Organize the OpenCelliD data by lat longs, and batch the scans by lat longs.

hospital_count = 0
for hospital_coord in hospital_coords:
    for cellular_coord in celldata_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 100:
            print('Got em at 100!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 100m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
        if (distance * 1000) <= 1000:
            print('Got em at 1000!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 1000m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
        
    hospital_count += 1


print(hospital_proximity)
hospital_proximity.to_csv('filtered_AHA_OpenCellID_analysis_section1', index=False)