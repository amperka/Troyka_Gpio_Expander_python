import gpioexp as exp
from time import sleep

while True:
    exp.digitalWritePort(0xffff)
    sleep(0.1)
    exp.digitalWritePort(0)
    sleep(0.1)
