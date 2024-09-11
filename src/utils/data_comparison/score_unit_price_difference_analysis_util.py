import json
import os

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def filter_and_sort_results(input_file_path, output_file_path, min_score, sort_by='unitPriceDiscrepancy'):
    # Load the comparison data
    data = load_json(input_file_path)

    # Filter results based on minimum score
    filtered_results = [item for item in data if item['score'] >= min_score]

    # Check if sorting key exists in data
    if filtered_results and all(sort_by in item for item in filtered_results):
        # Sort results by the specified field
        sorted_results = sorted(filtered_results, key=lambda x: x.get(sort_by, 0), reverse=True)
    else:
        print(f"Sorting field '{sort_by}' is missing in some results or there are no results to sort.")
        sorted_results = filtered_results  # No sorting if field is missing

    # Save the results to the output file
    save_json(sorted_results, output_file_path)

    print(f"Filtered and sorted results saved to {output_file_path}")
