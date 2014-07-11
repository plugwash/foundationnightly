#!/bin/bash -ev
VERSION=$1
wget http://nightly.raspberrypi.org/nightlyfirmware/pool/main/r/raspberrypi-firmware/raspberrypi-firmware_${VERSION}_armhf.changes
#gnupg doesn't like it if it's config dir doesn't exist
mkdir -p  ~/.gnupg
gpg --keyring /etc/apt/trusted.gpg --no-default-keyring --verify raspberrypi-firmware_${VERSION}_armhf.changes

for FILE in `dcmd -r --deb raspberrypi-firmware_${VERSION}_armhf.changes`; do
	wget http://nightly.raspberrypi.org/nightlyfirmware/pool/main/r/raspberrypi-firmware/$FILE
done
dscverify --keyring /etc/apt/trusted.gpg --no-default-keyrings raspberrypi-firmware_${VERSION}_armhf.changes
dcmd --deb dpkg -i raspberrypi-firmware_${VERSION}_armhf.changes

