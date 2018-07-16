
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
