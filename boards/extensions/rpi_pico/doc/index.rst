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

  - :code:`rpipico_serial: &pico_serial {};`
  - :code:`rpipico_spi: &pico_spi {};`
  - :code:`rpipico_i2c: &pico_i2c {};`

- enable the RP2040 SoC reset controller bindet as
  :dtcompatible:`raspberrypi,pico-reset`
