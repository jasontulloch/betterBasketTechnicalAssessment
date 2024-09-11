import json

# Extract product values from a JSON file based on specified keys
def get_product_values(file_path, required_keys=None):
    if required_keys is None:
        # Default keys to return if none are specified
        required_keys = ["name", "price", "priceInfo", "category", "type", "ironbankcategory", "brand"]

    # Open the JSON file and load its content
    with open(file_path, 'r') as file:
        data = json.load(file)

    # List to store product values
    product_values = []

    # Recursively collect values associated with the "product" key at the second level.
    def collect_product_values(obj, level=0):
        if isinstance(obj, dict):
            if level == 1:
                # Collect values associated with the "product" key at the second level
                if "product" in obj:
                    product = obj["product"]
                    # Extract only the required keys from the product
                    filtered_product = {key: product.get(key, 'N/A') for key in required_keys}
                    product_values.append(filtered_product)
            else:
                # Recursively search in dictionaries at deeper levels
                for key, value in obj.items():
                    collect_product_values(value, level + 1)
        elif isinstance(obj, list):
            for item in obj:
                collect_product_values(item, level)

    # Start collecting product values from the top level of the JSON data
    collect_product_values(data)

    # Return the list of product values
    return product_values