#!/bin/bash

set -e

echo "#EXTM3U"
echo "##"
echo "## This was was generated from the following (better) list: http://tiny.cc/b2k_music_global"
sets=$(curl -s -L http://tiny.cc/b2k_music_global | grep -B 1 99sets.livecdn.biz/99sets)
echo "$sets"

