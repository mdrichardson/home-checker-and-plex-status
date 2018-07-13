"""
This script logs into your Tomato-flashed router, looks up devices with an active DHCP reservation,
and notifies EventGhost (PC automation software) and AutoRemote (android automation app). For the devices
listed in mac_list, the script then notifies EventGhost and AutoRemote which devices are home. If none
are home, it notifies that they're All Away.

Once this is executed, no user input is necessary.

For your own use, replace the following variables with your own information:
    ip
    user
    password
    mac_list

Be sure to also edit the necessary variables in the "shared" module as well.
"""

import requests
import time
import datetime
import psutil
import os
import pickle
import private  # personal/private settings
import shared

# Router Info
ip = '192.168.1.1'
user = private.router_user
password = private.router_pass

# Device Info
mac_list = {
    'Michael': private.michael_mac,
    'Dani': private.dani_mac#,
    #'chromecast': private.chromecast_mac,
    #'chromecastUpstairs': private.chromecastUpstairs_mac
}

# Defaults, no need to change
home = []
last_home = ['Null']


def check_connected():
    # Attempt to log into router and return who is home
    try:
        data = requests.get('http://' + ip + '/status-devices.asp', auth=(user, password), verify=False).text
        start = data.find('dhcpd_lease = [ [')
        end = data.find('list = [];')
        connected = data[start:end]
        print(connected)
    except requests.exceptions.RequestException:
        print('Router Unreachable')
        connected = []
    return connected, home

# Get PID for this script
p = psutil.Process(os.getpid())
# Set script to low priority in Windows
p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
# Delay doing anything for the first 3 minutes after the script is executed
time.sleep(180)

# Run forever
while True:
    now = datetime.datetime.now()
    # Find out who's connected
    connected, home = check_connected()
    # Notify as appropriate
    for name, mac in mac_list.items():
        if mac in connected and name not in last_home:
            print(name, 'is home.')
            shared.eventghost_notify(name + ':Home')
            home.append(name)
            interval = 60 * 15  # check less frequently if home
        elif mac not in connected and name in last_home:
            print(name, 'is away.')
            shared.eventghost_notify(name + ':Away')
            if name in home:
                home.remove(name)
    if not home:
        print('All Away')
        shared.eventghost_notify('All:Away')
    # check more frequently if away, but home soon
    if not home and now.weekday() < 5 and datetime.time(16) <= now.time() <= datetime.time(19):
        interval = 15
    elif not home:
        interval = 60 * 2
    # Save who's home using pickle module for use in other scripts
    with open('shared.pkl', 'wb') as f:
        pickle.dump(home, f)
    # For debugging
    print('Home: ', ','.join(home))
    print('Interval: ', interval)
    print('---------------------')
    last_home = home
    # Wait for appropriate time before running again
    time.sleep(interval)
