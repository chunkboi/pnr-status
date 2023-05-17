# PNR Status Checker

The PNR Status Checker script allows you to check the status of a train ticket using the Passenger Name Record (PNR) number. It retrieves the status by making an API request to the MakeMyTrip API and displays the relevant information.

## Usage

1. Run the script using Python.
2. Enter the 10-digit PNR number when prompted.
3. The script will connect to the API and retrieve the status information.
4. The PNR status, including train details, chart preparation status, passenger details, and journey information, will be displayed.

## Requirements

- Python 3.x
- `requests` library (will be installed automatically if not found)

## Code Structure

The script is organized into the following functions:

1. `clear_screen()`
   - Clears the console screen.

2. `check_network_connection()`
   - Checks the network connection by making a request to a known server.
   - Returns `True` if the connection is successful, `False` otherwise.

3. `print_pnr_status(json_data)`
   - Extracts and prints the PNR status information from the retrieved JSON data.
   - Displays train details, chart preparation status, passenger details, and journey information.

4. `main()`
   - The main function of the script.
   - Checks for required libraries (`requests`, `json`).
   - Prompts the user to enter the PNR number.
   - Validates the PNR number.
   - Checks network connectivity.
   - Makes an API request to the MakeMyTrip API to retrieve the PNR status.
   - Parses and displays the PNR status information.

## How to Run

1. Install Python 3.x from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Save the script in a file (e.g., `pnr_status_checker.py`).
3. Open a command prompt or terminal.
4. Navigate to the directory containing the script.
5. Run the script using the command: `python pnr_status_checker.py`
6. Follow the on-screen prompts to enter the PNR number and view the status.

**Note:**
- Ensure you have an active internet connection to fetch the PNR status information.
- The MakeMyTrip API is used to retrieve the PNR status, so make sure the API is accessible.


[![CodeQL](https://github.com/chunkboi/pnr-status/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/codeql-analysis.yml)
[![OSSAR](https://github.com/chunkboi/pnr-status/actions/workflows/ossar.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/ossar.yml)
[![Codacy Security Scan](https://github.com/chunkboi/pnr-status/actions/workflows/codacy.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/codacy.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/chunkboi/pnr-status/badge)](https://www.codefactor.io/repository/github/chunkboi/pnr-status)
[![DeepSource](https://deepsource.io/gh/chunkboi/pnr-status.svg/?label=active+issues&show_trend=true&token=8c9BSEqF2nTvN-EmrdZDeAAR)](https://deepsource.io/gh/chunkboi/pnr-status/)

# DISCLAIMER

Author is not responsible for any losses incurrred to any individual, company or property either directly or indirectly as a result of using this script. Also, there is no warranty of any kind with this script.
