import os, csv
from collections import Counter
import pandas as pd

def find(name, files):
    for filename in files:
        if filename.find(name) != -1:
            return filename
    # print(name)
    return None

def find_number_station(filename, name):
    line_station = 0
    first_row = None
    second_row = None
    error_first_row = ['info', 'code']
    retry_code = '7'
 
    with open(filename, 'r') as file:
        line_station = len(file.readlines()) - 1

    if line_station == 1:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            first_row = next(reader)  # Read the first row
            second_row = next(reader) # Read the second row  
            if first_row == error_first_row:
                line_station = 0
                # if second_row[1] == retry_code:
                #     print(f"station numbe retry, error code 7, name {name[1]}")

    return line_station

def debug_find_station(filename):
    line_station = 0 
    with open(filename, 'r') as file:
        line_station = len(file.readlines()) - 1
        print (line_station)
    
 
def contains_non_letters(s):
    for index, char in enumerate(s):
        if not char.isalpha() and not char.isdigit():
            # Found a non-letter character
            s = s.replace(char, '_')
    return s  # All characters are letters

def find_duplicates_list(lst):
    counts = Counter(lst)
    return [item for item, count in counts.items() if count > 1]

def find_duplicates():
    with open("../Analysis Results/api_results.csv") as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            name = row[:2]
            name[1] = contains_non_letters(name[1])
            hospital_names.append(name[1])

    return find_duplicates_list(hospital_names)

final_output = []
hospital_names = []
duplicates = []
firstRow = ["", "Hospital Name" ,"Nearby Cell Towers"]
unfounded = set()
hospital_info = []

duplicates = find_duplicates()

# print (len(duplicates))


# Reading AHA dataset for hospitals and their respective co-ordinates
# Depending on version of python; might need to run the below command as:
# with open('2024_05_UC_San_Diego_Health.csv', 'r', encoding='utf-8-sig') as f:
with open('../2024_05_UC_San_Diego_Health.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extracting hospital name and coordinates
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]
print(len(hospital_lat_long_df))

# Clean and convert latitude/longitude to numeric
hospital_lat_long_df[['Latitude', 'Longitude']] = hospital_lat_long_df[['Latitude', 'Longitude']].apply(pd.to_numeric)

for index, row in hospital_lat_long_df.iterrows():
    ind = str(index)
    name = row['Hospital Name']
    lat = row['Latitude']
    long = row['Longitude']
    info = [ind, name, lat, long]
    hospital_info.append(info)

with open('aha_hospital.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(hospital_info)

        



# for index, row in hospital_lat_long_df.iterrows():
#     name = row['Hospital Name']
#     # names = names + [name]
#     underline_name = contains_non_letters(name)
#     # if underline_name in duplicates:
#     #     # print (f"find duplicate hospital name, name {name[1]}")
#     #     continue
#     dir_list = os.listdir("../Hospital Results")
#     underline_filename = underline_name + ".csv"
#     exact_matches = [filename for filename in dir_list if filename == underline_filename]
#     if exact_matches:
#         filename = exact_matches[0]
#     if len(exact_matches) == 0:
#         # print(f"unfound hospital, name {name}")
#         unfounded.add(name)
#     # filePath = "../Hospital Results/" + filename
#     # numStation = find_number_station(filePath, name)
#     # if numStation < 0:
#     #     # print(f"abnormal station, name {name[1]}")
#     #     continue
#     # name = name + [str(numStation)]
#     # # print(name)
#     # if len(name) < 3:
#     #     # print(f"abnormal name, name {name[1]}")
#     #     continue 
#     # final_output = final_output + [name]
# # print(len(final_output))

# print (len(unfounded))

# filename1 = "output.csv"

#     # Open or create a CSV file for writing
# with open('unfounded.txt', mode='w', newline='') as file:
#     for item in unfounded:
#         file.write(f"{item}\n")
        



