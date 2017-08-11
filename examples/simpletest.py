
import time

import Troyka_gpio_expander


gpioexp = Troyka_gpio_expander.GPIO_EXPANDER()

print('read analog')
while True:
    b = gpioexp.digitalReadPort()
    print(b)
    # Wait half a second and repeat.
    time.sleep(0.5)
