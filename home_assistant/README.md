# Home Assistant

I'm trying to make [home assistant](https://www.home-assistant.io/) to work on
my pi. I'm putting here some things I've picked up and usedful links for future
me and others as well.

## Insights

- Home assistant isn't the same as [Hass.io](https://www.home-assistant.io/blog/2017/07/25/introducing-hassio/).
Whereas home assistant is a python server, Hass.io is a full-system image you
can flash on an SD card and put on your pi. Personally, I wanted to keep my
pi running Raspbian, so I preferred to run home assistant directly. Hass.io does
make running home assistant easier with add-ons which make integrations easier
(with Google Assistant and Let's Encrypt, for example).

## What am I trying to accomplish?

- A home assistant server which I can operate using Google Assistant on my
phone.

## Useful links

- To get started with home assistant, you can download it using pip: `pip3 install homeassistant`.
You can also follow [this guide](https://www.home-assistant.io/docs/installation/raspberry-pi/)
for more details.

- [Setup systemd unit to run the service](https://www.home-assistant.io/docs/autostart/systemd/).

- Setup port forwarding in your router to make the server accessible from
outside your local network (This depends on your router).

- Setup a dynamic DNS entry using [DuckDNS](https://www.duckdns.org/). You can
use their suggestion on the site to periodically update the IP address, or you
can have the home assistant server update this using the [DuckDNS component](https://www.home-assistant.io/components/duckdns/).

- Follow [this tutorial](https://www.splitbrain.org/blog/2017-08/10-homeassistant_duckdns_letsencrypt)
to set up an SSL cert using Let's Encrypt.

- Setup Google Assistant using [this tutorial](https://www.home-assistant.io/components/google_assistant/).

- Setting up virtual hosts using nginx. I created an [nginx config](thelerners.conf)
which allows me to use virtual hosts. So far, I've created only one virtual host
for vlc, working with a wildcard certificate. Maybe I'll do more in the future.
I've created the wildcard certificate using [dehydrated](https://github.com/lukas2511/dehydrated)
as well (as described in a [previous link](https://www.splitbrain.org/blog/2017-08/10-homeassistant_duckdns_letsencrypt)),
it was just a matter to define an alias for the star domain.

## Alternative

There's a paid alternative to all of this named [Home Assistant Cloud](https://www.home-assistant.io/cloud/)
which gives easier integration. I didn't try making it work though.
