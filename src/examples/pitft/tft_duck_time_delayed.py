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

# --- RGB888 -> RGB565 ---
def rgb_to_rgb565(image):
    rgb_bytes = bytearray()
    for r, g, b in image.getdata():
        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        rgb_bytes.append((rgb565 >> 8) & 0xFF)
        rgb_bytes.append(rgb565 & 0xFF)
    return bytes(rgb_bytes)

# --- GIF URLs ---
gif_urls = [
    "https://img.itch.zone/aW1hZ2UvMjA2MjMyMy8xMjEyNjQ3Ni5naWY=/347x500/GDzpnO.gif", # Idle Duck
    "https://img.itch.zone/aW1hZ2UvMjA2MjMyMy8xMjEyNjQ3OC5naWY=/347x500/2OLf%2Fz.gif",  # Walking Duck
    "https://img.itch.zone/aW1hZ2UvMjA2MjMyMy8xMjEyNjQ3Ny5naWY=/347x500/jnAYn8.gif",  # Running Duck
]

# --- Download & Preprocess GIFs ---
all_gifs = []

for url in gif_urls:
    print(f"Load GIF: {url}")
    response = requests.get(url)
    gif = Image.open(BytesIO(response.content))

    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame_resized = frame.convert("RGB").resize((HEIGHT, WIDTH))
        frame_resized = frame_resized.transpose(Image.ROTATE_90)
        frame565 = rgb_to_rgb565(frame_resized)
        frames.append(frame565)

    print(f"Preprocessed {len(frames)} frames.")
    all_gifs.append(frames)

print("All GIFs were loaded and preprocessed.")

# --- Animation Loop ---
current_gif = 0
while True:
    frames = all_gifs[current_gif]
    start_time = time.time()

    i = 0
    while True:
        disp._block(0, 0, WIDTH - 1, HEIGHT - 1, frames[i])
        time.sleep(0.05)  # 20 FPS

        # switch to next frame
        i = (i + 1) % len(frames)

        # check if 5 seconds elapsed
        if time.time() - start_time >= 5:
            current_gif = (current_gif + 1) % len(all_gifs)
            break
