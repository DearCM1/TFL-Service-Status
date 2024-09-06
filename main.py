import time
import requests
import json 
import datetime

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

def new_file(id):

    f = open(id+".txt","x")
    f.write(
        "0,date,time,name,status,severity,reason"
    )
    f.close()

def get_tube():

    res = requests.get('https://api.tfl.gov.uk/line/mode/tube/status')
    response = json.loads(res.text)
    now = get_now()

    return response, now

def handle_tube(new=0):

    root = "/Users/Calum/Documents/Docs/Education/tfl_service/"
    response, time = get_tube()
    
    for i in range(len(response)):

        if new == 1:

            new_file(response[i]['id'])

        else:

            new = 0

        name = response[i]['id']
        status = str(response[i]['lineStatuses'][0]['statusSeverityDescription'])
        severity = str(response[i]['lineStatuses'][0]['statusSeverity'])
        reason = check_reason(response[i])

        f = open(root+response[i]['id']+".txt","r")
        lines = f.readlines()
        last  = str(int(lines[-1].partition(",")[0]) + 1)
        f.close()

        f = open(root+response[i]['id']+".txt","a")
        f.write("\n"+last+","+time[0]+","+time[1]+","+name+","+status+","+severity+","+reason)
        f.close()

        del f, lines, last, name, status, severity, reason
    
    del new, root, response, time
    


def get_elizabeth():

    res = requests.get('https://api.tfl.gov.uk/line/mode/elizabeth-line/status')
    response = json.loads(res.text)

    return response

def get_dlr():

    res = requests.get('https://api.tfl.gov.uk/line/mode/elizabeth-line/status')
    response = json.loads(res.text)

    return response