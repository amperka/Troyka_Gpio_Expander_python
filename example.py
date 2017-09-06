import gpioexp as exp
from time import sleep

exp = exp.gpioexp()

while True:
    exp.digitalWritePort(0xffff)
    sleep(0.1)
    exp.digitalWritePort(0)
    sleep(0.1)
