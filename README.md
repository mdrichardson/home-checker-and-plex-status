# Who's Home

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