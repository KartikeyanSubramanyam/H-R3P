import os, csv
from collections import Counter

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
                if second_row[1] == retry_code:
                    print(f"station numbe retry, error code 7, name {name[1]}")

    return line_station

def debug_find_station(filename):
    line_station = 0 
    with open(filename, 'r') as file:
        line_station = len(file.readlines()) - 1
        print (line_station)
    
 
def contains_non_letters(s):
    for index, char in enumerate(s):
        if not char.isalpha():
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

duplicates = find_duplicates()

# with open('duplicates.txt', mode='w', newline='') as file:
#     for item in duplicates:
#         file.write(f"{item}\n")

# print (len(duplicates))


with open("../Analysis Results/api_results.csv") as file:
    csvfile = csv.reader(file)
    for row in csvfile:
        name = row[:2]
        # names = names + [name]
        underline_name = contains_non_letters(name[1])
        if underline_name in duplicates:
            # print (f"find duplicate hospital name, name {name[1]}")
            continue
        # hospital_names.append(name[1])
        dir_list = os.listdir("../Hospital Results")
        underline_filename = underline_name + ".csv"
        exact_matches = [filename for filename in dir_list if filename == underline_filename]
        if exact_matches:
            filename = exact_matches[0]
        if len(exact_matches) == 0:
            # print(f"unfound hospital, name {name[1]}")
            continue
        filePath = "../Hospital Results/" + filename
        numStation = find_number_station(filePath, name)
        if numStation < 0:
            # print(f"abnormal station, name {name[1]}")
            continue
        name = name + [str(numStation)]
        # print(name)
        if len(name) < 3:
            # print(f"abnormal name, name {name[1]}")
            continue 
        final_output = final_output + [name]
    # print(len(final_output))

filename1 = "output.csv"

    # Open or create a CSV file for writing
with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(firstRow)
    # Write each sub-list as a row in the CSV file
    writer.writerows(final_output)


        




