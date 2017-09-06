import gpioexp as exp
from time import sleep

exp = exp.gpioexp()

while True:
    exp.digitalWrite(0, 1)
    sleep(0.1)
    exp.digitalWritePort(0, 0)
    sleep(0.1)
