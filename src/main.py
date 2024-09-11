from utils.key_finders.json_keys_util import get_json_keys
from utils.key_finders.nested_json_keys_util import get_nested_json_keys
from utils.data_extractors.store_a_key_extractor_util import get_product_values
from utils.data_extractors.store_b_html_extractor_util import extract_html_data
from utils.data_normalization.store_a_normalizer_util import normalize_a_products
from utils.data_normalization.store_b_normalizer_util import normalize_b_products
from utils.data_comparison.fuzzy_match_price_difference_util import perform_fuzzy_matching
from utils.data_normalization.variant_normalizer import perform_variant_normalization
from utils.data_comparison.score_unit_price_difference_analysis_util import filter_and_sort_results

import os
import json

def main():
    input_file_path_store_a_raw = os.path.join(os.path.dirname(__file__), 'data/grocery_items_raw', 'grocery_store_a.json')
    input_file_path_store_b_raw = os.path.join(os.path.dirname(__file__), 'data/grocery_items_raw', 'grocery_store_b.json')

    output_file_path_store_a_clean = os.path.join(os.path.dirname(__file__), 'test/data/grocery_items_clean/grocery_store_a_items.json')
    output_file_path_store_b_clean = os.path.join(os.path.dirname(__file__), 'test/data/grocery_items_clean/grocery_store_b_items.json')

    # Steps
    # Part I: Refer to README

    # Part II: Understanding the data
    # Store A
    # Return all unique keys at Store A
    store_a_unique_keys = get_json_keys(input_file_path_store_a_raw)
    print(f"Review all Store A keys {store_a_unique_keys}")

    # Return all unique 2nd level nested keys at Store A
    store_a_unique_second_level_keys = get_nested_json_keys(input_file_path_store_a_raw)
    print(f"Review second level Store A keys {store_a_unique_second_level_keys}")

    # Extract clean product data from Store A
    store_a_product_values = get_product_values(input_file_path_store_a_raw)
    print("Extracted Store A product values")

    # Write the clean Store A data to the output file
    with open(output_file_path_store_a_clean, 'w') as outfile:
        json.dump(store_a_product_values, outfile, indent=4)

    # Store B
    # Return all unique keys at Store B
    store_b_unique_keys = get_json_keys(input_file_path_store_b_raw)
    print(f"Review all Store B keys {store_b_unique_keys}")

    # Return all unique 2nd level nested keys at Store B
    store_b_unique_second_level_keys = get_nested_json_keys(input_file_path_store_b_raw)
    print(f"Review second level Store B keys {store_b_unique_second_level_keys}")

    # Extract clean product data from Store B
    store_b_product_values = extract_html_data(input_file_path_store_b_raw)
    print("Extracted Store B product values")

    # Write the clean Store B data to the output file
    with open(output_file_path_store_b_clean, 'w') as outfile:
        json.dump(store_b_product_values, outfile, indent=4)

    # Part III: Normalize the data
    input_file_path_store_a_clean = os.path.join(os.path.dirname(__file__), 'test/data/grocery_items_clean', 'grocery_store_a_items.json')
    input_file_path_store_b_clean = os.path.join(os.path.dirname(__file__), 'test/data/grocery_items_clean', 'grocery_store_b_items.json')

    output_file_path_store_a_normalized = os.path.join(os.path.dirname(__file__), 'test/data/grocery_items_normalized/grocery_store_a_items.json')
    output_file_path_store_b_normalized = os.path.join(os.path.dirname(__file__), 'test/data/grocery_items_normalized/grocery_store_b_items.json')

    # Store A
    try:
        print("Normalizing Store A data")
        # Read the input file
        with open(input_file_path_store_a_clean, 'r') as infile:
            products = json.load(infile)

        # Normalize the products
        normalized_store_a_data = normalize_a_products(products)

        # Write the normalized data to the output file
        with open(output_file_path_store_a_normalized, 'w') as outfile:
            json.dump(normalized_store_a_data, outfile, indent=4)

    except Exception as e:
        print(f"Error processing Store A data: {e}")

    # Store B
    try:
        print("Normalizing Store B data")
        # Read the input file
        with open(input_file_path_store_b_clean, 'r') as infile:
            products = json.load(infile)

        # Normalize the products
        normalized_store_b_data = normalize_b_products(products)

        # Write the normalized data to the output file
        with open(output_file_path_store_b_normalized, 'w') as outfile:
            json.dump(normalized_store_b_data, outfile, indent=4)

    except Exception as e:
        print(f"Error processing Store B data: {e}")

    # Part IV: Comparing the data
    # TESTING: Using existing normalized data (you can access real-time data in test/data...)
    print("Comparing Store A and Store B data")
    input_file_path_store_a_normalized = os.path.join(os.path.dirname(__file__), 'data/grocery_items_normalized/grocery_store_a_items.json')
    input_file_path_store_b_normalized = os.path.join(os.path.dirname(__file__), 'data/grocery_items_normalized/grocery_store_b_items.json')
    output_file_path = os.path.join(os.path.dirname(__file__), 'test/results/step_1_score_comparison.json')

    perform_fuzzy_matching(input_file_path_store_a_normalized, input_file_path_store_b_normalized, output_file_path)
    print("Performed fuzzy match on all grocery items")

    # Normalize data, specifically pounds to ounces for unit price comparison
    input_score_comparison_file_path = os.path.join(os.path.dirname(__file__), 'test/results/step_1_score_comparison.json')
    output_score_comparison_file_path = os.path.join(os.path.dirname(__file__), 'test/results/step_2_measurement_normalization.json')

    perform_variant_normalization(input_score_comparison_file_path, output_score_comparison_file_path)
    print("Normalized variant data for analysis")

    # Return final results
    input_file_path_normalized_score_data = os.path.join(os.path.dirname(__file__), 'test/results/step_2_measurement_normalization.json')
    output_file_path_price_comparison = os.path.join(os.path.dirname(__file__), 'test/results/step_3_price_comparison.json')

    filter_and_sort_results(input_file_path_normalized_score_data, output_file_path_price_comparison, min_score=90.0, sort_by='unitPriceDiscrepancy')
    print('Analysis complete! Grocery Store A and B products have been fuzzy matched by name, category, and variant. Unit price discrepancies appear in descending order (Note: outliers may be present in the first few discrepancies due to variant mismatches)')

if __name__ == "__main__":
    main()