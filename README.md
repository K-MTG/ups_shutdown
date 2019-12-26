# ups_shutdown
Python script that powers down Raspberry Pi &amp; Hubitat when UPS battery drops below threshold. 

# Features
* Email Alert if UPS is on battery power
* If UPS battery drops below specified threshold an email alert will be sent out and the Hubitat Hub and Pi will shutdown gracefully. 

# Installation
1. [Install NUT (Network UPS Tool) on RPI](https://www.reddit.com/r/homelab/comments/5ssb5h/ups_server_on_raspberry_pi/ "NUT Install")
2. Install [nut2](https://github.com/rshipp/python-nut2/ "NUT2") on Pi (pip3 install nut2) 

# Usage
On the ups_monitor.py file
* set the "ip" variable to the IP of your Hubitat Hub
* set the "username" & "password" to your Hubitat accordingly 
* You can optionally provide gmail login credentials to send an email alert if an outage or shutdown occurs. Modify the "user" and "pwd" variable accordingly. If you do not want email alerts, comment out all calls to "send_email"
* RUN SCRIPT: python3 ups_monitor.py (add this to crontab -e on @reboot if you want the script to autostart on bootup).

The "UPS_SHUTDOWN_THRES" variable is the percent at which the Pi and Hubitat will shutdown. 
THE "UPS_SHUTDOWN_MIN_THRES" is the number of minutes remaining on the UPS when the Pi and Hubitat will shutdown 
Note: The shutdown will occur if either the UPS_SHUTDOWN_THRES or UPS_SHUTDOWN_MIN_THRES conditions are satisfied. 
The "CHECK_INTERVAL" is the number of seconds on how frequently the script checks the UPS status.

