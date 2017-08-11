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
import struct

"""
# Minimal constants carried over from Arduino library:
LSM303_ADDRESS_ACCEL = (0x32 >> 1)  # 0011001x
LSM303_ADDRESS_MAG   = (0x3C >> 1)  # 0011110x
                                         # Default    Type
LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20 # 00000111   rw
LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23 # 00000000   rw
LSM303_REGISTER_ACCEL_OUT_X_L_A   = 0x28
LSM303_REGISTER_MAG_CRB_REG_M     = 0x01
LSM303_REGISTER_MAG_MR_REG_M      = 0x02
LSM303_REGISTER_MAG_OUT_X_H_M     = 0x03

# Gain settings for set_mag_gain()
LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3
LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9
LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5
LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0
LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7
LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6
LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1

"""
GPIO_EXPANDER_DEFAULT_I2C_ADDRESS   = 0X2A
GPIO_EXPANDER_WHO_AM_I              = 0x00  # Отдали UID
GPIO_EXPANDER_RESET                 = 0x01  # сброс
GPIO_EXPANDER_CHANGE_I2C_ADDR       = 0x02  # сменить I2C-адрес вручную
GPIO_EXPANDER_SAVE_I2C_ADDR         = 0x03  # Сохранить текущий адрес во флэшчтобы стартовать при последующих включениях с него
GPIO_EXPANDER_PORT_MODE_INPUT       = 0x04  # настроили пины на вход
GPIO_EXPANDER_PORT_MODE_PULLUP      = 0x05  # .. вход с поддтяжкой вверх
GPIO_EXPANDER_PORT_MODE_PULLDOWN    = 0x06  # .. с подтяжкой вниз
GPIO_EXPANDER_PORT_MODE_OUTPUT      = 0x07  # .. на выход
GPIO_EXPANDER_DIGITAL_READ          = 0x08  # считали состояние виртуального порта
GPIO_EXPANDER_DIGITAL_WRITE_HIGH    = 0x09  # Выставили пины виртуального порта в высокий уровень
GPIO_EXPANDER_DIGITAL_WRITE_LOW     = 0x0A # .. в низкий уровень
GPIO_EXPANDER_ANALOG_WRITE          = 0x0B # Запустить ШИМ
GPIO_EXPANDER_ANALOG_READ           = 0x0C # Считать значениие с АЦП
GPIO_EXPANDER_PWM_FREQ              = 0x0D # установка частоты ШИМ (общая для всех PWM-пинов)
GPIO_EXPANDER_ADC_SPEED             = 0x0E # Смена скорости АЦП. 0-8. Чем меньше - тем выше скорость, но больше требования к мощности источника измеряемого напряжения


class GPIO_EXPANDER(object):
    """Troyka gpio expander."""

    def __init__(self, gpioexp_address=GPIO_EXPANDER_DEFAULT_I2C_ADDRESS,
                 i2c=None, **kwargs):
        """Initialize the LSM303 accelerometer & magnetometer.  The hires
        boolean indicates if high resolution (12-bit) mode vs. low resolution
        (10-bit, faster and lower power) mode should be used.
        """
        # Setup I2C interface for accelerometer and magnetometer.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._gpioexp = i2c.get_i2c_device(gpioexp_address, **kwargs)
        self._gpioexp.writeRaw8(GPIO_EXPANDER_RESET)

        # Enable the accelerometer
#        self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x27)
        # Select hi-res (12-bit) or low-res (10-bit) output mode.
        # Low-res mode uses less power and sustains a higher update rate,
        # output is padded to compatible 12-bit units.
 #       if hires:
#            self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0b00001000)
#        else:
#            self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0)
#        # Enable the magnetometer
#        self._mag.write8(LSM303_REGISTER_MAG_MR_REG_M, 0x00)

    def digitalReadPort(self):
        port = self._gpioexp.readU16(GPIO_EXPANDER_DIGITAL_READ)
        return port

    def digitalWritePort(self, value):
        self._gpioexp.write16(GPIO_EXPANDER_DIGITAL_WRITE_HIGH, value)
        self._gpioexp.write16(GPIO_EXPANDER_DIGITAL_WRITE_LOW, ~value)        

    def digitalWrite(self, pin, value):
        sendData = 1<<pin
        if value:
            self._gpioexp.write16(DIGITAL_WRITE_HIGH, sendData)
        else:
            self._gpioexp.write16(DIGITAL_WRITE_LOW, sendData)

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
    def getUID(self):
    def adcSpeed(speed):

    def 

    def read(self):
        """Read the accelerometer and magnetometer value.  A tuple of tuples will
        be returned with:
          ((accel X, accel Y, accel Z), (mag X, mag Y, mag Z))
        """
        # Read the accelerometer as signed 16-bit little endian values.
        accel_raw = self._accel.readList(LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
        accel = struct.unpack('<hhh', accel_raw)
        # Convert to 12-bit values by shifting unused bits.
        accel = (accel[0] >> 4, accel[1] >> 4, accel[2] >> 4)
        # Read the magnetometer.
        mag_raw = self._mag.readList(LSM303_REGISTER_MAG_OUT_X_H_M, 6)
        mag = struct.unpack('>hhh', mag_raw)
        return (accel, mag)

    def set_mag_gain(gain=LSM303_MAGGAIN_1_3):
        """Set the magnetometer gain.  Gain should be one of the following
        constants:
         - LSM303_MAGGAIN_1_3 = +/- 1.3 (default)
         - LSM303_MAGGAIN_1_9 = +/- 1.9
         - LSM303_MAGGAIN_2_5 = +/- 2.5
         - LSM303_MAGGAIN_4_0 = +/- 4.0
         - LSM303_MAGGAIN_4_7 = +/- 4.7
         - LSM303_MAGGAIN_5_6 = +/- 5.6
         - LSM303_MAGGAIN_8_1 = +/- 8.1
        """
        self._mag.write8(LSM303_REGISTER_MAG_CRB_REG_M, gain)
'''
