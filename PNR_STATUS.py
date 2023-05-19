import os
import time
import http.client as httplib
import logging
from json import loads
from requests.exceptions import RequestException

PNR_LENGTH = 10
API_ENDPOINT = 'https://mapi.makemytrip.com/api/rails/pnr/currentstatus/v1'
MAX_RETRIES = 3
RETRY_DELAY = 1  # Number of seconds to wait between retries

def clear_screen():
    # Clear screen
    os.system("cls" if os.name == "nt" else "clear")


def check_network_connection():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


def print_pnr_status(json_data):
    train_number = json_data["TrainDetails"]["Train"]["Number"]
    train_name = json_data["TrainDetails"]["Train"]["Name"]
    chart_status = json_data["TrainDetails"]["ChartPrepared"]
    start_station = json_data["StationDetails"]["BoardingPoint"]["name"]
    destination_station = json_data["StationDetails"]["ReservationUpto"]["name"]
    date_of_journey = json_data["PnrDetails"]["SourceDoj"]["FormattedDate"]
    class_name = json_data["PnrDetails"]["Class"]
    quota = json_data["PnrDetails"]["Quota"]

    print("PNR STATUS")
    print("------------------------------------------------------------------")
    print(f"{start_station} -> {destination_station}")
    print(f"{train_number} - {train_name}\n")
    print("Chart Prepared?:", chart_status)
    print("Quota:", quota)
    print("Class:", class_name)
    print("Date Of Journey:", date_of_journey, "\n")

    for passenger in json_data["PassengerDetails"]["PassengerStatus"]:
        print(f"Passenger {passenger['Number']}: {passenger['CurrentStatus']}")


def install_required_libraries():
    required_libraries = ["argparse", "requests", "fake_useragent"]

    missing_libraries = []
    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            missing_libraries.append(library)

    if missing_libraries:
        print("Required libraries not found. Trying to install them...")
        for library in missing_libraries:
            os.system(f"pip install {library}")
            try:
                __import__(library)
            except ImportError:
                print(f"Failed to install {library}. Please install it manually.")
                return False

        clear_screen()  # Clear the screen after installing missing libraries

    return True


def get_pnr_status(pnr):
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
        except RequestException as e:
            logging.error(f"An error occurred while making the API request: {str(e)}")
            time.sleep(RETRY_DELAY)
            exit(1)
        except Exception as e:
            logging.error(str(e))
            time.sleep(RETRY_DELAY)
            exit(1)

    return json_data


def validate_pnr(pnr):
    if len(pnr) != PNR_LENGTH or not pnr.isdigit():
        raise ValueError("PNR should be a 10-digit number.")


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(description="Check PNR status.")
    parser.add_argument("pnr", type=str, help="PNR number")
    return parser.parse_args()


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def process_pnr_status(pnr):
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
