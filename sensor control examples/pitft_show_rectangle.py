import board
import busio
import digitalio
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

# create image buffer ---
image = Image.new("RGB", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

# draw rectangle
draw.rectangle(
    (50, 50, 150, 150),  # (x1, y1, x2, y2)
    fill=(0, 0, 255)     # color: blue
)

# update display
disp.image(image)
