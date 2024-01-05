.. _rpi_pico-extensions:

Raspberry Pi Pico and Pico W
############################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:rpi_pico` with some adaptions and improvement on Kconfig and
Devicetree level.

List of extensions
******************

.. rubric:: Kconfig

- :brd:`deactivate` self powered USB explicitly and set the maximum of
  electrical current consumption to :brd:`500㎃`:

  - :kconfig:option:`CONFIG_USB_SELF_POWERED`
  - :kconfig:option:`CONFIG_USB_MAX_POWER`

  .. list-table::
     :align: left
     :width: 50%
     :widths: 50, 50

     * - .. rubric:: Raspberry Pi Pico
       - .. rubric:: Raspberry Pi Pico W

     * - .. literalinclude:: ../rpi_pico.conf
           :caption: rpi_pico.conf
           :language: cfg
           :encoding: ISO-8859-1
           :start-at: CONFIG_USB_SELF_POWERED
           :end-at: CONFIG_USB_MAX_POWER
       - .. literalinclude:: ../rpi_pico_w.conf
           :caption: rpi_pico_w.conf
           :language: cfg
           :encoding: ISO-8859-1
           :start-at: CONFIG_USB_SELF_POWERED
           :end-at: CONFIG_USB_MAX_POWER

.. rubric:: Devicetree

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
