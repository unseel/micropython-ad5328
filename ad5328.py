from micropython import const

class Channel:
  """Channel Enum."""

  A = const(0x00)
  B = const(0x01)
  C = const(0x02)
  D = const(0x03)
  E = const(0x04)
  F = const(0x05)
  G = const(0x06)
  H = const(0x07)

class Mode:
  """Mode Enum."""
  GAIN = const(0x00)
  LDAC = const(0x01)
  POWER_DOWN = const(0x02)
  RESET = const(0x03)

class Prefix:
  """Control Enum."""
  DacWrite = const(0x00)
  Control = const(0x01)

class PresetData:
  """Preset Enum."""
  DoubleGain = const(0x030) # 0000,0011,0000
  LDACLow = const(0x000) # 0000,0000,0000
  LDACHigh = const(0x001) # 0000,0000,0001
  LDACSingle = const(0x002) # 0000,0000,0010

class Payload:
  """Data Input Register Format"""

  def __init__(self):
    self.prefix = const(0x00) # 1bit
    self.address = const(0x00) # 3bits
    self.data = const(0x00) # 12bits
  
  def set_prefix(self, prefix):
    self.prefix = prefix
  
  def set_address(self, address):
    self.address = address

  def set_data(self, data):
    self.data = data
  
  def to_bytes(self):
    result = 0
    result = result | self.prefix << 15
    result = result | self.address << 12
    result = result | self.data << 0
    return result.to_bytes(2, 'big')

class AD5328:
  """Implementation for ad5328"""

  def __init__(self, spi, cs):
    self.spi = spi
    self.cs = cs
  
  def set_gain(self):
    payload:Payload = Payload()
    payload.set_prefix(Prefix.Control)
    payload.set_address(Mode.GAIN)
    payload.set_data(PresetData.DoubleGain)
    self.__write__(payload)

  """set voltage to specified channel"""
  def set_and_update_voltage(self, channel, voltage):
    payload:Payload = self.set_voltage0(channel, voltage)
    payload.set_prefix(Prefix.DacWrite)
    self.__write__(payload)

  def set_voltage0(self, channel, voltage):
    voltage = self.check_voltage(voltage)
    payload:Payload = Payload()
    payload.set_address(channel)
    payload.set_data(voltage)
    return payload
  
  def check_voltage(self, voltage):
    if voltage < 0:
      voltage = 0
    if voltage > 4095:
      voltage = 4095
    return voltage

  def __write__(self, payload):
    self.cs.off()
    self.spi.write(payload.to_bytes())
    self.cs.on()

if __name__ == '__main__':
  payload = Payload()
  payload.set_prefix(Prefix.DacWrite)
  payload.set_address(Channel.A)
  payload.set_data(4095)
  print(payload.to_bytes())
