from requests import post
from json import loads
import sys
from uuid import uuid4
from pathlib import Path
import os
from pconst import const
import time
from sys import argv

file_path = Path(r"session.txt") # setting the path for the token and uuid

def setToken():
    ph_no = str(input("Ph No: "))

    if len(ph_no) < 10 or len(ph_no) > 10: # phone no input validation
        print("the phone no is incorrect")
        sys.exit()

    const.RANDOM_UUID = str(uuid4())
    otpDict = {
    'query': 'bruh',
    'source': 'IRCTC | Desktop User',
    'prevCode': None,
    'sessionId': None,
    'inputType': 'TEXT',
    'next_context': '64a3b2e6-0c9d-4aea-8cd9-0ddd09db2877,2',
    'cxpayload': {
    'mobileNumber':'bruh',
    },
    'userToken': 'bruh',
    }


    otpDict['query'] = ph_no
    otpDict['cxpayload']['mobileNumber'] = ph_no # setting phone no for request
    otpDict['userToken'] = const.RANDOM_UUID # setting the random uuid for otp request

    otp_req_res = post('https://assistant.corover.mobi/dishaAPI/bot/sendQuery/en', headers={'Accept': 'application/json, text/plain, */*'}, json=otpDict)

    otp_response = loads(otp_req_res.content.decode())

    if "Bad Request" in otp_response: # validating response
        print("Bad Request Error")
        sys.exit()
    else:
        otp_uuid = otp_response['renderTemplate']['data']['Details']
    tokenDict = {
    "query":"000000",
    "source":"IRCTC | Desktop User",
    "prevCode":None,
    "sessionId":None,
    "inputType":"TEXT",
    "next_context":"64a3b2e6-0c9d-4aea-8cd9-0ddd09db2877,3",
    "cxpayload":{"otp":"000000","otpuuid":"bruh"},
    "userToken":"bruh"
    }
    otp = str(input("enter otp: "))
    if len(otp) > 6 or len(otp) < 6:
        print("the otp is wrong")
        sys.exit()
    tokenDict['cxpayload']['otpuuid'] = otp_uuid
    tokenDict['userToken'] = const.RANDOM_UUID
    tokenDict['cxpayload']['otp'] = otp

    token_req_res = post('https://assistant.corover.mobi/dishaAPI/bot/sendQuery/en',headers={
        'Accept': 'application/json, text/plain, */*'}, json=tokenDict)

    
    token_json = loads(token_req_res.content.decode())

    print("setting token")
    time.sleep(0.5)
    
    if "cxtoken" not in token_json:
        print("the otp is wrong")
        sys.exit()

    token = token_json['cxtoken']

    with open(file_path, 'w') as file:
        file.write(token + '\n')
        file.write(const.RANDOM_UUID)
    print("Set Token Success")
    return token

def getPNRStatus(token, uuid,pnr):
    pnrDict={"query":"bruh",
    "source":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "prevCode":None,
    "sessionId":None,
    "inputType":"TEXT",
    "next_context":"1918abb8-6b17-426e-a79e-990c3b194c9a,2",
    "cxpayload":{"pnr":"bruh","enquiryType":"ALL"},
    "userToken":"bruh",
    "suggestion":False,
    "isFallback":False,
    "isRefund":False
    }
    pnrDict['query'] = str(pnr)
    pnrDict['cxpayload']['pnr'] = str(pnr)
    pnrDict['userToken'] = uuid

    headerDict = {'Accept': 'application/json, text/plain, */*', 'cxtoken':'bruh'}
    headerDict['cxtoken'] = str(token) # setting token for Request
    pnr_req_res = post('https://assistant.corover.mobi/dishaAPI/bot/sendQuery/en', headers=headerDict,json=pnrDict)
    return pnr_req_res.content.decode()


def pnr_input():
    if not os.path.exists(file_path):
        print("It seems like you dont have a token")
        setToken()
    elif os.path.exists(file_path):
        pnr = str(input("Enter PNR Number: "))
    if len(pnr) > 10 or len(pnr) < 10:
        print("the pnr is wrong")
        sys.exit()
    else:
        return pnr


def getToken():
    with open(file_path) as f:
        content_list = [line.rstrip() for line in f]
    
    token = content_list[0]
    return token

def getUUID():
    with open(file_path) as f:
        content_list = [line.rstrip() for line in f]
    uuid = content_list[1]
    return uuid


def print_pnr(token,uuid,pnr):

    pnrDict = loads(getPNRStatus(token,uuid,pnr))

    
     # moving in the JSON tree for easier access

    #print('currentBerthCode' in passenger_multiple)
    
    if str(pnrDict['renderTemplate']['data']['departureTime']) == '0': # check if pnr is generated or not
        print("PNR NOT YET GENERATED OR FLUSHED")
        sys.exit()
    else:
        data = pnrDict['renderTemplate']['data']
        passenger = pnrDict['renderTemplate']['data']['passengerList']
        #os.system('cls' if os.name == 'nt' else 'clear')

        print("Train Details: " + data['trainNumber'] + ' - ' + data['trainName'] + ' || ' + "Journey Date: "+data['dateOfJourney'] + ' || ' + "Chart Status: " + data['chartStatus'])
        
        if int(data['numberOfpassenger']) == 1: # checking number of passenger
            if int(data['passengerList']['currentBerthNo']) == 0: # for WL and RAC tickets the currentBerthNo value will be the current status of the ticket so here we check if the ticket is WL/RAC or not if the value is 0 then the ticket was confirmed from the beginning
                #print Coach and Seat No
                if 'bookingBerthCode' in passenger:
                    print("Passenger " +  data['passengerList']['passengerSerialNumber'] + ': ' + data['passengerList']['bookingStatus'] + '/'  + data['passengerList']['bookingCoachId'] +'/' + data['passengerList']['bookingBerthNo'] + "/" + data['passengerList']['bookingBerthCode'] +' ' + "Age: " + data['passengerList']['passengerAge'])
                else:
                    print("Passenger " +  data['passengerList']['passengerSerialNumber'] + ': ' + data['passengerList']['bookingStatus'] + '/'  + data['passengerList']['bookingCoachId'] +'/' + data['passengerList']['bookingBerthNo'] +' ' + "Age: " + data['passengerList']['passengerAge'])

            else:
                #print the WL/RAC position
                if 'currentBerthCode' in passenger:
                    print("Passenger " +  data['passengerList']['passengerSerialNumber'] + ': ' + data['passengerList']['currentStatus'] + '/'  + data['passengerList']['currentCoachId'] + '/' + data['passengerList']['currentBerthNo'] +'/'+data['passengerList']['currentBerthCode'] +" " + "Age: " + data['passengerList']['passengerAge'])
                else:
                    print("Passenger " +  data['passengerList']['passengerSerialNumber'] + ': ' + data['passengerList']['currentStatus'] + '/'  + data['passengerList']['currentCoachId'] + '/' + data['passengerList']['currentBerthNo'] + " " + "Age: " + data['passengerList']['passengerAge'])
                
        else:
            passenger_multiple = data['passengerList'][0]
            if data['passengerList'][0]['currentBerthNo'] == '0': #the currentBerthNo is in the passengerList so we need the list index to check for WL/RAC
                for i in range(int(data['numberOfpassenger'])):#looping through the number of passengers to print all the passenger data for multiple passengers
                    if 'bookingBerthCode' in passenger_multiple:
                        print("Passenger " +  data['passengerList'][i]['passengerSerialNumber'] + ': ' + data['passengerList'][i]['bookingStatus'] + '/'  + data['passengerList'][i]['bookingCoachId'] +'/' + data['passengerList'][i]['bookingBerthNo'] +'/' + data['passengerList'][i]['bookingBerthCode'] +" " + "Age: " + data['passengerList'][i]['passengerAge'])                
                    else:
                        print("Passenger " +  data['passengerList'][i]['passengerSerialNumber'] + ': ' + data['passengerList'][i]['bookingStatus'] + '/'  + data['passengerList'][i]['bookingCoachId'] +'/' + data['passengerList'][i]['bookingBerthNo'] +" " + "Age: " + data['passengerList'][i]['passengerAge'])


            else:
                for i in range(int(data['numberOfpassenger'])):  #looping for printing WL/RAC position
                    if 'currentBerthCode' in passenger_multiple:
                        print("Passenger " +  data['passengerList'][i]['passengerSerialNumber'] + ': ' + data['passengerList'][i]['currentStatus'] +'/' + data['passengerList'][i]['currentCoachId'] + '/' + data['passengerList'][i]['currentBerthNo'] + '/'+ data['passengerList'][i]['currentBerthCode']+ " " + "Age: " + data['passengerList'][i]['passengerAge'])
                    else:
                        print("Passenger " +  data['passengerList'][i]['passengerSerialNumber'] + ': ' + data['passengerList'][i]['currentStatus'] +'/' + data['passengerList'][i]['currentCoachId'] + '/' + data['passengerList'][i]['currentBerthNo'] + " " + "Age: " + data['passengerList'][i]['passengerAge'])
                        
                                
        print("Reservation From " + data['boardingPoint'] + " -> " + data['destinationStation'] )
        print("Quota: " + data['quota'])
        print("Journey Class: " + data['journeyClass'])
        print("Fare: " + "Rs." + data['ticketFare'])
        
        
token = getToken()
uuid = getUUID()

if len(argv) == 1:
    pnr = pnr_input()
    begin = time.time()
    print_pnr(token,uuid,pnr)
    end = time.time()
    print(f"total runtime was {end - begin} seconds")
else:
    if len(argv) > 2:
        print("Too Many Arguments" + '\n' + f"Correct Usage python {os.path.basename(__file__)} " + "<10 digit PNR>" + " or --reset")
        sys.exit()
    elif argv[1] == "--reset":
        choice = str(input("Do you really want to Reset your session Y for yes and N for no: "))
        if choice == 'Y':
            os.remove(file_path)
            print("Cleared Session")
            sys.exit()
        elif choice == 'N':
            print("Didn't Clear Session")
            sys.exit()
    elif len(argv[1]) != 10:
        print("The PNR is Not 10 digits long" + '\n' + f"Correct Usage python {os.path.basename(__file__)} " + "<10 digit PNR>" + " or --reset" )
        sys.exit()
    elif len(argv[1]) == 10:
        begin = time.time()
        print_pnr(token,uuid,argv[1])
        end = time.time()
        print(f"total runtime was {end - begin} seconds")
    

        
