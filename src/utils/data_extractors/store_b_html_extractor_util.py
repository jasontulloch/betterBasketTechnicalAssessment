import json
from bs4 import BeautifulSoup
import re

# Extract product information from HTML data embedded in a JSON file
def extract_html_data(file_path):

    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # List to store all extracted products
    all_products = []

    # Loop through each item in the array of data
    for entry in data:
        # Extract HTML data from the JSON structure
        html_data = entry['data']['html_data']

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html_data, 'html.parser')

        # Find the script tag that contains the data
        script_tag = soup.find('script', text=re.compile(r'logEvent\(\{'))
        if not script_tag:
            print("Script tag not found for this entry")
            continue

        # Extract the script content and clean it
        script_content = script_tag.string
        script_content_match = re.search(r'logEvent\(\{(.*)\}\);', script_content, re.DOTALL)

        if not script_content_match:
            print("No valid logEvent content found in script")
            continue

        # Extract the JSON-like string from the script content
        json_str = "{" + script_content_match.group(1).strip() + "}"

        # Clean up the JSON string
        json_str = json_str.replace("'", '"')  # Replace single quotes with double quotes
        json_str = re.sub(r'(\w+):', r'"\1":', json_str)  # Ensure all keys are quoted
        json_str = json_str.replace('&#13;', '')  # Replace any HTML entities

        try:
            # Parse the extracted JSON string
            json_data = json.loads(json_str)['ecommerce']['items']
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing JSON: {e}")
            continue

        # Extract relevant fields from each item
        products = []
        for item in json_data:
            product = {
                'name': item.get('item_name', 'N/A'),
                'price': item.get('price', 'N/A'),
                'item_variant': item.get('item_variant', 'N/A'),
                'item_discount': item.get('item_discount', 'N/A'),
                'item_id': item.get('item_id', 'N/A'),
                'item_index': item.get('item_index', 'N/A'),
                'promotion_name': item.get('promotion_name', 'N/A'),
                'item_list_name': item.get('item_list_name', 'N/A'),
                'item_category3': item.get('item_category3', 'N/A'),
                'item_category2': item.get('item_category2', 'N/A'),
                'item_category': item.get('item_category', 'N/A')
            }
            products.append(product)

        # Append extracted products for this entry to the final list
        all_products.extend(products)

    return all_products

