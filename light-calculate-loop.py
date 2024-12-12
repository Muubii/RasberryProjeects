from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)  

n = 0

while True:
    led.toggle()
    print(f"13 times {n} is {13 * n}")
    n = n + 1
    sleep(0.5)
