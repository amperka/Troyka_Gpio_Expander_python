import gpioexp
from time import sleep

exp = gpioexp.gpioexp()

while True:
    exp.digitalWrite(0, 1)
    sleep(0.1)
    exp.digitalWrite(0, 0)
    sleep(0.1)
    exp.analogWrite(1, exp.analogRead(3))
    print(exp.analogRead(3))
