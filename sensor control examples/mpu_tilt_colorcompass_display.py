import time
import board
import busio
import digitalio
from adafruit_rgb_display import ili9341
from PIL import Image, ImageDraw, ImageFont
import adafruit_mpu6050

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

image = Image.new("RGB", (disp.width, disp.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# --- MPU6050 Setup ---
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

# --- Funktion: Accelerometer-Werte in Farbe umrechnen ---
def color_from_accel(ax, ay, az, scale=3.0):
    # Empfindlicher: Werte zwischen -scale..+scale → 0..255
    def map_val(v):
        return int(min(max((v + scale) / (2 * scale) * 255, 0), 255))
    return (map_val(ax), map_val(ay), map_val(az))

# --- Hauptloop ---
while True:
    ax, ay, az = mpu.acceleration  # Beschleunigung in m/s²
    color = color_from_accel(ax, ay, az)

    # Bildschirm leeren (schneller: direkt Hintergrund schwarz füllen)
    draw.rectangle((0, 0, disp.width, disp.height), fill=(0, 0, 0))

    # draw rectangle 
    draw.rectangle((60, 80, 180, 240), fill=color)

    # show acc values
    draw.text((10, 10), f"Ax:{ax:.2f}", font=font, fill=(255, 255, 255))
    draw.text((10, 30), f"Ay:{ay:.2f}", font=font, fill=(255, 255, 255))
    draw.text((10, 50), f"Az:{az:.2f}", font=font, fill=(255, 255, 255))

    # update display
    disp.image(image)
    time.sleep(0.01)
