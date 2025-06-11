import ctypes
import json

def process_json_gen_output():
    # Load the shared library
    lib = ctypes.CDLL('./libdata_gen.so')

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
