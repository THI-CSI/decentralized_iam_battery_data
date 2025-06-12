import argparse, sys, time
from key_gen import bms_signing_key_pair_generation
from data_gen import generate_and_store_data
from utils import data_exchange

# Hardcoded API URLs
CLOUD_API_URL = 'http://127.0.0.1:8000/batterypass/'
BLOCKCHAIN_API_URL = 'http://localhost:8080/api/v1/dids/'

# Todo: Add function call for VC signing

def cli():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Adding arguments
    parser.add_argument('--generate-keys', action='store_true', help='Generates keypair for signing')
    parser.add_argument('--generate-data', action='store_true', help='Generates data')
    parser.add_argument('--data-exchange', action='store_true', help='Communicates with Cloud and Blockchain')
    parser.add_argument('--sign-vc', action='store_true', help='Signs received VC and sends it back')
    parser.add_argument('--automate', action='store_true', help='Generates new data and submits it every minute')

    # Parsing arguments
    args = parser.parse_args()

    # Generates the BMS Signing Key Pair and prints it on screen
    if args.generate_keys:
        print(f"Generating keys!")
        print(bms_signing_key_pair_generation())
        print(bms_signing_key_pair_generation().public_key())
    # Generates Battery Pass Data and stores it in a JSON file
    if args.generate_data:
        print(f"Generating data!")
        generate_and_store_data()
    # Performs the following actions:
    # - Loads saved Batterypass data
    # - Gets Cloud DID from Blockchain and extracts Public Key of Cloud
    # - Loads Key Pair
    # - Creates shared secret, encrypts data and signs message.
    # - Posts message to the Cloud
    if args.data_exchange:
        print(f"Exchanging data!")
        data_exchange(BLOCKCHAIN_API_URL, CLOUD_API_URL, False)
    if args.sign_vc:
        print(f"Signing VC!")
        # Call function with vc verification logic
    # Performs the same actions as the data-exchange flag, but repeats all steps every 60 seconds
    if args.automate:
        print(f"Started Automation!")
        print(f"Exit with Ctrl + c")
        while True:
            data_exchange(BLOCKCHAIN_API_URL, CLOUD_API_URL, True)
            print(f"Waiting for 60 Seconds.")
            time.sleep(60)
            print(f"Resending...")
    # Wrong or no argument provided
    if not any(vars(args).values()):
        print(f"Error")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    cli()

