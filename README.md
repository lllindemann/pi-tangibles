# pi-tangibles


## 1. Technical Specifications

The devices are designed as miniature computers that connect to web apps via web browser.
They feature:
- Touchscreens
- Position and magnetic sensors
- Gyroscope
- Acceleration Sensor
- Radio module

The hardware is based on a Raspberry Pi in a 3D-printed plastic case with integrated sensors.

### Further Ideas for Technical Specifications
- RFID/NFC Reader

### Communication Model / Structure

#### Compatible Radio Technologies (Receive)
- Bluetooth
- WiFi
    - MQTT


#### Compatible Radio Technologies (Emit)
- Bluetooth
- WiFi
    - MQTT

## 2. Initial Technical Setup

### 2.1 Prepare SD Card for Pi Zero
- Step 1: Flash Pi with [Raspberry PI Imager](https://www.raspberrypi.com/software/) on Pi SD-Card with the following settings:
    - Model: Raspberry Pi Zero
    - OS:  Raspberry Pi OS Lite --> listed in "Raspberry Pi OS (other)"
    - select your SD card
- Step2: Add additional settings:
    - continue BUT(!) add the following additional settings
    - General: set default user & password
    - General: add an wifi
    - Services: allow SSH
- Step 3: Flash the SD card with your settings

### 2.2 Setup Pi Zero 
- Step 1: Install OS on Pi Zero
    - Insert SD Card into Pi Zero
    - Boot Pi Zero
    - Pi Zero should connect to the added wifi network
- Step 3: Connect to pi SSH 
    - e.g. with Power Shell or Client like MobaXTerm
    - add a ssh session to: raspberrypi.local
    - connect with specified user and password

### 2.3 Add additional Wifi Network or add fallback wifi (optional) NEEDS TESTING!
**Step 1**: add another wifi network via nmcli
```console
sudo nmcli dev wifi connect "YOUR_SSID" password "YOUR_PASSWORD" ifname wlan0
```

**Step 2**: add a fallback wifi that is currently not available
```console
sudo nmcli connection add type wifi ifname wlan0 con-name backup ssid "Raspberry Wifi"
udo nmcli connection modify backup wifi-sec.key-mgmt wpa-psk wifi-sec.psk "r45p83rry"
sudo nmcli connection modify backup wifi.hidden yes
sudo nmcli connection modify backup connection.autoconnect-retries 0
sudo nmcli connection reload
```

**Step 3**: set highest prio to fallback wifi
```console
sudo nmcli connection modify BackupWLAN connection.autoconnect-priority 10
```

**Step 4**: check your setup wifi
```console
nmcli connection show
nmcli connection show backup
```

**Step 2**: show connections
```console
nmcli connection show
```
**Step 3**: inspect a specific connection
```console
sudo cat /etc/NetworkManager/system-connections/NETWORK_NAME.nmconnection
```

### 2.4 System Configuration 
**Step 1**: Update System Components & Packages:
```console
sudo apt-get update
sudo apt-get upgrade -y
```
**Step 2**: Install required software packages: Git, Pip3, Python-Venv
```console
sudo apt install -y git python3-pip python3-venv
```

### 2.5 Display Configuration 
**Step 1**: Clone Git Repo with Installer Scripts for TFT Display
```console
cd ~
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd ~/Raspberry-Pi-Installer-Scripts
```

**Step 2**: Install the Adafruit library to run the configuration script
```console
sudo pip3 install adafruit-python-shell --break-system-packages
sudo pip3 install click --break-system-packages
```

**Step 3**: Install PiTFT Driver
```console
sudo python3 adafruit-pitft.py
```
- select configuration: PiTFT 2.4" V2 resistive (240x320) (320x240)
- select rotation: 90 degrees
- select install type: setup PiTFT as desktop display (mirror)
- reboot when installation is finished

**Step 3**: Select mode (SPI or FBCP)
- FBCP (Framebuffer Copy)
    - Duplicates HDMI output
- SPI (Serial Peripheral Interface): Enables data transfer between the microcontroller or Raspberry Pi to peripherals such as displays 
    - enables script-based rendering on the TFT display

#### Configure the FBCP mode
- Configure PiTFT display mode using the install script
- 

```console
sudo python3 adafruit-pitft.py --display=24hat --rotation=90 --install-type=fbcp
sudo reboot
```



#### Configure the SPI mode
1. Disable FBCP if enabled
```console
sudo systemctl disable fbcp
sudo systemctl stop fbcp
```
2. Use Raspberry Config to enable SPI
```console
sudo raspi-config
```

- Interface Options → SPI → Enable

3. Reboot
```console
sudo reboot
```
