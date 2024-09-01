from gpiozero import LED
from time import sleep

led = LED(18)  # Change to your GPIO pin

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
