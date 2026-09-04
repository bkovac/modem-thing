#!/usr/bin/env python3
import gpiod
import time
from gpiod.line import Direction, Value

CHIP   = "/dev/gpiochip0"
MOSI   = 16
CLK    = 19
CS     = 18

WIDTH  = 400
HEIGHT = 240

def setup():
    req = gpiod.request_lines(CHIP, consumer="sharp", config={
        (MOSI, CLK, CS): gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)
    })
    return req

def pin(req, line, val):
    req.set_value(line, Value.ACTIVE if val else Value.INACTIVE)

def send_byte(req, b):
    for _ in range(8):
        pin(req, MOSI, b & 1)
        pin(req, CLK, 1)
        pin(req, CLK, 0)
        b >>= 1

def send(req, data):
    pin(req, CS, 1)
    for b in data:
        send_byte(req, b)
    pin(req, CS, 0)

def clear(req):
    send(req, [0x04, 0x00])
    time.sleep(0.00001)

def fill(req, pixel):
    buf = [0x01]
    for line in range(1, HEIGHT + 1):
        buf.append(line)
        p = pixel if line % 2 == 0 else (pixel ^ 0xFF)
        buf.extend([p] * (WIDTH // 8))
        buf.append(0x00)
    buf.append(0x00)
    send(req, buf)

req = setup()

print("clear");        clear(req);        time.sleep(1)
print("all black");    fill(req, 0xFF);   time.sleep(2)
print("all white");    fill(req, 0x00);   time.sleep(2)
print("checkerboard"); fill(req, 0xAA);   time.sleep(2)
print("clear");        clear(req)

req.release()
