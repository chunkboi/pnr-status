import os
import time
import requests
import http.client as httplib
from json import loads
import argparse
import logging

PNR_LENGTH = 10
API_ENDPOINT = 'https://mapi.makemytrip.com/api/rails/pnr/currentstatus/v1'


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
    try:
        import requests
        from json import loads
    except ImportError:
        print("Required libraries not found. Trying to install them...")
        os.system("pip install requests")
        try:
            import requests
            from json import loads
        except ImportError:
            print("Failed to install required libraries. Please install 'requests' manually.")
            return False
    return True


def get_pnr_status(pnr):
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=json)
        response.raise_for_status()
        json_data = loads(response.content)
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred while making the API request: %s", str(e))
    except ValueError:
        logging.error("Invalid JSON data received from the API.")

    return json_data


def validate_pnr(pnr):
    if len(pnr) != PNR_LENGTH or not pnr.isdigit():
        raise ValueError("PNR should be a 10-digit number.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Check PNR status.")
    parser.add_argument("pnr", type=str, help="PNR number")
    return parser.parse_args()


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def main():
    clear_screen()
    setup_logging()

    args = parse_arguments()
    pnr = args.pnr

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
        logging.error(json_data["Error"]["message"])
        logging.info("Total time taken: %s seconds", round(end_time - start_time, 3))
        return

    print_pnr_status(json_data)
    logging.info("Total time taken: %s seconds", round(end_time - start_time, 3))


if __name__ == "__main__":
    main()
