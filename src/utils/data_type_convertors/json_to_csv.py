import json
import csv
import os

current_json_file_path = os.path.join(os.path.dirname(__file__), './../../data/grocery_items_normalized', 'grocery_store_b_items.json')
current_csv_file_path = os.path.join(os.path.dirname(__file__), './../../data/grocery_items_normalized', 'grocery_store_b_items.csv')

# Convert json to csv
def jsonToCsv(json_file_path, csv_file_path):
    # Load the JSON data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Open a CSV file for writing
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        if len(data) > 0:
            # Create a CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())

            # Write the header
            writer.writeheader()

            # Write the rows
            for row in data:
                writer.writerow(row)

    print(f"CSV file has been created at: {csv_file_path}")

jsonToCsv(current_json_file_path, current_csv_file_path)