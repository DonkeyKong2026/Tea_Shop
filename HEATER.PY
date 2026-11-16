from gpiozero import PWMOutputDevice
from time import sleep
heater = PWMOutputDevice(18, active_high = False, frequency= 100)

print("heater on")
heater.value = 1.0

sleep(60)
heater.off()
input("Heater off waiting to exit")


