import os
import pandas as pd
import csv

# Step 1: Load AT&T MCC/MNC data from a CSV file
att_mcc_mnc_file = '../Databases/AT&T_MCC_MNC.csv'  # Replace with the path to your AT&T CSV file
att_df = pd.read_csv(att_mcc_mnc_file)

# Ensure the CSV contains the correct column names
# The script assumes the CSV has columns named 'mcc' and 'mnc'.
# If your CSV has different column names, you can rename them like this:
# att_df = att_df.rename(columns={"your_mcc_column": "mcc", "your_mnc_column": "mnc"})
print(att_df)
# Step 2: Define directory containing cell tower data

# Filter AT&T and FirstNet data separately
att_towers_df = att_df[att_df['network'] == 'AT&T']
firstnet_towers_df = att_df[att_df['network'] == 'FirstNet']
print(att_towers_df)
print(firstnet_towers_df)
directory = "../Hospital_Results/"  # Replace with your cell tower files directory

with open('../Databases/2024_05_UC_San_Diego_Health.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extracting hospital name and coordinates
df = pd.DataFrame(data[6:], columns=data[5])
hospital_lat_long_df = df[['Hospital Name', 'Latitude', 'Longitude']]
print(len(hospital_lat_long_df))
print(hospital_lat_long_df)
hospital_lat_long_df[['Latitude', 'Longitude']] = hospital_lat_long_df[['Latitude', 'Longitude']].apply(pd.to_numeric)

# Step 4: Prepare results logging
results = []

# Step 5: Iterate through hospitals in AHA database
for _, hospital in hospital_lat_long_df.iterrows():
    hospital_name = hospital['Hospital Name']
    
    # Generate a cleaned hospital name to match file names
    cleaned_hospital_name = "".join(c if c.isalnum() else "_" for c in hospital_name)
    file_path = os.path.join(directory, f"{cleaned_hospital_name}.csv")
    
    if os.path.exists(file_path):
        # Step 6: Open corresponding file and check for 'No cells found'
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            
            if first_line == 'info,code':
                # Read the second line to check if it contains 'No cells found'
                second_line = file.readline().strip()
                if second_line == 'No cells found,1':
                    # Log that no cells were found
                    results.append({
                        'Hospital Name': hospital_name,
                        'AT&T Towers': 0,
                        'FirstNet Towers': 0,
                    })
                    continue
        
        # Step 7: If no 'No cells found' case, proceed with normal processing
        tower_data = pd.read_csv(file_path)
        
        # Initialize counters for AT&T and FirstNet towers
        att_matches = 0
        firstnet_matches = 0
        
        # Step 8: Compare each entry (tower) to AT&T and FirstNet MCC/MNC lists
        for _, row in tower_data.iterrows():
            mcc = row.get('mcc')
            mnc = row.get('mnc')
            
            if not pd.isna(mcc) and not pd.isna(mnc):
                # Check if (mcc, mnc) exists in AT&T or FirstNet databases
                if not att_towers_df[(att_towers_df['mcc'] == mcc) & (att_towers_df['mnc'] == mnc)].empty:
                    att_matches += 1
                elif not firstnet_towers_df[(firstnet_towers_df['mcc'] == mcc) & (firstnet_towers_df['mnc'] == mnc)].empty:
                    firstnet_matches += 1
        
        # Step 9: Log results for this hospital
        results.append({
            'Hospital Name': hospital_name,
            'AT&T Towers': att_matches,
            'FirstNet Towers': firstnet_matches,
        })
    else:
        # Log missing file information
        results.append({
            'Hospital Name': hospital_name,
            'AT&T Towers': 0,
            'FirstNet Towers': 0,
        })

# Step 10: Save results to a CSV file
results_df = pd.DataFrame(results)
results_df.to_csv('hospital_att_firstnet_tower_comparison.csv', index=False)

# Optional: Print results summary
print(results_df.head())
