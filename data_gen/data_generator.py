import random, csv, json, string, uuid, requests
from tabulate import tabulate
from datetime import datetime, timedelta, date

##### Modifiable values to adjust seed and output size #####
SEED = 42
NUM_ROWS = 10
#### End of Modifiable #####

random.seed(SEED)

# Simple random data generator for different data types.
def generate_random_data(column_configs):
    data_2d_array = []
    for config in column_configs:
        column_type = config['type']
        null_probability = config.get('null_probability', 0) # default = 0
        if column_type == 'unique_id':
            # Generate unique IDs (UUIDs)
            data_2d_array.append([str(uuid.uuid4()) for _ in range(NUM_ROWS)])
        elif column_type == 'unique_id_2':# Generate custom unique IDs
            # Generate custom unique IDs
            length = config.get('length', 12)  # default length
            data_2d_array.append([
                ''.join(random.choices(string.ascii_letters + string.digits, k=length)) if random.random() > null_probability else None
                for _ in range(NUM_ROWS)
            ])
        elif column_type == 'integer':
            min_val = config.get('min', 1)
            max_val = config.get('max', 100)
            data_2d_array.append([
                random.randint(min_val, max_val) if random.random() > null_probability else None for _ in
                range(NUM_ROWS)
            ])
        elif column_type == 'float':
            min_val = config.get('min', 1.0)
            max_val = config.get('max', 100.0)
            float_digits = config.get('float_digits', 2)  # default: 2 decimal places
            data_2d_array.append([
                round(random.uniform(min_val, max_val), float_digits) if random.random() > null_probability else None
                for _ in
                range(NUM_ROWS)
            ])
        elif column_type == 'keyword':
            keyword_pool = config['params']
            data_2d_array.append([
                random.choice(keyword_pool) if random.random() > null_probability else None for _ in range(NUM_ROWS)
            ])
        elif column_type == 'boolean':
            data_2d_array.append([
                random.choice([True, False]) if random.random() > null_probability else None for _ in range(NUM_ROWS)
            ])
        elif column_type == 'date':
            start_date = config.get('start_date', datetime(2020, 1, 1))
            end_date = config.get('end_date', datetime(2023, 12, 31))
            delta = (end_date - start_date).days
            data_2d_array.append([
                (start_date + timedelta(days=random.randint(0, delta))).date() if random.random() > null_probability else None
                #start_date + timedelta(days=random.randint(0, delta)) if random.random() > null_probability else None
                for _ in range(NUM_ROWS)
            ])
    return data_2d_array

# Saves Data to CSV. For easy readability and debugging purposes.
def save_to_csv(data, filename, headers):
    table_data = list(zip(*data))
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(table_data)

# Saves Data to JSON.
def save_to_json(data, filename):
    json_data = json.dumps(data, default=datetime_serializer)
    with open(filename, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

# Serializes datetime objects for JSON file.
def datetime_serializer(obj):
    if isinstance(obj, date):  # Handle date objects
        return obj.isoformat()  # Convert to ISO 8601 format (date only)
    #if isinstance(obj, datetime):
        #return obj.isoformat()  # Convert to ISO 8601 format
    raise TypeError("Type not serializable")

# Sends a 2D array of data to an API as a JSON payload.
def send_data_over_api(data, api_url):
    # Convert the 2D array data to a list of dictionaries
    headers = [config['name'] for config in column_configs]
    data_dicts = []

    for row in zip(*data):
        row_dict = dict(zip(headers, row))
        # Convert date objects to string using the datetime_serializer
        for key, value in row_dict.items():
            if isinstance(value, date):
                row_dict[key] = datetime_serializer(value)  # Use your existing serializer
        data_dicts.append(row_dict)

    # Send the data as a JSON payload
    try:
        response = requests.post(api_url, json=data_dicts)
        response.raise_for_status()  # Raise an error for bad responses
        print("Data sent successfully:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error sending data:", e)


if __name__ == "__main__":
    # Easily expandable configuration "config":
    column_configs = [
        {'name': 'Battery passport identifier', 'type': 'unique_id', 'null_probability': 0},
        {'name': 'Battery identifier', 'type': 'unique_id_2', 'null_probability': 0},
        {'name': 'Manufacturing place', 'type': 'keyword', 'params': [
            "Tesla Gigafactory 1, Nevada", "LG Energy Solution, South Korea", "Panasonic, Japan",
            "CATL, China", "Samsung SDI, South Korea", "BYD, China", "A123 Systems, USA",
            "SK Innovation, South Korea", "Northvolt, Sweden", "Fengfan, China"
        ], 'null_probability': 0},
        {'name': 'Manufacturing Date', 'type': 'date', 'start_date': datetime(2020, 1, 1),
         'end_date': datetime(2023, 12, 31), 'null_probability': 0},
        {'name': 'Battery Categories', 'type': 'keyword', 'params': [
            "LMT Battery", "Electric Vehicle Battery", "NMC"
        ], 'null_probability': 0},
        {'name': 'Battery mass (kg)', 'type': 'float', 'min': 100.0, 'max': 600.0, 'float_digits': 3, 'null_probability': 0},
        {'name': 'Battery status', 'type': 'keyword', 'params': [
            "original", "repurposed", "reused", "remanufactured", "waste"
        ], 'null_probability': 0},
        {'name': 'Absolute battery carbon footprint (tCO2e)', 'type': 'integer', 'min': 2400, 'max': 18000, 'null_probability': 0},
        {'name': 'Battery chemistry', 'type': 'keyword', 'params': [
                "Lithium-Ion (Li-ion)", "Lithium Nickel Manganese Cobalt (NMC)", "Lithium Iron Phosphate (LiFePO4)",
                "Lithium Nickel Cobalt Aluminum Oxide (NCA)", "Lithium Manganese Oxide (LMO)",
                "Nickel-Metal Hydride (NiMH)", "Solid-State Batteries", "Lead-Acid Batteries", "Ultracapacitors",
                "Flow Batteries"
        ], 'null_probability': 0},
        {'name': 'Rate capacity (Ah)', 'type': 'integer', 'min': 85, 'max': 430, 'null_probability': 0},
        {'name': 'Remaining capacity (Ah)', 'type': 'integer', 'min': 60, 'max': 360, 'null_probability': 0},
        {'name': 'State of Charge (%)', 'type': 'float', 'min': 0, 'max': 100, 'float_digits': 2, 'null_probability': 0},
    ]

    headers = [config['name'] for config in column_configs]

    data_2d_array = generate_random_data(column_configs) # Array that contains all generated data

    # Saves generated Data.
    save_to_csv(data_2d_array, 'generated_data.csv', headers)
    save_to_json(data_2d_array, 'generated_data.json')

    table_data = list(zip(*data_2d_array))

    # Console Output.
    print("Generated Data (Table):")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Submits data to API
    send_data_over_api(data_2d_array, "http://127.0.0.1:5000/data")


# // AI: Load from JSON file (Node.js example)
# fs.readFile('data.json', 'utf8', (err, data) => {
#     if (err) throw err;
#     const loadedData = JSON.parse(data);
#     loadedData.currentTime = new Date(loadedData.currentTime); // Convert back to Date
#     console.log(loadedData);
# });