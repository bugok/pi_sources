# `crawler.py`

## Motivation

As part of my playing around with the Pi, I wanted to have a playlist based on
the playlists that [eco99fm](http://eco99fm.maariv.co.il/) has. Therefore, as an
exercise I built a crawler which makes an m3u file of the various playlists.

## Prerequisites

There are a few needed packages:

- [`basicstruct`](https://pypi.org/project/basicstruct/)
- [`click`](https://pypi.org/project/click/)
- [`fake-useragent`](https://pypi.org/project/fake-useragent/)
- [`requests`](https://pypi.org/project/requests/)
- [`selenium`](https://pypi.org/project/selenium/), as well as
[`ChromeDriver`](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## How to run

```lang=bash
$ ./crawler.py eco99_playlists.m3u
```

## What happens under the hood

1. Using Chrome, webdriver crawls the eco99fm site, identifying the different playlists.
1. Each playlist is crawled, identifying the link to the corresponding m3u file.
1. An m3u file in constructed, made out of the m3u files identified.
1. The m3u file is written to the given path.
