import time
import math
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
disp = ili9341.ILI9341(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin,
                       rotation=0, baudrate=24000000)

# --- MPU6050 Setup ---
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

# --- Display Setup ---
image = Image.new("RGB", (disp.width, disp.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

while True:
    # read vector3 values of gyroskop and accelerometer
    ax, ay, az = mpu.acceleration
    gx, gy, gz = mpu.gyro

    # compute ROLL and PITCH with acc values
    roll = math.degrees(math.atan2(ay, az))
    pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

    # TODO: compute yaw 

    # render black background (rectangle with full display size)
    draw.rectangle((0, 0, disp.width, disp.height), fill=(0, 0, 0))

    # render three text lines, every line shows one tilt dimension (roll, pitch, yaw)
    draw.text((10, 10), f"Roll:  {roll:.2f}°", font=font, fill=(255, 255, 255))
    draw.text((10, 30), f"Pitch: {pitch:.2f}°", font=font, fill=(255, 255, 255))
    draw.text((10, 50), f"Gz:    {gz:.2f}", font=font, fill=(255, 255, 255))

    # update display
    disp.image(image)
    time.sleep(0.05)
