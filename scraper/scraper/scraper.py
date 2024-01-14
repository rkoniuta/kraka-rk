import csv

# Using csv module and indexing by column names:
with open('./data/import_yeti_alu_with_contact.csv', 'r') as csvfile:

    reader = csv.reader(csvfile)
    header = next(reader)  # Get column names

    d = {}
    for i, column_name in enumerate(header):
            d[column_name] = i
    print(d)

    o = []
    for row in reader:
        if 
        r = []
        'Company Total Shipments'
        r.append()
        
        #print(row[d["Company Name"]]

#print(d['Column2'])  # Access a column using the csv module approach

