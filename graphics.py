from subprocess import run

try:
    from requests import post 
    from json import loads
    from os import name
    from time import perf_counter
    import http.client as httplib
    import tkinter as tk
    
except ModuleNotFoundError:
    print("Core modules not found trying to install them")
    run(["pip", "install", "requests", "tkinter"],check=True, text=True)
    
except:
    print("Some Error Occurred, could not import libraries")
    exit(0)
    

def connect():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

def request(pnr):
    headers = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',   
    }
    
    json = {
    'pnrID': pnr,
    'trackingParams': {
        'affiliateCode': 'MMT001',
        'channelCode': 'WEB',
    },
    }
    
    request = post('https://mapi.makemytrip.com/api/rails/pnr/currentstatus/v1',headers=headers, json=json)
    return request.content
    


root= tk.Tk()
root.title("pnr status app")

canvas1 = tk.Canvas(root, width = 400, height = 200,  relief = 'raised')
canvas1.pack()
canvas2 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
canvas2.pack()

label1 = tk.Label(root, text='PNR STATUS APP')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Enter PNR Number:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)
def clear():
    canvas2.delete('all')
def getPNR ():
    
    pnr = entry1.get()
    clear()
    
    json_data = loads(request(pnr))
    
    if len(pnr) != 10: # pnr validation
        label3 = tk.Label(root, text= "PNR SHOULD BE 10 DIGITS",font=('helvetica', 12, 'bold'))
        canvas2.create_window(200, 210, window=label3)
        return
    if len(json_data["TrainDetails"]["Train"]) == 0:
        label3 = tk.Label(root, text= "PNR NOT GENERATED OR FLUSHED",font=('helvetica', 12, 'bold'))
        canvas2.create_window(200, 210, window=label3)
        return
        
        

    
    
    train_number = json_data["TrainDetails"]["Train"]["Number"]
    train_name = json_data["TrainDetails"]["Train"]["Name"]
    chart_status = json_data["TrainDetails"]["ChartPrepared"]
    start_station = json_data["StationDetails"]["BoardingPoint"]["name"]
    destination_station = json_data["StationDetails"]["ReservationUpto"]["name"]
    date_of_journey = json_data["PnrDetails"]["SourceDoj"]["FormattedDate"]
    class_name = json_data["PnrDetails"]["Class"]
    quota = json_data["PnrDetails"]["Quota"]
    
    label3 = tk.Label(root, text= start_station + " -> " + destination_station,font=('helvetica', 10))
    canvas2.create_window(200, 50, window=label3)
    
    label4 = tk.Label(root, text= train_number + " - " + train_name ,font=('helvetica', 10,))
    canvas2.create_window(110, 70, window=label4)
    
    label3 = tk.Label(root, text= "Chart Prepared?: " + str(chart_status),font=('helvetica', 10))
    canvas2.create_window(100, 90, window=label3)
    
    label4 = tk.Label(root, text= "Quota: " + quota ,font=('helvetica', 10,))
    canvas2.create_window(50, 110, window=label4)
    
    label3 = tk.Label(root, text= "Class: " + class_name,font=('helvetica', 10))
    canvas2.create_window(50, 130, window=label3)
    
    label4 = tk.Label(root, text= "Date Of Journey: " + date_of_journey,font=('helvetica', 10,))
    canvas2.create_window(100, 150, window=label4)
    
    a = 170
    
    for p in json_data["PassengerDetails"]["PassengerStatus"]:
        label4 = tk.Label(root, text= "Passenger " + str(p["Number"]) + ": " + p["CurrentStatus"],font=('helvetica', 10,))
        canvas2.create_window(100, a, window=label4)
        a = a + 20



    
   
  

    
button1 = tk.Button(text='Get the PNR STATUS', command=getPNR, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()