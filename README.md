# AD5328(WIP)

## Description

`AD5328`是一个8通道、12位精度的数模转换器，兼容`SPI`, `QSPI`, `Microwave`和`DSP`接口。

## Features

1. 给指定通道施加指定的电压

## Example

```python
from machine import SPI, Pin
import ad5328

# define spi/cs, esp32-s for example
spi = SPI(2, 10000)
cs = machine.Pin(5, Pin.OUT)

# init dac8568
ad5328_ = ad5328.AD5328(spi, cs)

# set voltage
ad5328_.set_and_update_voltage(ad5328.Channel.A, 4095)
```

## Reference

- [data sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ad5308_5318_5328.pdf)

