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
sudo apt install -y git python3-pip python3-venv python3-dev python3-pil python3-numpy
```

## 3. Display Configuration 
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

OR use these commands
```console
sudo python3 adafruit-pitft.py --display=24hat --rotation=90 --install-type=fbcp
sudo reboot
```

### 3.1 PiTFT Mode
- FBCP (Framebuffer Copy)
    - Duplicates HDMI output
- SPI (Serial Peripheral Interface): Enables data transfer between the microcontroller or Raspberry Pi to peripherals such as displays 
    - enables script-based rendering on the TFT display

- when you want to use FBCP Mode, then your finished, otherwise continue with the next steps if you want to use SPI mode

  
#### 3.2 Configure the SPI mode
**Step 1**: Disable FBCP if enabled
```console
sudo systemctl disable fbcp
sudo systemctl stop fbcp
```

**Step 2**: Use Raspberry Config to enable SPI
```console
sudo raspi-config
```
- Interface Options → SPI → Enable
```console
sudo reboot
```

**Step 3**: Edit Boot Config
```console
sudo nano /boot/firmware/config.txt
```
- remove these dtoverlay related parameters
- delete this: dtoverlay=pitft24rv2,rotate=90,fps=60,drm
- delete this: dtoverlay=dwc2,dr_mode=host
- check if spi is set to on: dtparam=spi=on

## 4. Setup Python Virtual Environment + Initial SPI Test
**Step 1**: Setup virtual environment
- this is recommended to install python packages only for this development environment and not system-wide
- also recommended to prevent interference between multiple python projects

```console
cd ~/pi-tangibles
python3 -m venv venv
source venv/bin/activate
```

**Step 2**: install adafruit related packages
```console
pip install adafruit-blinka adafruit-circuitpython-rgb-display pillow
```

**Step 3**: SPI Test Script
- run this test script to check if spi ist setup correctly
```python
import board, busio, digitalio
from adafruit_rgb_display import ili9341
from PIL import Image, ImageDraw

# --- TFT Setup ---
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
spi = board.SPI()

disp = ili9341.ILI9341(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    rotation=0,
    baudrate=24000000
)

WIDTH = disp.width
HEIGHT = disp.height

# create test screen
image = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# color palette
colors = [
    (255, 255, 255),  # white
    (255, 255, 0),    # yellow
    (0, 255, 255),    # cyan
    (0, 255, 0),      # green
    (255, 0, 255),    # magenta
    (255, 0, 0),      # red
    (0, 0, 255),      # blue
    (0, 0, 0),        # black
]

bar_width = WIDTH // len(colors)

# upper color bars (colors)
for i, color in enumerate(colors):
    x0 = i * bar_width
    x1 = (i + 1) * bar_width
    draw.rectangle([x0, 0, x1, HEIGHT // 2], fill=color)

# bottom color bars (gray)
gray_steps = 8
gray_width = WIDTH // gray_steps
for i in range(gray_steps):
    gray = int(i * 255 / (gray_steps - 1))
    x0 = i * gray_width
    x1 = (i + 1) * gray_width
    draw.rectangle([x0, HEIGHT // 2, x1, HEIGHT], fill=(gray, gray, gray))

# send to display
disp.image(image)
print("you should see a color test screen.")

```

