# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import smbus

GPIO_EXPANDER_DEFAULT_I2C_ADDRESS   = 0X2A
GPIO_EXPANDER_WHO_AM_I              = 0x00
GPIO_EXPANDER_RESET                 = 0x01
GPIO_EXPANDER_CHANGE_I2C_ADDR       = 0x02
GPIO_EXPANDER_SAVE_I2C_ADDR         = 0x03
GPIO_EXPANDER_PORT_MODE_INPUT       = 0x04
GPIO_EXPANDER_PORT_MODE_PULLUP      = 0x05
GPIO_EXPANDER_PORT_MODE_PULLDOWN    = 0x06
GPIO_EXPANDER_PORT_MODE_OUTPUT      = 0x07
GPIO_EXPANDER_DIGITAL_READ          = 0x08
GPIO_EXPANDER_DIGITAL_WRITE_HIGH    = 0x09
GPIO_EXPANDER_DIGITAL_WRITE_LOW     = 0x0A
GPIO_EXPANDER_ANALOG_WRITE          = 0x0B
GPIO_EXPANDER_ANALOG_READ           = 0x0C
GPIO_EXPANDER_PWM_FREQ              = 0x0D
GPIO_EXPANDER_ADC_SPEED             = 0x0E


class Gpio_exp(object):
    """Troyka gpio expander."""

    def __init__(self, gpioexp_address=GPIO_EXPANDER_DEFAULT_I2C_ADDRESS,
                 i2c=1):

        # Setup I2C interface for accelerometer and magnetometer.
        self._gpioexp = smbus.SMBus(i2c)
        self._gpioexp.write_byte(GPIO_EXPANDER_RESET)

    def digitalReadPort(self):
        port = self._gpioexp.read_word_data(GPIO_EXPANDER_DIGITAL_READ)
        return port

    def digitalWritePort(self, value):
        self._gpioexp.write_word_data(GPIO_EXPANDER_DIGITAL_WRITE_HIGH, value)
        self._gpioexp.write_word_data(GPIO_EXPANDER_DIGITAL_WRITE_LOW, ~value)        

    def digitalWrite(self, pin, value):
        sendData = 1<<pin
        if value:
            self._gpioexp.write_word_data(DIGITAL_WRITE_HIGH, sendData)
        else:
            self._gpioexp.write_word_data(DIGITAL_WRITE_LOW, sendData)
'''
#    def pinMode(pin, mode):
#        if mode
        
    def analogWrite(self, pin, value):
        valWord = value * 65535
        valH = (valWord>>8) & 0xff
        valL = valWord & 0xff
        sendData = [pin, valH, valL]
        self._gpioexp.writeList(GPIO_EXPANDER_ANALOG_WRITE, sendData)
    
    def pwmFreq(self, freq):
        self._gpioexp.write16(GPIO_EXPANDER_PWM_FREQ, freq)
    
    def changeAddr(self, newAddr):
        self._gpioexp.write8(GPIO_EXPANDER_CHANGE_I2C_ADDR, newAddr)


    def saveAddr(self):
        self._gpioexp.writeRaw8(GPIO_EXPANDER_SAVE_I2C_ADDR)

    def reset(self):
        self._gpioexp.writeRaw8(GPIO_EXPANDER_RESET)

    def digitalRead(self, pin):
        mask = 1 << pin
        return (digitalReadPort() & mask)

    def analogRead(self, pin):
        self._gpioexp.write8(GPIO_EXPANDER_ANALOG_READ, pin)
        resilt = self._gpioexp._bus.i2c_read_device(self._address, 2)
'''