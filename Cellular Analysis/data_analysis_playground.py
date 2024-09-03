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
print(hospital_lat_long_df)
column_names = ['Radio Gen.', 'MCC', 'MNC', 'LAC', 'CID', 'X', 'Longitude', 'Latitude', 'Range', 'Samples', 'Changeable', 'Created', 'Updated', 'Average Signal']
# Extracting OpenCellID Data (7 different files for 310-316 MCC)
celldata310 = pd.read_csv('310.csv.gz', compression='gzip', header=None, names=column_names)
celldata311 = pd.read_csv('311.csv.gz', compression='gzip', header=None, names=column_names)
celldata312 = pd.read_csv('312.csv.gz', compression='gzip', header=None, names=column_names)
celldata313 = pd.read_csv('313.csv.gz', compression='gzip', header=None, names=column_names)
celldata314 = pd.read_csv('314.csv.gz', compression='gzip', header=None, names=column_names)
celldata315 = pd.read_csv('315.csv.gz', compression='gzip', header=None, names=column_names)
celldata316 = pd.read_csv('316.csv.gz', compression='gzip', header=None, names=column_names)


# print(len(celldata310))
# print(len(celldata311))
# print(len(celldata312))
# print(len(celldata313))
# print(len(celldata314))
# print(len(celldata315))
# print(len(celldata316))

print(len(celldata310)+len(celldata311)+len(celldata312)+len(celldata313)+len(celldata314)+len(celldata315)+len(celldata316))

combined_celldata = [celldata310, celldata311, celldata312, celldata313, celldata314, celldata315, celldata316]
celldata = pd.concat(combined_celldata, ignore_index=True)

# lengths for separate and concatenated match
# print(len(celldata))

filtered_by_range_df = celldata[celldata.iloc[:, 8] <= 15000]
print(len(filtered_by_range_df))
fin_celldata = filtered_by_range_df[filtered_by_range_df.iloc[:, 9] > 2]
print(len(fin_celldata))
# print(fin_celldata)