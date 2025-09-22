import time, json
from websocket import create_connection, WebSocketConnectionClosedException, WebSocketException
import board, digitalio
from adafruit_stmpe610 import Adafruit_STMPE610_SPI
from typing import Final

# --- CONFIG ---
"""Server"""
SERVER_IP: Final[str] = "192.168.178.30"
SERVER_PORT: Final[str] = "8080"
SERVER = f"ws://{SERVER_IP}:{SERVER_PORT}"

"""TFT Display"""
TOUCH_SPI = board.SPI()
cs_touch = digitalio.DigitalInOut(board.CE1)
touch = Adafruit_STMPE610_SPI(TOUCH_SPI, cs_touch)
DEBOUNCE: Final[float] = 0.3


# --- WEBSOCKET ---
def connect_ws(url: str, retry_delay: int = 2):
    """ Connect to websocket server (with reconnect handling)"""
    while True:
        try:
            ws = create_connection(url, timeout=5)
            print("Connected to", url)
            return ws
        except Exception as e:
            print("WS connect failed:", e)
            time.sleep(retry_delay)


def send_message(ws, payload: dict):
    """Send JSON message to server"""
    try:
        ws.send(json.dumps(payload))
        print("Sent:", payload)
    except (WebSocketConnectionClosedException, WebSocketException) as e:
        print("Send failed:", e)
        return False
    return True


def receive_message(ws):
    """Receive JSON message from server (non-blocking)"""
    try:
        ws.settimeout(0.01)
        msg = ws.recv()
        if msg:
            print("Recv:", msg)
    except Exception:
        # handling of any thrown exception
        pass


# --- TOUCH ---
_last_touch_time = 0.0


def check_touch():
    """Check and process touch interaction and fires an actions message"""
    global _last_touch_time
    if not touch.touched:
        return None

    point = touch.touch_point
    if not point:
        return None

    now = time.time()
    if now - _last_touch_time > DEBOUNCE:
        _last_touch_time = now
        x, y, z = point
        print(f"Touch: x={x}, y={y}, z={z}")
        return {"actions": ["Jump"]}

    return None


# --- MAIN LOOP ---
def main():
    ws = connect_ws(SERVER)
    try:
        while True:
            # check cpnnection to the websocket server
            if ws and not ws.connected:
                ws.close()
                ws = connect_ws(SERVER)

            # process touch interactions
            payload = check_touch()
            if payload:
                ok = send_message(ws, payload)
                if not ok:
                    ws = connect_ws(SERVER)

            # receive and process messages
            receive_message(ws)

            time.sleep(0.02)
    finally:
        try:
            ws.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
