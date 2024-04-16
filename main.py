import network
import socket
import time
from machine import Pin
import _thread

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid = ''
password = ''
wlan.connect(ssid, password)

max_wait = 30  # Increase the timeout to 30 seconds

while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection... ({}s remaining)'.format(max_wait))
    time.sleep(1)

if wlan.status() != 3:
    print('Network connection failed')
    print('Connection status:', wlan.status())
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP address:', status[0])
    
    # Set up onboard LED connected to GPIO25 pin
    led = Pin("LED", Pin.OUT)
    led.value(1)  # Turn on the onboard LED

# Set up GPIO17 pin as output
gpio_pin = Pin(17, Pin.OUT)

# Variable to control the yellow thread
yellow_thread_running = False

# Function to handle the yellow signal in a separate thread
def yellow_thread():
    global yellow_thread_running
    while yellow_thread_running:
        gpio_pin.value(0)
        time.sleep(0.25)
        gpio_pin.value(1)
        time.sleep(0.25)

# Set up socket to listen for TCP packets
import socket

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)
print('Listening on', addr)

while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            data = cl.recv(1024)
            signal = data.decode('utf-8')
            if signal == "red":
                yellow_thread_running = False
                gpio_pin.value(1)
            elif signal == "green":
                yellow_thread_running = False
                gpio_pin.value(0)
            elif signal == "yellow":
                yellow_thread_running = True
                _thread.start_new_thread(yellow_thread, ())
            else:
                yellow_thread_running = False
                gpio_pin.value(0)
        cl.close()
    except OSError as e:
        cl.close()
        print('Connection closed')


