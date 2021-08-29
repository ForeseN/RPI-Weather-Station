import time
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    print(f"The temp is {temperature}")
    time.sleep(1)
    
    