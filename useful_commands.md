
# Audio output

## Set output audio to analog:

`amixer cset numid=3 1`

# VLC

## Set web as an extra interface

`vlc --extraintf=http`

## Set the password

(Probably preferable to set using the UI, to avoid having the password in
the bash history)

`vlc --http-password=MYPASS`

# Pi Setup

## Set a static IP

### What should you do

Configure the static IP using your router. For me, it was done by going to
my router's IP address (192.168.1.1) and setting the static IP using the web UI.

### What not to do
I mostly followed [this guide](https://www.modmypi.com/blog/how-to-give-your-raspberry-pi-a-static-ip-address-update).
Here's what I had setup (as I'm using only wireless and my router's IP address
is 192.168.1.1):

```
interface wlan0
static ip_address=192.168.1.80/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

In order to activate this, I turned the interface off and on (while being
connected to the pi directly):

```
sudo ifconfig wlan0 down
sudo ifconfig wlan0 up
```

After a few seconds, `ifconfig` was able to to show the static IP I set.

### Why should you set the static IP that way?

To avoid weird stuff. Details [here](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=218167), but the
gist is that I had the Pi not respond to network requests (ping, ssh) after a
while. Spare yourself the unnecessary troubleshooting and use the router to
specify the static IP.

Thinking about this even more - setting static IPs on the device is more
collision-prone. If the configuration is in a central place - it's more easy to
maintain.


## Disable power management on wifi

See [this thread](https://www.raspberrypi.org/forums/viewtopic.php?t=197975)
for more information, but I got the Pi get unresponsive to  network requests
after some time, and it seems like disabling the wifi's power management is
supposed to help:

```
iwconfig wlan0 power off
```

Also, added this to `/etc/rc.local` to make sure that the pi runs this
command on boot.
