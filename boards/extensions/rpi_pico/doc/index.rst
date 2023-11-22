.. _rpi_pico-extensions:

Raspberry Pi Pico and Pico W
############################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:rpi_pico` with some adaptions and improvement on Devicetree
level.

List of extensions
******************

- add the Bridle specific edge connecor binding
  :dtcompatible:`raspberrypi,pico-header-r3`
- add the Bridle specific interface labels:

  - :devicetree:`rpipico_serial: &pico_serial {};`
  - :devicetree:`rpipico_spi: &pico_spi {};`
  - :devicetree:`rpipico_i2c: &pico_i2c {};`

- enable the RP2040 SoC reset controller bindet as
  :dtcompatible:`raspberrypi,pico-reset`
- prepare the RP2040 SoC SPI1 controller bindet as
  :dtcompatible:`raspberrypi,pico-spi` with default
  :dtcompatible:`raspberrypi,pico-pinctrl` and
  :devicetree:`clock-frequency = <DT_FREQ_M(8)>;`
  properties, but explicitly set this to disabled status
