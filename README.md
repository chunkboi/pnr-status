# PNR Status Checker
# NO LONGER WORKS DEPRECATED 

The PNR Status Checker is a Python script that allows users to check the status of their PNR (Passenger Name Record) for Indian Railways. It retrieves real-time information about the train, chart preparation, and passenger details.

## Features

- Retrieves PNR status details from the MakeMyTrip API.
- Validates the format and length of the PNR.
- Checks network connectivity before making the API request.
- Displays the PNR status information on the console.

## Prerequisites

To run the PNR Status Checker script, ensure that you have the following prerequisites:

- Python 3.x installed on your system.
- Internet connectivity to make the API request.
- Required libraries installed (they will be automatically installed if missing).

## Usage

1. Open a terminal or command prompt.

2. Navigate to the directory containing the script.

3. Run the script with the following command:

```shell
python pnr_status_checker.py <pnr>
```

Replace `<pnr>` with the actual PNR number you want to check.

4. The script will retrieve the PNR status information and display it on the console.

**Note:**
- Ensure you have an active internet connection to fetch the PNR status information.


[![CodeQL](https://github.com/chunkboi/pnr-status/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/codeql-analysis.yml)
[![OSSAR](https://github.com/chunkboi/pnr-status/actions/workflows/ossar.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/ossar.yml)
[![Codacy Security Scan](https://github.com/chunkboi/pnr-status/actions/workflows/codacy.yml/badge.svg)](https://github.com/chunkboi/pnr-status/actions/workflows/codacy.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/chunkboi/pnr-status/badge)](https://www.codefactor.io/repository/github/chunkboi/pnr-status)
[![DeepSource](https://deepsource.io/gh/chunkboi/pnr-status.svg/?label=active+issues&show_trend=true&token=8c9BSEqF2nTvN-EmrdZDeAAR)](https://deepsource.io/gh/chunkboi/pnr-status/)

# DISCLAIMER

Author is not responsible for any losses incurrred to any individual, company or property either directly or indirectly as a result of using this script. Also, there is no warranty of any kind with this script.
