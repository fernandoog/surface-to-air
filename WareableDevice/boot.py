# Boot.py file include and wifi config

from machine import Pin
import usocket as socket
import socket
import network
import dht
import esp
import gc
gc.collect()

esp.osdebug(None)

ssid = 'WeWork'
password = 'P@ssw0rd'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Wifi Connection Successful')
print(station.ifconfig())

sensor = dht.DHT11(Pin(14))