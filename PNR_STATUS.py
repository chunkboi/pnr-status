import subprocess

REQUIRED_PACKAGES = ['cryptography', 'requests']

# Check if the required packages are installed
for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        # Package is not installed, so attempt to install it
        subprocess.check_call(['pip', 'install', package])


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode
from requests import post
from json import loads
import time
import sys

def clear_screen():
    # Clear screen
    print("\033[2J")
    
def encrypt_pnr(pnr):
    """Encrypts the PNR number using AES CBC encryption with PKCS7 padding.

    Args:
        pnr (str): The PNR number to encrypt.

    Returns:
        str: The base64-encoded encrypted PNR.

    """
    data = bytes(pnr, 'utf-8')
    backend = default_backend()
    padder = padding.PKCS7(128).padder()

    data = padder.update(data) + padder.finalize()
    key = b'8080808080808080'
    iv = b'8080808080808080'
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    enc_pnr = b64encode(ct)
    return enc_pnr.decode('utf-8')

def print_pnr_data(json_data):
    """Prints the formatted PNR status information.

    Args:
        json_data (dict): JSON data containing the PNR status information.

    Raises:
        KeyError: If the required keys are missing in the JSON data.

    """
    try:
        boarding_station = json_data["BrdPointName"]
        destination_station = json_data["DestStnName"]
        quota = json_data["quota"]
        class_name = json_data["className"]
        train_number = json_data["trainNumber"]
        train_name = json_data["trainName"]
        date_of_journey = json_data["dateOfJourney"]

        print("PNR STATUS")
        print("------------------------------------------------------------------")
        print(f"{boarding_station} -> {destination_station}")  # source and destination station
        print(f"{train_number} - {train_name}")  # train number and name
        print()
        print(f"Quota: {quota}")
        print(f"Journey Class: {class_name}")
        print(f"Date Of Journey: {date_of_journey}")
        print()
        for passenger in json_data["passengerList"]:
            passenger_serial_number = passenger["passengerSerialNumber"]
            current_status = passenger["currentStatus"]
            current_coach_id = passenger["currentCoachId"]
            current_berth_no = passenger["currentBerthNo"]
            print(f"Passenger {passenger_serial_number}: {current_status}/{current_coach_id}/{current_berth_no}")
    except KeyError as e:
        raise KeyError("Invalid JSON data format. Missing key: " + str(e))

def main():
    clear_screen()

    pnr = input("Enter PNR Number: ")
    start_time = time.time()

    # Input validation: PNR should be 10 digits
    if len(pnr) != 10:
        print("PNR LENGTH should be 10 DIGITS")
        sys.exit(1)

    encrypted_pnr = encrypt_pnr(pnr)

    json_data = {
        'pnrNumber': encrypted_pnr,
    }

    try:
        # Perform a POST request to the API endpoint with the encrypted PNR
        response = post('https://railways.easemytrip.com/Train/PnrchkStatus', json=json_data, verify=True)
        response.raise_for_status()
        json_data = loads(response.content)
    except (ConnectionError, TimeoutError, requests.exceptions.RequestException) as e:
        print("An error occurred while connecting to the API:", str(e))
        sys.exit(1)
    except ValueError as e:
        print("Invalid response from the API. Response cannot be parsed as JSON.", str(e))
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", str(e))
        sys.exit(1)

    clear_screen()
    end_time = time.time()
    
    try:
        print_pnr_data(json_data)
    except KeyError as e:
        print("An error occurred while parsing the API response:", str(e))
        sys.exit(1)
        
    print(f"Total time taken: {round(end_time - start_time, 3)} seconds")

if __name__ == "__main__":
    main()
