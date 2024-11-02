import spidev
import RPi.GPIO as GPIO
from mfrc522 import MFRC522

class MFRC522Custom(MFRC522):
    def __init__(self, bus, device, speed_hz=1000000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = speed_hz
        super().__init__()

    def _write(self, register, value):
        self.spi.xfer2([((register << 1) & 0x7E), value])

    def _read(self, register):
        return self.spi.xfer2([((register << 1) & 0x7E) | 0x80, 0])[1]

    def close(self):
        self.spi.close()
        GPIO.cleanup()
