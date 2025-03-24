.. _rpi_pico-extensions:

Raspberry Pi Pico and Pico W
############################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
|zephyr:board:rpi_pico| with some adaptions and improvement on Kconfig and
Devicetree level.

List of extensions
******************

.. rubric:: Kconfig

- :brd:`deactivate` self powered USB explicitly and set the maximum of
  electrical current consumption to :brd:`500㎃`:

  - |CONFIG_USB_SELF_POWERED|
  - |CONFIG_USB_MAX_POWER|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico and Pico W

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 1-2,5-6
            :start-at: config USB_SELF_POWERED
            :end-before: Workaround for not being able to have commas in macro arguments

- :brd:`change` log level and startup delay only in case of use the
  native USB device port :dtcompatible:`raspberrypi,pico-usbd` with
  CDC-ACM UART :dtcompatible:`zephyr,cdc-acm-uart` as Zephyr console:

  - |CONFIG_USB_CDC_ACM_LOG_LEVEL_CHOICE| :=
    |CONFIG_USB_CDC_ACM_LOG_LEVEL_OFF|
  - |CONFIG_USB_DEVICE_LOG_LEVEL_CHOICE| :=
    |CONFIG_USB_DEVICE_LOG_LEVEL_ERR|
  - |CONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS|
  - |CONFIG_BOOT_DELAY|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico and Pico W

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 3-4,16-17,22-23,28-29,33-34
            :start-at: Workaround for not being able to have commas in macro arguments
            :end-at: endif # zephyr,cdc-acm-uart

.. rubric:: Devicetree

- set default entries for ``model`` and ``compatible`` of the boards:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico

     * - .. literalinclude:: ../rpi_pico.overlay
            :caption: rpi_pico.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-at: compatible
            :append: };

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico W

     * - .. literalinclude:: ../rpi_pico_w.overlay
            :caption: rpi_pico_w.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-at: compatible
            :append: };

- add the Bridle specific edge connecor binding
  :dtcompatible:`raspberrypi,pico-header-r3`

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico and Pico W

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

- enable the RP2040 SoC reset controller bindet as
  :dtcompatible:`raspberrypi,pico-reset`

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico and Pico W

     * - .. literalinclude:: ../rpipico_r3.dtsi
            :caption: rpipico_r3.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :start-at: &reset {
            :end-at: };

- prepare the RP2040 SoC SPI1 controller bindet as
  :dtcompatible:`raspberrypi,pico-spi` with default
  :dtcompatible:`raspberrypi,pico-pinctrl` and
  :dts:`clock-frequency = <DT_FREQ_M(8)>;`
  properties, but explicitly set this to disabled status

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Raspberry Pi Pico and Pico W

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
