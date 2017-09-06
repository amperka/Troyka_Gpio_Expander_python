# The MIT License (MIT)

import wiringpi as wp

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

def getPiI2CBusNumber():
    """
    Returns the I2C bus number (/dev/i2c-#) for the Raspberry Pi being used.

    Courtesy quick2wire-python-api
    https://github.com/quick2wire/quick2wire-python-api
    """
    try:
        with open('/proc/cpuinfo','r') as f:
            for line in f:
                if line.startswith('Revision'):
                    return 1
    except:
        return 0

class gpioexp(object):
    """Troyka gpio expander."""

    def __init__(self, gpioexp_address=GPIO_EXPANDER_DEFAULT_I2C_ADDRESS):

        # Setup I2C interface for accelerometer and magnetometer.
        wp.wiringPiSetup()
        self._i2c = wp.I2C()
        self._io = self._i2c.setupInterface('/dev/i2c-' + str(getPiI2CBusNumber()), gpioexp_address)
#        self._gpioexp.write_byte(self._addr, GPIO_EXPANDER_RESET)
    def reverse_uint16(self, data):
        result = ((data & 0xff) << 8) | ((data>>8) & 0xff)
        return result

    def digitalReadPort(self):
        port = self.reverse_uint16(self._i2c.readReg16(self._io, GPIO_EXPANDER_DIGITAL_READ))
        return port

    def digitalWritePort(self, value):
        value = self.reverse_uint16(value)
        self._i2c.writeReg16(self._io, GPIO_EXPANDER_DIGITAL_WRITE_HIGH, value)
        self._i2c.writeReg16(self._io, GPIO_EXPANDER_DIGITAL_WRITE_LOW, ~value)

    def digitalWrite(self, pin, value):
        sendData = (0x0001<<pin)
        if value:
            self._i2c.writeReg16(self._io, GPIO_EXPANDER_DIGITAL_WRITE_HIGH, sendData)
        else:
            self._i2c.writeReg16(self._io, GPIO_EXPANDER_DIGITAL_WRITE_LOW, sendData)

    def analogRead16(self, pin):
        self._i2c.writeReg16(self._io, GPIO_EXPANDER_ANALOG_READ, pin)
        return self.reverse_uint16(self._i2c.readReg16(self._io, GPIO_EXPANDER_ANALOG_READ))

    def analogRead(self, pin):
        return self.analogRead16(pin)/4095.0


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
