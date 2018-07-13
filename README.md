# Who's Home + Plex Status

I used these combined scripts to find out who's home, create notifications for these events in AutoRemote (Android App)
and EventGhost (Windows automation). Based off of these events, it would turn on Voice Recognition on my phone so that 
I could control Plex with my voice when I'm home and when Plex is playing a video. 

I also had a webcam that I used as a security camera with Netcam Studio. When somebody was home, the script would send an event to EventGhost to turn the camera off and stop recording. When nobody was home, it would turn the camera on and start recording.

These scripts only hand the "who's home" and "what is Plex's current status" portion of that.

*Note: This was a small project I completed in 2016*

## connectedDevices.py

This script logs into your Tomato-flashed router, looks up devices with an active DHCP reservation,
and notifies EventGhost (PC automation software) and AutoRemote (android automation app). For the devices
listed in mac_list, the script then notifies EventGhost and AutoRemote which devices are home. If none
are home, it notifies that they're All Away.

Once this is executed, no user input is necessary.

For your own use, replace the following variables with your own information:

* `ip`
* `user`
* `password`
* `mac_list`

Be sure to also edit the necessary variables in the "shared" module as well.

## plexStatus.py

This script keeps track of Plex's status (Play/Pause/Stop) to be used in additional automation through EventGhost

