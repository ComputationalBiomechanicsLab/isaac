#!/usr/bin/env bash

echo "sorry, parts of this are manual, for now"
echo "sourced from: https://docs.anaconda.com/free/anaconda/install/linux/"

# it lists these dependencies
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

# i then manually downloaded conda and ran the installer as `root`, but specified
# that anaconda should be installed to `/opt/anaconda3`, instead of its default
# location
