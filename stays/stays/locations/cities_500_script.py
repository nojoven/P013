import json
import os

def format_cities_500():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, 'cities500.json')
    # Load the input data
    with open(json_file_path, 'r') as f:
        input_data = json.load(f)

    # Convert the input data to the desired format
    output_data = {}
    for item in input_data:
        city_name = item.pop('name')  # Remove the 'name' key and get its value
        output_data[city_name] = item

    # Write the output data to a new JSON file
    with open('C:\Users\Me\Downloads\cities_500_keys.json', 'w') as f:
        json.dump(output_data, f)

if __name__ == '__main__':
    format_cities_500()