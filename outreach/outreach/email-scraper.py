import pandas as pd
import os
import re

# Specify the folder path containing the CSV files
folder_path = './data'

# Create an empty list to store the data
supplier_data_list = []
client_data_list = []

def find_at(text):
  """Finds all words containing "@" in a string.

  Args:
    text: The string to search.

  Returns:
    A list of words containing "@".
  """

  words_with_at = re.findall(r"\b\w+@\w+\b", text)
  return words_with_at


# Iterate through each CSV file in the folder
for filename in os.listdir(folder_path):
   if filename.startswith('IY_') and filename.endswith('.csv'):
       file_path = os.path.join(folder_path, filename)
       try:
           # Read the CSV file using pandas
           df = pd.read_csv(file_path)

           # Extract the email, color, and type from each row
           for index, row in df.iterrows():
               name = row[0]
               emails = [ a + '.com' for a in find_at(row[3]) ]
               total_vol = row[10]
               country = row[4]
               color = filename.split('_')[1]  # Extract color from filename
               client_type = filename.split('_')[2].split('.')[0]  # Extract type from filename
            
               # Append the extracted data to the list
               if len(emails) > 0:
                if country == "Mexico" and client_type.lower() == 'manufacturers':
                        supplier_data_list.append([name, emails, color, client_type, total_vol, country])
                elif country != "Mexico" and client_type.lower() == 'manufacturers':
                        pass
                elif client_type.lower() == 'clients':
                        client_data_list.append([name, emails, color, client_type, total_vol, country])
                else:
                        print(f"error! {filename}")

       except Exception as e:
           print(f"Error processing file {filename}: {e}")


# Create a DataFrame from the consolidated data
supplier_master_df = pd.DataFrame(supplier_data_list, columns=['name', 'email', 'product', 'client type', 'total volume', 'country'])
client_master_df = pd.DataFrame(client_data_list, columns=['name', 'email', 'product', 'client type', 'total volume', 'country'])

# Save the consolidated DataFrame to a new CSV file
supplier_master_df.to_csv('./outputs/supplier_master_file.csv', index=False)
client_master_df.to_csv('./outputs/client_master_file.csv', index=False)