import json

# Get all unique keys from json file
def get_json_keys(file_path):
    # Open the JSON file and load its content
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Initialize a set to store unique keys
    all_keys = set()

    def collect_keys(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                all_keys.add(key) # Add the key to the set
                collect_keys(value) # Recurse into the value
        elif isinstance(obj, list):
            for item in obj:
                collect_keys(item) # Recurse into each item in the list

    # Start the key collection process
    collect_keys(data)

    # Return the collected keys as a list
    return list(all_keys)
