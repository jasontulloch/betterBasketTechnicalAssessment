import os
import json
import re
from googletrans import Translator, constants

# Set to store unique labels
unique_labels = set()

# Initialize the translator
translator = Translator()

# Extract and normalize the label and amount from the item variant string
def extract_variant_details(item_variant):
    if not item_variant:
        return {"label": None, "amount": None}

    # Normalize the item_variant string
    item_variant = item_variant.strip().lower()

    # Extract the numeric part (including the period) and text part
    amount_match = re.search(r'(\d*\.?\d+)', item_variant)
    amount_str = amount_match.group(0) if amount_match else None

    # Extract the remaining text after the numeric part
    if amount_str:
        remaining_text = re.sub(re.escape(amount_str), '', item_variant).strip()
    else:
        remaining_text = item_variant

    # Clean up the label
    label = remaining_text

    # Special case handling
    if label == 'por peso':
        label = 'by weight'

    # Convert amount to a number (float) if applicable
    try:
        amount = float(amount_str) if amount_str else None
    except ValueError:
        amount = None

    unique_labels.add(label)

    return {"label": label, "amount": amount}

# Normalize a list of product dictionaries by formatting prices, translating names and categories, and extracting variant details
def normalize_b_products(products):

    normalized = []

    for product in products:
        # Extract variant details
        variant_details = extract_variant_details(product.get("item_variant", None))

        variant_label = variant_details.get("label", None)
        variant_amount_str = variant_details.get("amount", None)
        try:
            variant_amount_number = float(variant_amount_str) if variant_amount_str else None
        except ValueError:
            variant_amount_number = None

        # Special case handling
        if variant_label == '/oz':
            variant_amount_number = variant_amount_number if variant_amount_number else None

        # Translate the product name
        original_name = product.get("name", None)
        try:
            translation = translator.translate(original_name)
            translated_name = translation.text
        except ValueError:
            translated_name = None

        # Calculate unit price if applicable
        price = product.get("price", None)
        if price is not None and variant_amount_number is not None:
            try:
                unit_price = price / variant_amount_number
                if variant_label:
                    formatted_unit_price = f"${unit_price} / {variant_label}"
                else:
                    formatted_unit_price = f"${unit_price}"
            except ZeroDivisionError:
                unit_price = None
                formatted_unit_price = None
            except TypeError:
                unit_price = None
                formatted_unit_price = None
        else:
            unit_price = None
            formatted_unit_price = None

        # Format price for string
        if price is not None:
            formatted_price = f"${price:.2f}"
        else:
            formatted_price = None

        # Translate categories and list name
        category = product.get("item_category", None)
        category2 = product.get("item_category2", None)
        category3 = product.get("item_category3", None)
        listName = product.get("item_list_name", None)

        try:
            translation = translator.translate(category)
            category = translation.text
        except ValueError:
            category = None

        try:
            translation = translator.translate(category2)
            category2 = translation.text
        except ValueError:
            category2 = None

        try:
            translation = translator.translate(category3)
            category3 = translation.text
        except ValueError:
            category3 = None

        try:
            print('Attempting translation')
            translation = translator.translate(listName)
            print(translation)
            listName = translation.text
        except ValueError:
            listName = None

        # Construct the normalized product dictionary
        normalized_product = {
            "name_translated": translated_name,
            "name": original_name,
            "price": price,
            "priceString": formatted_price,
            "unitPrice": unit_price,
            "unitPriceString": formatted_unit_price,
            "category": category,
            "category2": category2,
            "category3": category3,
            "listName": listName,
            "itemVariant": product.get("item_variant", None),
            "variantLabel": variant_label,
            "variantAmount": variant_amount_number
        }
        normalized.append(normalized_product)

    return normalized


# input_file_path = os.path.join(os.path.dirname(__file__), './../../data/grocery_items_clean', 'grocery_store_b_items.json')
# output_file_path = os.path.join(os.path.dirname(__file__), './../../data/grocery_items_normalized/grocery_store_b_items.json')
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
#     print(unique_labels)
#     # print(unique_name_counts)