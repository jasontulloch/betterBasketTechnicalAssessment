import os
import json
import re

# Format a unit price string into a more readable format and extract the unit label
def format_unit_price(unit_price):
    if unit_price is None:
        return None, None  # Return None for both formatted price and variant label

    unit_price = unit_price.strip()

    # Remove any non-numeric characters except for the decimal point and slashes
    cleaned_price = re.sub(r'[^\d./]+', '', unit_price)

    # Extract numeric value
    match = re.match(r'(\d+(\.\d+)?)', cleaned_price)
    if not match:
        return unit_price, None  # Return original if no match

    # Convert cents to dollars
    price_in_cents = float(match.group(0))
    price_in_dollars = price_in_cents / 100

    # Extract the unit part (e.g., "g", "oz", "unit")
    unit_match = re.search(r'/\s*(\w+)$', unit_price)
    unit = unit_match.group(1) if unit_match else None

    # Format the final string
    formatted_price = f"${price_in_dollars:.3f} / {unit}" if unit else f"${price_in_dollars:.3f}"

    return formatted_price, unit

# Normalize a list of product dictionaries by formatting prices and extracting category information
def normalize_a_products(products):

    normalized = []

    for product in products:
        price_info = product.get("priceInfo") or {}
        current_price_info = price_info.get("currentPrice") or {}
        unit_price_info = price_info.get("unitPrice") or {}
        unit_price_value = unit_price_info.get("price") or None

        # Handle category path safely
        category_path = product.get("category", {}).get("path", [])
        category_length = len(category_path)

        # Format the unit price
        formatted_unit_price, variant_label = format_unit_price(unit_price_info.get("priceString"))

        # Format price for string
        price = current_price_info.get("price", None)
        if price is not None:
            formatted_price = f"${price:.2f}"
        else:
            formatted_price = None

        # Construct the normalized product dictionary
        normalized_product = {
            "name": product.get("name", None),
            "price": price,
            "priceString": formatted_price,
            "unitPrice": unit_price_value,
            "unitPriceString": formatted_unit_price,
            "category": category_path[1]["name"] if category_length == 4 and category_path[1] else (
                category_path[0]["name"] if category_length > 0 and category_path[0] else None),
            "category2": category_path[2]["name"] if category_length == 4 and category_path[2] else (
                category_path[1]["name"] if category_length > 1 and category_path[1] else None),
            "category3": category_path[3]["name"] if category_length == 4 and category_path[3] else (
                category_path[2]["name"] if category_length > 2 and category_path[2] else None),
            "group": category_path[0]["name"] if category_length == 4 and category_path[0] else None,
            "type": product.get("type", None),
            "brand": product.get("brand", None),
            "variantLabel": variant_label,
        }
        normalized.append(normalized_product)

    return normalized
#
# # Define file paths for input and output
# input_file_path = os.path.join(os.path.dirname(__file__), './../../data/grocery_items_clean', 'grocery_store_a_items.json')
# output_file_path = os.path.join(os.path.dirname(__file__), './../../data/grocery_items_normalized/grocery_store_a_items.json')
#
# # Read the input file
# with open(input_file_path, 'r') as infile:
#     products = json.load(infile)
#
# # Normalize the products
# normalized_data = normalize_products(products)
#
# # Write the normalized data to the output file
# with open(output_file_path, 'w') as outfile:
#     json.dump(normalized_data, outfile, indent=4)
#
# # Optionally, print the normalized data
# for product in normalized_data:
#     print(product)