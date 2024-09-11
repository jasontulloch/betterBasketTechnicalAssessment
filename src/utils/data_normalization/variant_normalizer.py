import json
import os

def perform_variant_normalization(input_score_comparison_file_path, output_score_comparison_file_path):
    # Load the data from the JSON file
    with open(input_score_comparison_file_path, 'r') as file:
        data = json.load(file)

    def convert_lb_to_oz(unit_price, variant_label):
        if variant_label == 'lb':
            return unit_price / 16, 'oz'  # Convert lb to oz and return new label
        return unit_price, variant_label  # No conversion needed

    def normalize_data(data):
        for item in data:
            try:
                # Debug: Print original item
                print("Original item:", item)

                variantLabelA = (item.get("variantLabels", {}).get("variantLabelA") or "").lower()
                variantLabelB = (item.get("variantLabels", {}).get("variantLabelB") or "").lower()

                unitPriceA = item.get("unitPrice", {}).get("unitPriceA", 0)
                unitPriceB = item.get("unitPrice", {}).get("unitPriceB", 0)

                # Debug: Print before conversion
                print(f"Before conversion: unitPriceA={unitPriceA}, variantLabelA={variantLabelA}")
                print(f"Before conversion: unitPriceB={unitPriceB}, variantLabelB={variantLabelB}")

                # Convert both to oz if necessary
                unitPriceA, variantLabelA = convert_lb_to_oz(unitPriceA, variantLabelA)
                unitPriceB, variantLabelB = convert_lb_to_oz(unitPriceB, variantLabelB)

                # Debug: Print after conversion
                print(f"After conversion: unitPriceA={unitPriceA}, variantLabelA={variantLabelA}")
                print(f"After conversion: unitPriceB={unitPriceB}, variantLabelB={variantLabelB}")

                # Update item
                item["unitPrice"] = {
                    "unitPriceA": unitPriceA,
                    "unitPriceB": unitPriceB
                }
                item["variantLabels"] = {
                    "variantLabelA": variantLabelA,
                    "variantLabelB": variantLabelB
                }

                # Recalculate unitPriceDiscrepancy
                item["unitPriceDiscrepancy"] = abs(unitPriceA - unitPriceB)

                # Debug: Print updated item
                print("Updated item:", item)

            except Exception as e:
                print(f"Error processing item {item}: {e}")
                continue

        return data

    # Normalize the data
    normalized_data = normalize_data(data)

    # Save the normalized data to a new JSON file
    with open(output_score_comparison_file_path, 'w') as file:
        json.dump(normalized_data, file, indent=4)

    print("Normalization complete. Data saved to 'results/step_2_measurement_normalization.json'.")
    return normalized_data
