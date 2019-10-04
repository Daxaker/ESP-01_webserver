# This is your main script.
import machine
import time
import network
import usocket as socket

pin = machine.Pin(0, machine.Pin.OUT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ssid', 'password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def start_server():
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        if "GET /?led=on" in request:
            pin.on()
        if "GET /?led=off" in request:
            pin.off()
        print(request)
        response = "Ok"
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-type: text/html\n")
        conn.send("Connection: close\n")
        conn.sendall(response)
        conn.close()

do_connect()
start_server()
