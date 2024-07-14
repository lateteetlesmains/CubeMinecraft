import network
import socket
import machine
import neopixel
import time

# Set up the NeoPixel strip
pixels = neopixel.NeoPixel(machine.Pin(5), 7)

ssid = 'lampe-Olivier'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
while ap.active() == False:
    pass

print('Connection successful')
print(ap.ifconfig())

# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.4.1', 80))
sock.listen(5)

print('Access Point "lampe-Olivier" started')

def hex_to_rgb(hex, brightness=255):
    hex = hex.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return tuple(int(c * int(brightness) / 255) for c in rgb)

def set_color(r, g, b):
    for i in range(7):
        pixels[i] = (r, g, b)
    pixels.write()
for i in range(7):  # set all 7 pixels to red
        pixels[i] = (0, 0, 255)
        pixels.write()
time.sleep(0.5)
for i in range(7):  # set all 7 pixels to red
        pixels[i] = (255, 255, 255)
        pixels.write()
time.sleep(0.5)
for i in range(7):  # set all 7 pixels to red
        pixels[i] = (255, 0, 0)
        pixels.write()
time.sleep(0.5)            
for i in range(7):  # set all 7 pixels to red
        pixels[i] = (0, 0, 0)
        pixels.write()
time.sleep(0.5)

while True:
    conn, addr = sock.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Request: %s' % request)

    try:
        if 'GET /set_color' in request:
            color_str = request.split('color=')[1].split('&')[0]
            brightness = request.split('brightness=')[1].split(' ')[0]
            r, g, b = hex_to_rgb(color_str, brightness)
            set_color(r, g, b)
            conn.sendall(b'200 OK')  # Send a response back to the client
        elif 'GET / ' in request:
            with open('index.html', 'r') as f:
                html_page = f.read()
            conn.sendall(html_page.encode())
        elif 'GET /style.css' in request:
            with open('style.css', 'r') as f:
                css_page = f.read()
            conn.sendall(css_page.encode())
        elif 'GET /script.js' in request:
            with open('script.js', 'r') as f:
                js_page = f.read()
            conn.sendall(js_page.encode())
        else:
            conn.sendall(b'404 Not Found')
    except Exception as e:
        print('Error processing request:', e)
        conn.sendall(b'500 Internal Server Error')

    conn.close()