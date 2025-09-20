import time
import requests
from io import BytesIO
from PIL import Image, ImageSequence
import board, digitalio
from adafruit_rgb_display import ili9341

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
    rotation=90,
    baudrate=24000000
)

WIDTH = disp.width
HEIGHT = disp.height

# --- Convert RGB888 to RGB565 ---
def rgb_to_rgb565(image):
    "Convert PIL.Image (RGB888) in RGB565-Bytearray"
    rgb_bytes = bytearray()
    pixels = image.getdata()
    for r, g, b in pixels:
        "use bitmasking for conversion"
        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        rgb_bytes.append((rgb565 >> 8) & 0xFF)
        rgb_bytes.append(rgb565 & 0xFF)
    return bytes(rgb_bytes)

# --- Download GIF ---
url_walking = "https://img.itch.zone/aW1hZ2UvMjA2MjMyMy8xMjEyNjQ3OC5naWY=/347x500/2OLf%2Fz.gif"
response = requests.get(url_walking)
gif = Image.open(BytesIO(response.content))

# --- Preprocessing Frames ---
frames = []
for frame in ImageSequence.Iterator(gif):
    frame_resized = frame.convert("RGB").resize((HEIGHT, WIDTH))
    frame_resized = frame_resized.transpose(Image.ROTATE_90)
    frame565 = rgb_to_rgb565(frame_resized)
    frames.append(frame565)

print(f"Preprocessed {len(frames)} frames.")

# --- Frame-Loop ---
while True:
    for frame_data in frames:
        disp._block(0, 0, WIDTH - 1, HEIGHT - 1, frame_data)
        time.sleep(0.05)  # 20 FPS
