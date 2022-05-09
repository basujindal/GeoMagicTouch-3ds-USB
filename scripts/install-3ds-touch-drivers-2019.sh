#!/bin/bash -e

# Simple script to install 3DS touch drives

# Use at your own risk!

CUR_DIR=`pwd`

echo "--- Downloading package"
mkdir -p tmp
curl https://s3.amazonaws.com/dl.3dsystems.com/binaries/Sensable/Linux/TouchDriver2019_2_15_Linux.tar.xz --output tmp/TouchDriver2019_2_15_Linux.tar.xz

echo "--- Extracting package"
cd tmp && tar xf TouchDriver2019_2_15_Linux.tar.xz

echo "--- Installing"
sudo cp TouchDriver2019_2_14/bin/Touch* /usr/bin
sudo cp TouchDriver2019_2_14/usr/lib/libPhantomIOLib42.so /usr/lib

echo "--- Create and configure shared directory for configuration files"
sudo mkdir -p /usr/share/3DSystems/config
sudo chmod 777 /usr/share/3DSystems/config

echo "--- Create profile.d configurationfile"
echo "export GTDD_HOME=/usr/share/3DSystems" > 3ds-touch-drivers.sh
sudo cp 3ds-touch-drivers.sh /etc/profile.d/3ds-touch-drivers.sh

echo "--- Removing temporary files"
cd $CUR_DIR
rm -rf tmp/TouchDriver2019_2_15_Linux*

echo "--- Done"
