from requests import post
from subprocess import call
from json import loads
from os import name
from time import time

def clear():
    #clear screen
    call(["clear"] if name == 'posix' else ["cls"], shell=True)
  

def printData(json_data):
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
    print(start_station + " -> " + destination_station)
    print(train_number + " - " + train_name)
    print()
    print("Chart Prepared?: " + str(chart_status))
    print("Quota: " + quota)
    print("Class: " + class_name)
    print("Date Of Journey: " + date_of_journey)
    print()
    for p in json_data["PassengerDetails"]["PassengerStatus"]:
        print("Passenger " + str(p["Number"]) + ": " + p["CurrentStatus"])
    
    
    

headers = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',   
}

pnr = input("Enter PNR number: ")
start = time()
if len(pnr) != 10: # pnr validation
    print("PNR LENGTH should be 10 DIGITS")
    sys.exit(0)
   
    
json = {
    'pnrID': pnr,
    'trackingParams': {
        'affiliateCode': 'MMT001',
        'channelCode': 'WEB',
    },
}

response = post('https://mapi.makemytrip.com/api/rails/pnr/currentstatus/v1',headers=headers, json=json)

json_data = loads(response.content)
end = time()
clear()
printData(json_data)
print(f"Total time taken: {round(end - start, 3)} seconds") # print total time taken to complete the program
