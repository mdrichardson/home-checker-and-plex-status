"""
This is a shared script that I've used for a couple of different hobby projects. 
I use it to create notifications and restart EventGhost as needed (it freezes farily frequently)
"""
import subprocess
import os
import time
import requests
import private
from debug import alert

eventghost_location = 'H:\Program Files (x86)\EventGhost\EventGhost.exe'

autoremote_url = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?text='


def eventghost_notify(message, *payload, debug_alert=''):
    print('Notifying EventGhost with ', message, ' ', payload)
    # Check to see that EventGhost is running, open it if not
    tmp = os.popen("tasklist").read()
    if "EventGhost.exe" not in tmp and "eventghost.exe" not in tmp:
        print('EventGhost not running. Starting...')
        subprocess.run([eventghost_location], shell=True)
        time.sleep(30)
    # Create EventGhost notification
    try:
        subprocess.run([eventghost_location, '-e', message + ' ', *payload], shell=True, timeout=90)
    # Restart EventGhost if it's frozen
    except subprocess.TimeoutExpired:
        if eventghost_restart() == 'OK':
            eventghost_notify(message, *payload, debug_alert)
        if debug_alert != '':
            alert('EG ' + debug_alert)
        eventghost_notify(message, *payload, debug_alert)
    return


def eventghost_restart():
    print('EG Notification Failed, Killing EventGhost...')
    os.system("taskkill /im eventghost.exe /f")
    time.sleep(10)
    os.system("taskkill /im eventghost.exe /f")
    time.sleep(30)
    print('Restarting EventGhost...')
    subprocess.run([eventghost_location], shell=True)
    time.sleep(30)
    return 'OK'

# AutoRemote from Joaoapps is used for multi-device notifications
def autoremote_notify(message, device, debug_alert=''):
    import private
    print('Notifying AutoRemote with ', message)
    try:
        requests.get(autoremote_url + message + '&deviceId=' + private.autoremote_device[device] + '&apikey=' + private.autoremote_key)
    except:
        print('AutoRemote Connection Failed')
        if debug_alert != '':
            alert('AR ' + debug_alert)
    return
