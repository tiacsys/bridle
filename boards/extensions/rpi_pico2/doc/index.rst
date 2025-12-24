.. _rpi_pico2-extensions:

Raspberry Pi Pico 2 and Pico 2W
###############################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
|zephyr:board:rpi_pico2| with some adaptions and improvement on Kconfig and
Devicetree level.

List of extensions
******************

.. rubric:: Kconfig

- :brd:`deactivate` self powered USB explicitly and set the maximum of
  electrical current consumption to :brd:`500㎃`:

  - |CONFIG_CDC_ACM_SERIAL_SELF_POWERED|
  - |CONFIG_CDC_ACM_SERIAL_MAX_POWER|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico 2 and Pico 2W

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 1-2,5-6
            :start-at: config CDC_ACM_SERIAL_SELF_POWERED
            :end-before: Logger cannot use itself to log

- :brd:`change` log level only in case of use the native USB device port
  :dtcompatible:`raspberrypi,pico-usbd` with CDC-ACM UART
  :dtcompatible:`zephyr,cdc-acm-uart` as Zephyr console:

  - |CONFIG_USBD_CDC_ACM_LOG_LEVEL_CHOICE| :=
    |CONFIG_USBD_CDC_ACM_LOG_LEVEL_OFF|
  - |CONFIG_USBD_LOG_LEVEL_CHOICE| :=
    |CONFIG_USBD_LOG_LEVEL_ERR|
  - |CONFIG_UDC_DRIVER_LOG_LEVEL_CHOICE| :=
    |CONFIG_UDC_DRIVER_LOG_LEVEL_ERR|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico 2 and Pico 2W

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :lines: -14,23-
            :emphasize-lines: 3-4,16-17,22-23,28-29
            :start-at: Workaround for not being able to have commas in macro arguments
            :end-at: endif # zephyr,cdc-acm-uart

.. rubric:: Devicetree

- set default entries for ``model`` and ``compatible`` of the boards:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico 2

     * - .. literalinclude:: ../rpi_pico2_m33.overlay
            :caption: rpi_pico2_rp2350a_m33.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-before: chosen {
            :append: };

     * - .. literalinclude:: ../rpi_pico2_hazard3.overlay
            :caption: rpi_pico2_hazard3.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-before: chosen {
            :append: };

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico 2W

     * - .. literalinclude:: ../rpi_pico2_m33_w.overlay
            :caption: rpi_pico2_rp2350a_m33_w.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-before: chosen {
            :append: };

- add the Bridle specific edge connecor binding
  :dtcompatible:`raspberrypi,pico-header-r3`

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico 2 and Pico 2W

     * - .. literalinclude:: ../rpipico_r3_connector.dtsi
            :caption: rpipico_r3_connector.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: rpipico_header: connector {
            :end-at: };
            :append: };

- add the Bridle specific interface labels:

  - :dts:`rpipico_serial: &pico_serial {};`
  - :dts:`rpipico_spi: &pico_spi {};`
  - :dts:`rpipico_spi0: &pico_spi0 {};`
  - :dts:`rpipico_spi1: &pico_spi1 {};`
  - :dts:`rpipico_i2c: &pico_i2c {};`
  - :dts:`rpipico_i2c0: &pico_i2c0 {};`
  - :dts:`rpipico_i2c1: &pico_i2c1 {};`

- enable the RP2350 SoC reset controller bindet as
  :dtcompatible:`raspberrypi,pico-reset`

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico 2 and Pico 2W

     * - .. literalinclude:: ../rpipico_r3.dtsi
            :caption: rpipico_r3.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :start-at: &reset {
            :end-at: };

- prepare the RP2350 SoC SPI1 controller bindet as
  :dtcompatible:`raspberrypi,pico-spi` with default
  :dtcompatible:`raspberrypi,pico-pinctrl` and
  :dts:`clock-frequency = <DT_FREQ_M(8)>;`
  properties, but explicitly set this to disabled status

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico 2 and Pico 2W

     * - .. literalinclude:: ../rpipico_r3-spi1.dtsi
            :caption: rpipico_r3-spi1.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :start-at: &spi1 {
            :end-at: };

         .. literalinclude:: ../rpipico_r3-pinctrl.dtsi
            :caption: rpipico_r3-pinctrl.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: &pinctrl {
            :start-at: spi1_default: spi1_default {
            :end-before: }; // pinctrl
            :append: };
