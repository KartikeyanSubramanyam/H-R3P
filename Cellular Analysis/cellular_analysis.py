import pandas as pd
import csv
from geopy.distance import geodesic

# Reading AHA dataset for hospitals and their respective co-ordinates
with open('2024_05_UC_San_Diego_Health.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extracting only the hospital name and coords
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]


# Extracting OpenCellID Data (6 different files for 310-316 MCC)
celldata310 = pd.read_csv('310.csv.gz', compression='gzip')
celldata311 = pd.read_csv('311.csv.gz', compression='gzip')
celldata312 = pd.read_csv('312.csv.gz', compression='gzip')
celldata313 = pd.read_csv('313.csv.gz', compression='gzip')
celldata314 = pd.read_csv('314.csv.gz', compression='gzip')
celldata315 = pd.read_csv('315.csv.gz', compression='gzip')
celldata316 = pd.read_csv('316.csv.gz', compression='gzip')
# print(celldata310.iloc[:, [6, 7]].values)

# Extracting only the co-ordinates for cellular samples
celldata310_coords = celldata310.iloc[:, [7, 6]].values
celldata311_coords = celldata311.iloc[:, [7, 6]].values
celldata312_coords = celldata312.iloc[:, [7, 6]].values
celldata313_coords = celldata313.iloc[:, [7, 6]].values
celldata314_coords = celldata314.iloc[:, [7, 6]].values
celldata315_coords = celldata315.iloc[:, [7, 6]].values
celldata316_coords = celldata316.iloc[:, [7, 6]].values

# print(celldata310_coords)


hospital_names = hospital_lat_long_df['Hospital Name'].values
hospital_coords = hospital_lat_long_df[['Latitude', 'Longitude']].values
# print(hospital_names)
# print(hospital_coords)
# print(celldata316.size + celldata315.size + celldata314.size + celldata313.size + celldata312.size + celldata311.size + celldata310.size)
# print(hospital_lat_long_df.head())

# Custom DataFrame to help record various distance metric requirements
hospital_proximity = pd.DataFrame({
    'Hospital Name': hospital_names,
    'Nearby Cell Towers 10m': 0,
    'Nearby Cell Towers 100m': 0,
    'Nearby Cell Towers 1000m': 0
})

# print(hospital_proximity.iloc[0])

hospital_count = 0
for hospital_coord in hospital_coords:

    # 310 MCC
    for cellular_coord in celldata310_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 10:
            print('Got em at 10!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 10m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
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

    # 311 MCC
    for cellular_coord in celldata311_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 10:
            print('Got em at 10!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 10m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
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

    # 312 MCC
    for cellular_coord in celldata312_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 10:
            print('Got em at 10!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 10m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
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

    # 313 MCC
    for cellular_coord in celldata313_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 10:
            print('Got em at 10!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 10m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
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

    # 314 MCC
    for cellular_coord in celldata314_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 10:
            print('Got em at 10!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 10m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
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

    # 315 MCC
    for cellular_coord in celldata315_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 10:
            print('Got em at 10!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 10m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
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
    
    # 316 MCC
    for cellular_coord in celldata316_coords:
        distance = geodesic((hospital_coord[0], hospital_coord[1]), (cellular_coord[0], cellular_coord[1])).kilometers
        if (distance * 1000) <= 10:
            print('Got em at 10!')
            hospital_proximity.at[hospital_count, 'Nearby Cell Towers 10m'] += 1
            print(hospital_proximity.iloc[hospital_count])
            print(cellular_coord)
            continue
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


# hospital_proximity.at[0, 'Nearby Cell Towers 100m'] = 5
print(hospital_proximity)
hospital_proximity.to_csv('preliminary_AHA_OpenCellID_analysis', index=True)