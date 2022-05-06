import asyncio
import board
import pwmio  # using this instead of pulseio
import neopixel
import wifi
from adafruit_wsgi.wsgi_app import WSGIApp
import wsgiserver as server

# TODO: figure out a fix to the strip flashing to full brightness on boot
# RGBW strip: 31 and below is effectively 0, range is 0-65535
rr = pwmio.PWMOut(board.A0, frequency=5000, duty_cycle=0)
gg = pwmio.PWMOut(board.A1, frequency=5000, duty_cycle=0)
bb = pwmio.PWMOut(board.A2, frequency=5000, duty_cycle=0)
ww = pwmio.PWMOut(board.A3, frequency=5000, duty_cycle=0)

currentColor = (0, 16, 0)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print(
        "WiFi secrets for ssid and password are kept in secrets.py,"
        + " please add them there!"
    )
    raise

print("Connecting wifi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
HOST = repr(wifi.radio.ipv4_address)
PORT = 80  # Port to listen on
print(HOST, PORT)

html = ""
try:
    with open("/index.html", "r") as f:
        html = f.readlines()
except OSError:  # Typically when the filesystem isn't writeable...
    print("Error loading index.html")
    raise

print("Starting web server...")
web_app = WSGIApp()

@web_app.route("/")
def homepage(request):  # pylint: disable=unused-argument
    text = html
    return ("200 OK", [], text)

@web_app.route("/rgbwj/<r>/<g>/<b>/<w>")
def rgbwj(request, r, g, b, w):  # pylint: disable=unused-argument
    global currentColor, rr, gg, bb, ww
    print(f"before {currentColor}")
    currentColor = (int(r), int(g), int(b))
    print(f"after {currentColor}")
    rr.duty_cycle = int(r) * 256
    gg.duty_cycle = int(g) * 256
    bb.duty_cycle = int(b) * 256
    ww.duty_cycle = int(w) * 256
    json = """
        {
            "color": {
                "r": """ + r + """,
                "g": """ + g + """,
                "b": """ + b + """,
                "w": """ + w + """
            }
        }
    """
    print(json)
    return ("200 OK", [], json)


wsgiServer = server.WSGIServer(PORT, application=web_app)
print(f"open this IP in your browser: http://{HOST}:{PORT}/")
wsgiServer.start()


class WebServerControls:
    """The controls to allow you to vary the web server."""
    def __init__(self):
        self.reverse = False
        self.wait = 0.01

class AnimationControls:
    """The controls to allow you to vary the rainbow and blink animations."""
    def __init__(self):
        self.reverse = False
        self.wait = 0.0
        self.delay = 0.5

async def web_server(controls):
    """Run web server in the background"""
    while True:
        global wsgiServer
        wsgiServer.update_poll()
        await asyncio.sleep(controls.wait)

async def blink(controls):
    """Blink the main neopixel"""
    while True:
        global currentColor, pixel
        pixel.fill(currentColor)
        await asyncio.sleep(controls.delay)

        pixel.fill((0, 0, 0))
        await asyncio.sleep(controls.delay)
        await asyncio.sleep(controls.wait)


async def main():
    web_server_controls = WebServerControls()
    web_server_task = asyncio.create_task(web_server(web_server_controls))

    animation_controls = AnimationControls()
    blink_task = asyncio.create_task(blink(animation_controls))

    # This will run forever, because no tasks ever finish.
    await asyncio.gather(web_server_task, blink_task)

asyncio.run(main())
