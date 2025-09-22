import time
import requests
from io import BytesIO
from PIL import Image, ImageSequence
import board, digitalio
from adafruit_rgb_display import ili9341
from adafruit_stmpe610 import Adafruit_STMPE610_SPI

# --- TFT Setup ---
cs_disp = digitalio.DigitalInOut(board.CE0)
dc_disp = digitalio.DigitalInOut(board.D25)
reset_disp = digitalio.DigitalInOut(board.D24)
spi = board.SPI()

disp = ili9341.ILI9341(
    spi,
    cs=cs_disp,
    dc=dc_disp,
    rst=reset_disp,
    rotation=90,       # Display dreht das Bild intern
    baudrate=24000000
)

WIDTH = disp.width
HEIGHT = disp.height

# --- Touch Setup ---
cs_touch = digitalio.DigitalInOut(board.CE1)
touch = Adafruit_STMPE610_SPI(spi, cs_touch)

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

# --- Download & Preprocess alle GIFs ---
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

# --- Animation Loop mit Touch ---
current_gif = 0

while True:
    frames = all_gifs[current_gif]
    i = 0

    while True:
        disp._block(0, 0, WIDTH - 1, HEIGHT - 1, frames[i])
        time.sleep(0.05)  # 20 FPS

        # switch to next frame
        i = (i + 1) % len(frames)

        if touch.touched:
            point = touch.touch_point

            while touch.touched:
                     time.sleep(0.05)

            if point is not None:
                x, y, z = point
                print(f"Touch erkannt: X={x}, Y={y}, Z={z}")

                current_gif = (current_gif + 1) % len(all_gifs)
                frames = all_gifs[current_gif]
                i = 0  # Start von Frame 0
                print(f"Wechsel zu GIF {current_gif + 1}")
                break

                


# Frame anzeigen
#    disp.image(frames[i])
#    time.sleep(0.05)  # ~20 FPS
#
#    # Nächster Frame
#    i = (i + 1) % len(frames)
#
#    # Touch prüfen
#    if touch.touched:
#        point = touch.touch_point
#        if point:
#            x, y, z = point
#            print(f"Touch erkannt: X={x}, Y={y}, Druck={z}")
#
#            # Zum nächsten GIF wechseln
#            current_gif = (current_gif + 1) % len(all_gifs)
#            frames = all_gifs[current_gif]
#            i = 0  # Start von Frame 0
#            print(f"Wechsel zu GIF {current_gif + 1}")
#
#            # Warten bis Finger weg, um Mehrfachwechsel zu verhindern
#            while touch.touched:
#                time.sleep(0.05)
