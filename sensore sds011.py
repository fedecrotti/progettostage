"""This module provides an abstraction for the SDS011 air partuclate densiry sensor."""
import struct
import serial
print("Lettura dati dalla porta: COM 3")
#TODO: Commands against the sensor should read the reply and return success status.
class SDS011(object):
    """Provides method to read from a SDS011 air particlate density sensor using UART."""
    HEAD = b'\xaa'
    TAIL = b'\xab'
    CMD_ID = b'\xb4'
    # The sent command is a read or a write
    READ = b"\x00"
    WRITE = b"\x01"
    REPORT_MODE_CMD = b"\x02"
    ACTIVE = b"\x00"
    PASSIVE = b"\x01"
    QUERY_CMD = b"\x04"
    # The sleep command ID
    SLEEP_CMD = b"\x06"
    # Sleep and work byte
    SLEEP = b"\x00"
    WORK = b"\x01"
    # The work period command ID
    WORK_PERIOD_CMD = b'\x08'


ser = serial.Serial(
    port="COM3",
    baudrate=9600,
    timeout=2
)


def _execute(cmd_bytes):
    """Writes a byte sequence to the serial."""
    ser.writeline(cmd_bytes)
def _get_reply():
    """Read reply from device."""
    raw = ser.readline(size=10)
    data = raw[2:8]
    if len(data) == 0:
        return None
    if (sum(d for d in data) & 255) != raw[8]:
        return None  #TODO: also check cmd id
    return raw
def cmd_begin(self):
    """Get command header and command ID bytes.@rtype: list"""
    return self.HEAD + self.CMD_ID
def set_report_mode(self, read=False, active=False):
    """Get sleep command. Does not contain checksum and tail.@rtype: list"""
    cmd = cmd_begin()
    cmd += (self.REPORT_MODE_CMD
            + (self.READ if read else self.WRITE)
            + (self.ACTIVE if active else self.PASSIVE)
            + b"\x00" * 10)
    cmd = self._finish_cmd(cmd)
    _execute(cmd)
    _get_reply()
def query(self):
    """Query the device and read the data.@return: Air particulate density in micrograms per cubic meter.@rtype: tuple(float, float) -> (PM2.5, PM10)"""
    cmd = cmd_begin()
    cmd += (self.QUERY_CMD
            + b"\x00" * 12)
    cmd = self._finish_cmd(cmd)
    _execute(cmd)
    raw = _get_reply()
    if raw is None:
        return None  #TODO:
    data = struct.unpack('<HH', raw[2:6])
    pm25 = data[0] / 10.0
    pm10 = data[1] / 10.0
    return (pm25, pm10)



    raw = struct.unpack('<HHxxBBB', data[2:])
    checksum = sum(v for v in data[2:8]) % 256
    if checksum != data[8]:
        return None
    pm25 = raw[0] / 10.0
    pm10 = raw[1] / 10.0
    return (pm25, pm10)




def read(self):
    """Read sensor data.@return: PM2.5 and PM10 concetration in micrograms per cube meter.@rtype: tuple(float, float) - first is PM2.5."""
    byte = 0
    while byte != self.HEAD:
        byte = self.ser.read(size=1)
        d = self.ser.read(size=10)
        if d[0:1] == b"\xc0":
            data = self._process_frame(byte + d)
            return data