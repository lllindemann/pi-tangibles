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

def solid_rect_rgb565(width, height, color):
    r, g, b = color
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    high = (rgb565 >> 8) & 0xFF
    low = rgb565 & 0xFF
    return bytes([high, low] * (width * height))

# --- Funktion: Accelerometer-Werte in Farbe umrechnen ---
def color_from_accel(ax, ay, az, scale=3.0):
    # Empfindlicher: Werte zwischen -scale..+scale → 0..255
    def map_val(v):
        return int(min(max((v + scale) / (2 * scale) * 255, 0), 255))
    return (map_val(ax), map_val(ay), map_val(az))

# --- Hauptloop ---
while True:
    ax, ay, az = mpu.acceleration
    color = color_from_accel(ax, ay, az)

    # Rechteck direkt als Block füllen
    rect_bytes = solid_rect_rgb565(120, 160, color)
    disp._block(60, 80, 179, 239, rect_bytes)

    # Text via Pillow (kleiner Bereich reicht)
    text_img = Image.new("RGB", (120, 60))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((0, 0), f"Ax:{ax:.2f}", font=font, fill=(255, 255, 255))
    text_draw.text((0, 20), f"Ay:{ay:.2f}", font=font, fill=(255, 255, 255))
    text_draw.text((0, 40), f"Az:{az:.2f}", font=font, fill=(255, 255, 255))

    # auf Display (kleine Region)
    disp.image(text_img, x=10, y=10)

    time.sleep(0.03)  # ~30 FPS
