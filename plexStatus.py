"""
This script keeps track of Plex's status (Play/Pause/Stop) to be used in additional automation through EventGhost
"""
import requests
import xml.etree.ElementTree as ET
import time
import psutil
import os
import pickle  # to grab home status from connectedDevices
import shared

ip = '127.0.0.1'
port = '32400'

last_state = None
last_media_type = None

# Get Plex's current status (Play/Pause/Stop)
def get_status(home):
    media_type = 'Nobody'
    state = 'Home'
    try:
        data = requests.get('http://' + ip + ':' + port + '/status/sessions', verify=False).text
        response = ET.fromstring(data)
        if home:
            if '<MediaContainer size="0">' in data:
                media_type = 'None'
                state = 'STOPPED'
                print('Nothing Streaming')
            else:
                try:
                    for i in response.iter('Video'):
                        media_type = i.get('type').capitalize()
                        print('Type: ' + str(media_type))
                    for i in response.iter('Player'):
                        state = i.get('state').upper()
                        print('State: ' + str(state))
                except IndexError:
                    time.sleep(30)
                    print('IndexError. Plex unreachable?')
    except requests.exceptions.RequestException:
        print('Plex unreachable')
    print('Home: ', ','.join(home))
    return media_type, state

p = psutil.Process(os.getpid())  # Get PID for this script
p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)  # Set script to low priority in Windows
time.sleep(180)


# Constatnly check Plex's status, create notifications if I'm home.
while True:
    try:
        with open('shared.pkl', 'rb') as f:
            home = pickle.load(f)
    except EOFError:
        home = []
    media_type, state = get_status(home)
    if last_media_type != media_type or last_state != state:
            # notify EventGhost
            shared.eventghost_notify('Plex', media_type, state)
            # notify phone via AutoRemote
            if 'Michael' in home:
                shared.autoremote_notify('Plex ' + state + ' ' + media_type + '=:=', 'Michael Home Autoremote')
    # Adjust frequency of checks based off of status and whether or not somebody is home
    if state == 'PLAYING' or state == 'BUFFERING':
        interval = 1
    elif state == 'PAUSED':
        interval = 10
    elif state == 'STOPPED':
        interval = 15
    else:
        interval = 60 * 3  # if nobody home, only check once every 3 minutes
    print('Interval: ' + str(interval))
    print('-----------------------------')
    time.sleep(interval)

    last_state, last_media_type = state, media_type
