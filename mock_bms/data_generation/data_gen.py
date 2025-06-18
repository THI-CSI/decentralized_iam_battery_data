import ctypes
import json
#import pathlib

def run_battery_data_generator():
    # Load the shared library
    lib = ctypes.CDLL('./libdata_gen_c_v2.so')

    # Define the return type of the function
    lib.process_json_data.restype = ctypes.c_char_p

    # Define the free function
    #lib.free_json_string.argtypes = [ctypes.c_char_p]

    # Call the C function to get the JSON string
    json_string = lib.process_json_data()

    if json_string is not None:
        # Convert the byte string to a regular string
        json_string = json_string.decode('utf-8')

        # Output the JSON string
        #print("Output JSON string:", json_string)

        # Parse the JSON string
        try:
            json_data = json.loads(json_string)
            #print("Parsed JSON data:", json_data)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)

        # Free the allocated JSON string (Causes Errors)
        #lib.free_json_string(json_string.encode('utf-8'))  # Ensure it's in bytes
    else:
        print("Failed to generate JSON string.")

    return json_string

def generate_and_store_data():
    filename = "battery_data.json"
    battery_data = run_battery_data_generator()

    try:
        with open(filename, 'w') as f:
            json.dump(battery_data, f, indent=4)
        print(f"Data has been written to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def retrieve_stored_battery_data():
    filename = "battery_data.json"

    try:
        with open(filename, 'r') as f:
            battery_data = json.load(f)
        print("Data loaded successfully:")
        return battery_data
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
        return None
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
