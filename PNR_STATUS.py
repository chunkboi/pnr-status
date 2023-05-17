import requests
import os
import time
import http.client as httplib


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
        response = requests.post('https://mapi.makemytrip.com/api/rails/pnr/currentstatus/v1', headers=headers,
                                 json=json)
        response.raise_for_status()
        json_data = loads(response.content)
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the API request:", str(e))
    except ValueError:
        print("Invalid JSON data received from the API.")

    return json_data


def main():
    clear_screen()

    if not install_required_libraries():
        return

    pnr = input("Enter PNR number: ")

    if len(pnr) != 10 or not pnr.isdigit():
        print("PNR should be a 10-digit number.")
        return

    if not check_network_connection():
        print("Please connect to a network to check PNR status.")
        return

    start_time = time.perf_counter()

    json_data = get_pnr_status(pnr)

    end_time = time.perf_counter()

    if json_data is None:
        print("Failed to retrieve PNR status.")
        return

    if "Error" in json_data:
        print(json_data["Error"]["message"])
        print(f"Total time taken: {round(end_time - start_time, 3)} seconds")
        return

    print_pnr_status(json_data)
    print(f"Total time taken: {round(end_time - start_time, 3)} seconds")


if __name__ == "__main__":
    main()
