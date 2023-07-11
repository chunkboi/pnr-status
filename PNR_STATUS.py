import time
import logging
import http.client as httplib
from json import loads
import argparse
import subprocess


PNR_LENGTH = 10
API_ENDPOINT = 'https://mapi.makemytrip.com/api/rails/pnr/currentstatus/v1'
MAX_RETRIES = 3
RETRY_DELAY = 1  # Number of seconds to wait between retries


def clear_screen():
    """Clears the console screen."""
    print("\033[2J")


def check_network_connection():
    """Checks the network connection by pinging a server.

    Returns:
        bool: True if the network connection is available, False otherwise.
    """
    conn = None
    try:
        conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        if conn is not None:
            conn.close()


def install_required_libraries():
    """Installs the required libraries if they are not found.

    Returns:
        bool: True if all required libraries are installed or already present,
              False if any library installation fails.
    """
    required_libraries = ["requests", "colorama"]

    missing_libraries = []
    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            missing_libraries.append(library)

    if missing_libraries:
        print("Required libraries not found. Trying to install them...")
        for library in missing_libraries:
            subprocess.check_call(['pip', 'install', library])
            try:
                __import__(library)
            except ImportError:
                print(f"Failed to install {library}. Please install it manually.")
                return False

        clear_screen()  # Clear the screen after installing missing libraries

    return True


def print_pnr_status(json_data):
    """Prints the PNR status details extracted from the JSON data.

    Args:
        json_data (dict): JSON data containing PNR status details.
    """
    import colorama
    from colorama import Fore, Style
    train_number = json_data["TrainDetails"]["Train"]["Number"]
    train_name = json_data["TrainDetails"]["Train"]["Name"]
    chart_status = json_data["TrainDetails"]["ChartPrepared"]
    start_station = json_data["StationDetails"]["BoardingPoint"]["name"]
    destination_station = json_data["StationDetails"]["ReservationUpto"]["name"]
    date_of_journey = json_data["PnrDetails"]["SourceDoj"]["FormattedDate"]
    class_name = json_data["PnrDetails"]["Class"]
    quota = json_data["PnrDetails"]["Quota"]

    separator = "-" * 70

    print(Fore.YELLOW + Style.BRIGHT + "PNR STATUS".center(70) + Style.RESET_ALL)
    print(separator)
    print(f"Train: {train_number} - {train_name}".center(70))
    print(Fore.CYAN + f"Route: {start_station} -> {destination_station}".center(70) + Style.RESET_ALL)
    print(Fore.RED + f"Date of Journey: {date_of_journey}".center(70) + Style.RESET_ALL)
    print(Fore.RED + f"Class: {class_name}".center(70) + Style.RESET_ALL)
    print(Fore.RED + f"Quota: {quota}".center(70) + Style.RESET_ALL)
    print(Fore.MAGENTA + f"Chart Prepared: {chart_status}".center(70) + Style.RESET_ALL)
    print(separator)

    print(Fore.YELLOW + Style.BRIGHT + "Passenger Details:".center(70) + Style.RESET_ALL)
    for passenger in json_data["PassengerDetails"]["PassengerStatus"]:
        passenger_info = f"Passenger {passenger['Number']}: {passenger['CurrentStatus']}"
        print(Fore.GREEN + passenger_info.center(70) + Style.RESET_ALL)

    print(separator)

def get_pnr_status(pnr):
    """Retrieves the PNR status by making an API request.

    Args:
        pnr (str): PNR number.

    Returns:
        dict: JSON data containing the PNR status details.
    """
    import requests
    from fake_useragent import UserAgent

    json_data = None

    json = {
        'pnrID': pnr,
        'trackingParams': {
            'affiliateCode': 'MMT001',
            'channelCode': 'WEB',
        },
    }
    headers = {
        'accept': 'application/json',
        'user-agent': UserAgent().random,
    }
    for _ in range(MAX_RETRIES):
        try:
            response = requests.post(API_ENDPOINT, headers=headers, json=json)
            response.raise_for_status()
            json_data = loads(response.content)
            break  # Break the loop if the request is successful
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred while making the API request: {str(e)}")
            time.sleep(RETRY_DELAY)
            exit(1)
        except Exception as e:
            logging.error(str(e))
            time.sleep(RETRY_DELAY)
            exit(1)

    return json_data


def validate_pnr(pnr):
    """Validates the PNR number.

    Args:
        pnr (str): PNR number.

    Raises:
        ValueError: If the PNR number is not a 10-digit number.
    """
    if len(pnr) != PNR_LENGTH or not pnr.isdigit():
        raise ValueError("PNR should be a 10-digit number.")


def parse_arguments():
    """Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Check PNR status.")
    parser.add_argument("pnr", type=str, help="PNR number")
    return parser.parse_args()


def setup_logging():
    """Sets up the logging configuration."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def process_pnr_status(pnr):
    """Processes the PNR status by performing necessary checks and retrieving the status.

    Args:
        pnr (str): PNR number.
    """
    setup_logging()

    if not install_required_libraries():
        return

    try:
        validate_pnr(pnr)
    except ValueError as e:
        logging.error(str(e))
        return

    if not check_network_connection():
        logging.error("Please connect to a network to check PNR status.")
        return

    start_time = time.perf_counter()

    json_data = get_pnr_status(pnr)

    end_time = time.perf_counter()

    if json_data is None:
        logging.error("Failed to retrieve PNR status.")
        return

    if "Error" in json_data:
        error_message = json_data["Error"]["message"]
        logging.error(error_message)
        logging.info("Total time taken: %s seconds", round(end_time - start_time, 3))
        return

    print_pnr_status(json_data)
    logging.info("Total time taken: %s seconds", round(end_time - start_time, 3))


if __name__ == "__main__":
    clear_screen()

    args = parse_arguments()
    pnr = args.pnr

    process_pnr_status(pnr)
