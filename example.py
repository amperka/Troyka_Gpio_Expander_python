import gpioexp
from time import sleep

exp = gpioexp.gpioexp()

while True:
    exp.digitalWrite(0, 1)
    sleep(0.1)
    exp.digitalWritePort(0, 0)
    sleep(0.1)
    print(exp.analogRead(3))
