import json

# Extract keys from the second level of a JSON file's structure.
def get_nested_json_keys(file_path):

    # Open the JSON file and load its content
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Set to store unique keys at the second level
    second_level_keys = set()

    def collect_keys(obj, level=0):
        if isinstance(obj, dict):
            if level == 1:
                # Collect keys at the second level of the dictionary
                for key in obj.keys():
                    second_level_keys.add(key) # Add the key to the set
            else:
                # Recursively collect keys at deeper levels
                for key, value in obj.items():
                    collect_keys(value, level + 1) # Increment level for nested objects
        elif isinstance(obj, list):
            for item in obj:
                collect_keys(item, level) # Maintain the current level for lists

    # Start collecting keys from the top level of the JSON data
    collect_keys(data)

    # Return the collected second-level keys as a list
    return list(second_level_keys)
