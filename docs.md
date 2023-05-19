# PNR Status Checker Documentation

This documentation provides a detailed explanation of the PNR Status Checker script, which is used to check the status of a Passenger Name Record (PNR) for Indian Railways. The script is written in Python and utilizes various libraries and APIs to retrieve and display the PNR status.

## Prerequisites

- Python 3.x

Ensure that Python 3.x is installed on your system. The script will automatically install the required libraries if they are missing.

## Script Overview

The PNR Status Checker script performs the following tasks:

1. Imports the necessary libraries and modules.
2. Defines constants for the PNR length and the API endpoint.
3. Defines utility functions for clearing the screen, checking network connectivity, printing the PNR status, and installing required libraries.
4. Defines the main functions for retrieving and processing the PNR status.
5. Parses command-line arguments.
6. Sets up logging.
7. Executes the main script logic.

## Functions and Classes

### 1. `clear_screen()`

This function clears the console screen. It uses the `os` module and calls the appropriate system command based on the operating system.

### 2. `check_network_connection()`

This function checks the network connection by establishing a connection with a well-known IP address (`8.8.8.8`). It uses the `http.client` module to send an HTTP `HEAD` request and returns `True` if the connection is successful, otherwise `False`.

### 3. `print_pnr_status(json_data)`

This function takes the JSON data representing the PNR status and prints the relevant information in a formatted manner. It extracts information such as train details, chart preparation status, station details, date of journey, class, quota, and passenger details.

### 4. `install_required_libraries()`

This function checks if the required libraries (`argparse`, `requests`, and `fake_useragent`) are installed. If any library is missing, it attempts to install them using the `os` module and the `pip` command. It returns `True` if all required libraries are installed or successfully installed, otherwise `False`.

### 5. `get_pnr_status(pnr)`

This function takes a PNR number as input and retrieves the PNR status using the MakeMyTrip API. It sends a POST request to the API endpoint with the PNR number and other tracking parameters. The response is received in JSON format and parsed using the `json.loads()` function. The parsed JSON data is returned.

### 6. `validate_pnr(pnr)`

This function validates the format of the PNR number. It checks if the PNR number has the correct length (10 digits) and consists only of digits. If the PNR number is invalid, it raises a `ValueError` with an appropriate error message.

### 7. `parse_arguments()`

This function parses the command-line arguments using the `argparse` module. It defines a single positional argument `pnr` for the PNR number. The parsed arguments are returned.

### 8. `setup_logging()`

This function sets up logging configuration using the `logging` module. It configures the logging level to `INFO` and the log message format.

### 9. `process_pnr_status(pnr)`

This function is the main entry point of the script. It sets up the logging, installs the required libraries, validates the PNR number, checks the network connection, retrieves the PNR status, and prints the status if successful. The total time taken for the process is logged.

### 10. `__name__ == "__main__"`

This condition is used to ensure that the script is run directly and not imported as a

 module. It clears the screen, installs the required libraries if necessary, parses the command-line arguments, and calls the `process_pnr_status()` function with the provided PNR number.

## Usage

To use the PNR Status Checker script, follow these steps:

1. Ensure that Python 3.x is installed on your system.
2. Open a terminal or command prompt.
3. Navigate to the directory where the script is saved.
4. Run the script with the following command:

```
python pnr_status_checker.py <pnr_number>
```

Replace `<pnr_number>` with the actual PNR number you want to check.

## Example

```
python pnr_status_checker.py 1234567890
```

This command will check the PNR status for the PNR number `1234567890`.

## Conclusion

The PNR Status Checker script provides a convenient way to check the status of a PNR for Indian Railways. By following the steps outlined in this documentation, you can easily utilize the script to retrieve and display the PNR status information.
