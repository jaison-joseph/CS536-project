import os
import pandas as pd

# Define the directory path
simid = 1
directory_path = "simulations/nsfnet_10_15/run_" + str(simid) + "/decoded_data/"

# Initialize an empty DataFrame to store the results
columns = ['source', 'destination', 'bitrate', 'delay', 'jitter', 'packet_loss', 'simid']
result_df = pd.DataFrame(columns=columns)

# Traverse all files in the directory
for filename in os.listdir(directory_path):
    # Split the filename to extract source and destination nodes
    parts = filename.split('_')
    if len(parts) < 2:
        continue  # Skip files that do not have the expected naming convention
    source = parts[-2]
    destination = parts[-1]
    
    # Read the file into a DataFrame
    file_path = os.path.join(directory_path, filename)
    try:
        df = pd.read_csv(file_path, delim_whitespace=True, header=None)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        avg_values = [0, 0, 0, 0]
    
    # Check if the DataFrame has at least 4 columns
    if df.shape[1] < 4:
        print(f"File {filename} does not have enough columns.")
        avg_values = [0, 0, 0, 0]
    
    # Calculate the average of the last four columns
    avg_values = df.iloc[:, -4:].mean().values
    
    # Append the row to the result DataFrame
    new_row = {
        'source': source,
        'destination': destination,
        'bitrate': avg_values[0],
        'delay': avg_values[1],
        'jitter': avg_values[2],
        'packet_loss': avg_values[3],
        'simid' : simid
    }
    result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)

# Display the resulting DataFrame
print(result_df)

# Optionally, save the resulting DataFrame to a CSV file
result_df.to_csv('network_data_summary.csv', index=False)
