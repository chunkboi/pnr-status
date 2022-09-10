from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode
from requests import post
from json import loads
import time
import sys

def clear():
    #clear screen by printing tons of newlines
    print('\n'* 1000)
clear()

# encrypt pnr with key and iv stole it from https://stackoverflow.com/questions/50062663/encryption-decryption-using-aes-cbc-pkcs7padding
def getEncryptedPNR(pnr):
    data = bytes(pnr, 'utf-8')
    backend = default_backend()
    padder = padding.PKCS7(128).padder()
    
    data = padder.update(data) + padder.finalize()
    key = b'8080808080808080'
    iv = b'8080808080808080'
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    enc_pnr = b64encode(ct)
    return enc_pnr.decode('utf-8')

 # format response json and print it
def printData(json_data):
    boardingStation = json_data["BrdPointName"]
    destinationStation = json_data["DestStnName"]
    quota = json_data["quota"]
    className = json_data["className"]
    trainNumber = json_data["trainNumber"]
    trainName = json_data["trainName"]
    dateOfJourney = json_data["dateOfJourney"]    
    
    print("PNR STATUS")
    print("------------------------------------------------------------------")
    print(boardingStation + " -> " + destinationStation) # source and destination station
    print(trainNumber + ' - ' + trainName) # train number and name
    print()
    print("Quota: " + quota)
    print("Journey Class: " + className)
    print("Date Of Journey: " + dateOfJourney)
    print()
    for p in json_data["passengerList"]:
        print("Passenger " + p["passengerSerialNumber"] + ": " + p["currentStatus"] + '/' + p["currentCoachId"] + '/' + p["currentBerthNo"])



pnr = input("Enter PNR Number: ") #  recieve PNR number
start = time.time()

#input validation pnr should be 10 digits
if len(pnr) != 10:
    print("PNR LENGTH should be 10 DIGITS")
    sys.exit(0)
   
    
json_data = {
    'pnrNumber': getEncryptedPNR(pnr),
}


# do a post request to the url with encrypted pnr
response = post('https://railways.easemytrip.com/Train/PnrchkStatus', json=json_data)
json_data = loads(response.content) # parse response content into json


clear()
end = time.time()
printData(json_data)
print(f"Total time taken: {round(end - start, 3)} seconds") # print total time taken to complete the program

