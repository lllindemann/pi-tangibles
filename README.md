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

### SSH Connection 
- Step 1: Flash Pi with [Raspberry PI Imager](https://www.raspberrypi.com/software/) on Pi SD-Card with the following settings:
    - OS with GUI
    - set default user & password 
    - allow SSH
- Step 2: Configure WiFi
    - SD into Pi
    - Boot Pi
    - add WiFi
- Step 3: Connect to pi SSH 
    - e.g. with Power Shell or Client like MobaXTerm 

### System Configuration 
Update System Components & Packages:
```console
apt get update
apt get upgrade -y
```
### Display Configuration 
**Step 1**: Clone Git Repo with Installer Scripts for TFT Display
```console
cd ~
git clone [https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git](https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git)
cd ~/Raspberry-Pi-Installer-Scripts
```

**Step 2**: Install the Adafruit library to run the configuration script
```console
cd ~
sudo pip3 install adafruit-python-shell --break-system-packages
```

**Step 3**: Select mode (SPI or FBCP)
- FBCP (Framebuffer Copy)
    - Duplicates HDMI output
- SPI (Serial Peripheral Interface): Enables data transfer between the microcontroller or Raspberry Pi to peripherals such as displays 
    - enables script-based rendering on the TFT display

#### Configure the FBCP mode
- Configure PiTFT display mode using the install script 

```console
sudo python3 adafruit-pitft.py --display=24hat --rotation=90 --install-type=fbcpsudo Reboot
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