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
