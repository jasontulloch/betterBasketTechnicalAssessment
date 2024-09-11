import pandas as pd
from rapidfuzz import fuzz, process
import os
import json
import concurrent.futures

def perform_fuzzy_matching(grocery_store_a_path, grocery_store_b_path, output_file_path):

    # Read the JSON files
    with open(grocery_store_a_path, 'r') as file_a:
        dataA = json.load(file_a)

    with open(grocery_store_b_path, 'r') as file_b:
        dataB = json.load(file_b)

    # Convert JSON data to DataFrames
    dfA = pd.DataFrame(dataA)
    dfB = pd.DataFrame(dataB)

    # Preprocess the DataFrames by lowercasing relevant fields (avoid doing this in loops)
    dfA['name_lower'] = dfA['name'].str.lower()
    dfB['name_lower'] = dfB['name'].str.lower() + ' ' + dfB['itemVariant'].str.lower().fillna('')

    dfA['category_concat'] = dfA[['category', 'category2', 'category3']].fillna('').agg(' -> '.join, axis=1)
    dfB['category_concat'] = dfB[['category', 'category2', 'category3']].fillna('').agg(' -> '.join, axis=1)


    # Helper function to safely concatenate category strings, handling None values
    def safe_concat(*args):
        return ' -> '.join(arg for arg in args if arg)


    # Define a function to compute fuzzy matching with weighted categories
    def fuzzy_match(rowA):
        matches = []

        rowA_name = rowA['name_lower']
        rowA_category = rowA['category_concat'].lower()

        for _, rowB in dfB.iterrows():
            name_score = fuzz.ratio(rowA_name, rowB['name_lower'])
            category_score = fuzz.ratio(rowA_category, rowB['category_concat'].lower())

            # Weighting the scores
            score = (name_score * 0.9) + (category_score * 0.1)

            matches.append((rowB, score))

        return matches


    # Perform fuzzy matching using parallel processing
    def process_row(index, rowA):
        if rowA is None:
            print(f"Skipping row {index + 1} because it is None.")
            return []

        print(f"Processing row {index + 1} of {total_rows}")

        all_matches = fuzzy_match(rowA)
        results = []
        for match, score in all_matches:
            if score > 60:
                # Handle None values for variant labels
                variantLabelA = (rowA.get("variantLabel") or "").lower()
                variantLabelB = (match.get("variantLabel") or "").lower()

                # Handle None values for unit prices
                unitPriceA = rowA.get("unitPrice", 0)  # Default to 0 if None
                unitPriceB = match.get("unitPrice", 0)  # Default to 0 if None

                # Adjust unit price based on variant labels
                if (variantLabelA == "oz" and variantLabelB == "lb") or (variantLabelA == "lb" and variantLabelB == "oz"):
                    unitPriceA = unitPriceA / 16 if variantLabelA == "lb" else unitPriceA
                    unitPriceB = unitPriceB / 16 if variantLabelB == "lb" else unitPriceB

                # Recalculate price discrepancy
                priceDiscrepancy = abs(rowA.get("price", 0) - match.get("price", 0))

                # Set unitPriceDiscrepancy to None if either unitPriceA or unitPriceB is 0
                unitPriceDiscrepancy = None if unitPriceA == 0 or unitPriceB == 0 else abs(unitPriceA - unitPriceB)

                result = {
                    "name": {
                        "nameA": rowA["name"],
                        "nameB": match["name"] + ', ' + match["itemVariant"]
                    },
                    "price": {
                        "priceA": rowA["price"],
                        "priceB": match["price"]
                    },
                    "unitPrice": {
                        "unitPriceA": rowA["unitPrice"],
                        "unitPriceB": match["unitPrice"]
                    },
                    "categories": {
                        "categoryA": safe_concat(rowA.get("category"), rowA.get("category2"), rowA.get("category3")),
                        "categoryB": safe_concat(match.get("category"), match.get("category2"), match.get("category3"))
                    },
                    "variantLabels": {
                        "variantLabelA": rowA["variantLabel"],
                        "variantLabelB": match["variantLabel"]
                    },
                    "priceDiscrepancy": priceDiscrepancy,
                    "unitPriceDiscrepancy": unitPriceDiscrepancy,
                    "score": score
                }
                results.append(result)
        return results


    # Process in batches of 100
    batch_size = 100
    total_rows = len(dfA)
    all_results = []


    def process_batch(start_idx, end_idx):
        batch_results = []
        for index in range(start_idx, end_idx):
            rowA = dfA.iloc[index]
            batch_results.extend(process_row(index, rowA))
        return batch_results


    # Parallel execution with batching
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, total_rows, batch_size):
            start_idx = i
            end_idx = min(i + batch_size, total_rows)
            futures.append(executor.submit(process_batch, start_idx, end_idx))

        for future in concurrent.futures.as_completed(futures):
            all_results.extend(future.result())

    # Sort results by score in descending order
    sorted_results = sorted(all_results, key=lambda x: x['score'], reverse=True)

    # Save results to JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(sorted_results, outfile, indent=4)

    print(f"Results saved to {output_file_path}")
    return sorted_results
