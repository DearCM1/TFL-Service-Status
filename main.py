# =============================================================
# packages
# =============================================================

import time
import requests
import json 
import datetime

# =============================================================
# functions
# =============================================================

def get_now():
    # just gets the date and time and outputs two separate
    # strings in the format of "yyyy_mm_dd" and "HH:MM:SS"

    now = datetime.datetime.now()
    
    date = [
        str(now.date().year),
        str(now.date().month),
        str(now.date().day)
    ]

    if len(date[1]) == 1:

        date[1] = "0" + date[1]

    else:

        date[1] = date[1]

    if len(date[2]) == 1:

        date[2] = "0" + date[2]
    
    else:

        date[2] = date[2]

    date = date[0] + "_" + date[1] + "_" + date[2]

    time = [
        str(now.time().hour),
        str(now.time().minute),
        str(now.time().second)
    ]

    if len(time[0]) == 1:

        time[0] = "0" + time[0]
    
    else:

        time[0] = time[0]

    if len(time[1]) == 1:

        time[1] = "0" + time[1]
    
    else:

        time[1] = time[1]

    if len(time[2]) == 1:

        time[2] = "0" + time[2]
    
    else:

        time[2] = time[2]

    time = time[0] + ":" + time[1] + ":" + time[2]

    del now

    return date, time

def check_reason(response):
    # checks if the lineStatuses:reasons entry exists and
    # handles error if there is an issue.

    try:

        reason = response['lineStatuses'][0]['reason']

    except KeyError:

        reason = "none"
    
    finally:

        return reason

def initialise(root):
    
    r1, _ = get_tube()
    r2, _ = get_elizabeth()
    r3, _ = get_dlr()

    response = [r1, r2, r3]
    last = []

    for i in range(len(response)):

        for j in range(len(response[i])):

            id = response[i][j]['id']
            
            try:
        
                f = open(root+id+".txt","r")

            except FileNotFoundError:

                new_file(root, id)
                last.append(0)

            finally:

                f = open(root+id+".txt","r")
                lines = f.readlines()
                last.append(str(int(lines[-1].partition(",")[0]) + 1))
                f.close()

    return last


def new_file(root, id):

    f = open(root+id+".txt","x")
    f.write(
        "0,date,time,name,status,severity,reason"
    )
    f.close()

def reset_file(id):

    f = open(id+".txt","w")
    f.write(
        "0,date,time,name,status,severity,reason"
    )
    f.close()

def get_tube():

    res = requests.get('https://api.tfl.gov.uk/line/mode/tube/status')
    response = json.loads(res.text)
    now = get_now()

    return response, now

def get_elizabeth():

    res = requests.get('https://api.tfl.gov.uk/line/mode/elizabeth-line/status')
    response = json.loads(res.text)
    now = get_now()

    return response, now

def get_dlr():

    res = requests.get('https://api.tfl.gov.uk/line/mode/dlr/status')
    response = json.loads(res.text)
    now = get_now()

    return response, now

def handle_tube(last):

    response, now = get_tube()
    
    for i in range(len(response)):

        name = response[i]['id']
        status = str(response[i]['lineStatuses'][0]['statusSeverityDescription'])
        severity = str(response[i]['lineStatuses'][0]['statusSeverity'])
        reason = check_reason(response[i])
    
        f = open(root+response[i]['id']+".txt","a")
        f.write("\n"+last[i]+","+now[0]+","+now[1]+","+name+","+status+","+severity+","+reason)
        f.close()

        del f, name, status, severity, reason
    
    del response, now

def handle_elizabeth(last):

    response, now = get_elizabeth()

    name = response[0]['id']
    status = str(response[0]['lineStatuses'][0]['statusSeverityDescription'])
    severity = str(response[0]['lineStatuses'][0]['statusSeverity'])
    reason = check_reason(response[0])

    f = open(root+response[0]['id']+".txt","a")
    f.write("\n"+last+","+now[0]+","+now[1]+","+name+","+status+","+severity+","+reason)
    f.close()

    del f, name, status, severity, reason, response, now

def handle_dlr(last):

    response, now = get_dlr()

    name = response[0]['id']
    status = str(response[0]['lineStatuses'][0]['statusSeverityDescription'])
    severity = str(response[0]['lineStatuses'][0]['statusSeverity'])
    reason = check_reason(response[0])

    f = open(root+response[0]['id']+".txt","a")
    f.write("\n"+last+","+now[0]+","+now[1]+","+name+","+status+","+severity+","+reason)
    f.close()

    del f, name, status, severity, reason, response, now

root = "/Users/Calum/Documents/Docs/Education/projects/tfl_service/data/"

k = 0

while True:

    k += 1
    last = initialise(root)

    handle_tube(last)
    handle_elizabeth(last[-2])
    handle_dlr(last[-1])

    time.sleep(60)

    if k > 59:

        break
    
    else:

        continue