import time
import board
import busio
import digitalio
from adafruit_stmpe610 import Adafruit_STMPE610_SPI

# SPI Setup
spi = board.SPI()
cs_touch = digitalio.DigitalInOut(board.CE1)  # CE1 = Touch
touch = Adafruit_STMPE610_SPI(spi, cs_touch)

print("Starte Touch-Test – tippe aufs Display...")

while True:
    if touch.touched:
        point = touch.touch_point  # (x, y, z)
        if point:
            x, y, z = point
            print(f"Touch: X={x}, Y={y}, Druck={z}")
            while touch.touched:  # wait until finger is released
                time.sleep(0.05)
    time.sleep(0.05)
