#!/usr/bin/env python3
import spidev
import gpiod
import time
from gpiod.line import Direction, Value

CHIP   = "/dev/gpiochip0"
CS     = 18

WIDTH  = 400
HEIGHT = 240

REV = bytes(int(f'{i:08b}'[::-1], 2) for i in range(256))

def setup_cs():
    req = gpiod.request_lines(CHIP, consumer="sharp", config={
        (CS,): gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)
    })
    return req

def cs_high(req): req.set_value(CS, Value.ACTIVE)
def cs_low(req):  req.set_value(CS, Value.INACTIVE)

def clear(spi, req):
    cs_high(req)
    spi.writebytes2(bytes([REV[0x04], 0x00]))
    cs_low(req)
    time.sleep(0.00001)

def fill(spi, req, pixel):
    rp = REV[pixel]
    buf = bytearray(1 + HEIGHT * (1 + WIDTH//8 + 1) + 1)
    i = 0
    buf[i] = REV[0x01]; i += 1
    for line in range(1, HEIGHT + 1):
        buf[i] = REV[line]; i += 1
        for _ in range(WIDTH // 8):
            buf[i] = rp; i += 1
        buf[i] = 0x00; i += 1
    buf[i] = 0x00
    cs_high(req)
    spi.writebytes2(buf)
    cs_low(req)

def checkerboard(spi, req):
    BLOCK = 20
    buf = bytearray(1 + HEIGHT * (1 + WIDTH//8 + 1) + 1)
    i = 0
    buf[i] = REV[0x01]; i += 1
    for line in range(1, HEIGHT + 1):
        buf[i] = REV[line]; i += 1
        row_block = (line - 1) // BLOCK
        for col_byte in range(WIDTH // 8):
            byte = 0
            for bit in range(8):
                col = col_byte * 8 + bit
                col_block = col // BLOCK
                if (row_block + col_block) % 2 == 0:
                    byte |= (1 << bit)
            buf[i] = REV[byte]; i += 1
        buf[i] = 0x00; i += 1
    buf[i] = 0x00
    cs_high(req)
    spi.writebytes2(buf)
    cs_low(req)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 2_000_000
spi.mode = 0

req = setup_cs()

print("clear");        clear(spi, req);        time.sleep(1)
print("all black");    fill(spi, req, 0xFF);   time.sleep(2)
print("all white");    fill(spi, req, 0x00);   time.sleep(2)
print("checkerboard"); checkerboard(spi, req)

input("press enter to clear...")
clear(spi, req)

spi.close()
req.release()
