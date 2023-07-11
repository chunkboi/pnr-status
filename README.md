# PNR Status Checker

This script allows you to check the status of a Passenger Name Record (PNR) for Indian Railways. It performs the following tasks:

1. Accepts a 10-digit PNR number from the user.
2. Encrypts the PNR number using AES CBC encryption with PKCS7 padding.
3. Sends a POST request to the `https://railways.easemytrip.com/Train/PnrchkStatus` API endpoint with the encrypted PNR.
4. Parses the response from the API and prints the formatted PNR status information, including boarding station, destination station, quota, class name, train number, train name, date of journey, and passenger details.
5. Displays the total time taken to complete the program execution.

## Prerequisites

To run this script, you need to have the following:

- Python 3.x installed on your system. You can download and install Python from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

## How to Use

1. Clone the repository or download the script file (`PNR_STATUS.py`).
2. Open a terminal or command prompt.
3. Navigate to the directory where the script is located.
4. Run the script using the command: `python PNR_STATUS.py`.
5. Follow the prompts to enter the 10-digit PNR number when prompted.

## Automatic Package Installation

If the required packages (`cryptography` and `requests`) are not already installed on your system, the script will attempt to install them automatically.

Note: This automatic installation requires an internet connection and assumes that `pip` is available and associated with the correct Python interpreter on your system.

If you encounter any issues with the automatic package installation, you can manually install the required packages using the following commands:
`pip install cryptography requests`


[![CodeQL](https://github.com/chunkboi/pnr-status/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/codeql-analysis.yml)
[![OSSAR](https://github.com/chunkboi/pnr-status/actions/workflows/ossar.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/ossar.yml)
[![Codacy Security Scan](https://github.com/chunkboi/pnr-status/actions/workflows/codacy.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/codacy.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/chunkboi/pnr-status/badge)](https://www.codefactor.io/repository/github/chunkboi/pnr-status)
[![DeepSource](https://deepsource.io/gh/chunkboi/pnr-status.svg/?label=active+issues&show_trend=true&token=8c9BSEqF2nTvN-EmrdZDeAAR)](https://deepsource.io/gh/chunkboi/pnr-status/)

# DISCLAIMER
Author is not responsible for any losses incurrred to any individual, company or property either directly or indirectly as a result of using this script. Also, there is no warranty of any kind with this script.
