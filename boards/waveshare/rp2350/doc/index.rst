.. _waveshare_rp2350:

Waveshare RP2350
################

The `RP2350 SoC`_ by Raspberry Pi Ltd. is a small sized and low-cost 32-bit
dual ARM Cortex-M33 and dual 32-bit Hazard3 RISC-V (RV32IMAC+) microcontroller
and predestined for versatile board designs. The Waveshare RP2350 board series
based on this microcontroller offers a wide range with different scaling
factors, in size, features and interfaces for communication, input and output.

Supported Boards
****************

Hardware
========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: RP2350-CAN

      .. _waveshare_rp2350_can:

      .. include:: rp2350-can/hardware.rsti

   .. zephyr-keep-sorted-stop

Positions
=========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: RP2350-CAN

      .. include:: rp2350-can/positions.rsti

   .. zephyr-keep-sorted-stop

Pinouts
=======

The peripherals of the `RP2350 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignments
for the various Waveshare RP2350 boards are defined below separately
in a single tab.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: RP2350-CAN

      .. include:: rp2350-can/pinouts.rsti

   .. zephyr-keep-sorted-stop

Supported Features
******************

Similar to the |zephyr:board:rpi_pico2| the Waveshare RP2350 board configuration
supports the following hardware features:

.. list-table:: Hardware Features Supported by Zephyr
   :class: longtable
   :align: center
   :header-rows: 1

   * - Peripheral
     - Kconfig option
     - Devicetree compatible
     - Zephyr API
   * - PINCTRL
     - :kconfig:option:`CONFIG_PINCTRL`
     - :dtcompatible:`raspberrypi,pico-pinctrl`
     - :external+zephyr:ref:`pinctrl_api`
   * - GPIO
     - :kconfig:option:`CONFIG_GPIO`
     - :dtcompatible:`raspberrypi,pico-gpio`
     - :external+zephyr:ref:`gpio_api`
   * - UART
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`raspberrypi,pico-uart`
     - :external+zephyr:ref:`uart_api`
   * - UDC (USB Device Controller)
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK_NEXT`
     - :dtcompatible:`raspberrypi,pico-usbd`
     - :external+zephyr:ref:`usb_device_next_api`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - :dtcompatible:`raspberrypi,pico-i2c`
     - :external+zephyr:ref:`i2c_api`
   * - SPI
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi`
     - :external+zephyr:ref:`spi_api`
   * - PWM
     - :kconfig:option:`CONFIG_PWM`
     - :dtcompatible:`raspberrypi,pico-pwm`
     - :external+zephyr:ref:`pwm_api`
   * - ADC
     - :kconfig:option:`CONFIG_ADC`
     - :dtcompatible:`raspberrypi,pico-adc`
     - :external+zephyr:ref:`adc_api`
   * - Temperature (Sensor)
     - :kconfig:option:`CONFIG_SENSOR`
     - :dtcompatible:`raspberrypi,pico-temp`
     - :external+zephyr:ref:`sensor`
   * - Timer (Counter)
     - :kconfig:option:`CONFIG_COUNTER`
     - :dtcompatible:`raspberrypi,pico-timer`
     - :external+zephyr:ref:`counter_api`
   * - Watchdog Timer (WDT)
     - :kconfig:option:`CONFIG_WATCHDOG`
     - :dtcompatible:`raspberrypi,pico-watchdog`
     - :external+zephyr:ref:`watchdog_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`raspberrypi,pico-flash-controller`
     - :external+zephyr:ref:`flash_api` and
       :external+zephyr:ref:`flash_map_api`
   * - PIO
     - :kconfig:option:`CONFIG_PIO_RPI_PICO`
     - :dtcompatible:`raspberrypi,pico-pio`
     - N/A
   * - UART (PIO)
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`raspberrypi,pico-uart-pio`
     - :external+zephyr:ref:`uart_api`
   * - SPI (PIO)
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi-pio`
     - :external+zephyr:ref:`spi_api`
   * - WS2812 (PIO)
     - :kconfig:option:`CONFIG_LED_STRIP`
     - :dtcompatible:`worldsemi,ws2812-rpi-pico-pio`
     - N/A
   * - DMA
     - :kconfig:option:`CONFIG_DMA`
     - :dtcompatible:`raspberrypi,pico-dma`
     - :external+zephyr:ref:`dma_api`
   * - HWINFO
     - :kconfig:option:`CONFIG_HWINFO`
     - N/A
     - :external+zephyr:ref:`hwinfo_api`
   * - VREG
     - :kconfig:option:`CONFIG_REGULATOR`
     - :dtcompatible:`raspberrypi,core-supply-regulator` (!)
     - :external+zephyr:ref:`regulator_api`
   * - RESET
     - :kconfig:option:`CONFIG_RESET`
     - :dtcompatible:`raspberrypi,pico-reset`
     - :external+zephyr:ref:`reset_api`
   * - CLOCK
     - :kconfig:option:`CONFIG_CLOCK_CONTROL`
     - | :dtcompatible:`raspberrypi,pico-clock-controller`
       | :dtcompatible:`raspberrypi,pico-clock`
     - :external+zephyr:ref:`clock_control_api`
   * - NVIC
     - N/A
     - :dtcompatible:`arm,v8m-nvic`
     - Nested Vector :external+zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv8m-systick`
     -

(!) POWMAN with VREG on RP2350 not yet supported by Zephyr.

    See section **Peripherals RP2350** in upstream issue:
    https://github.com/zephyrproject-rtos/zephyr/issues/53810

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

.. zephyr-keep-sorted-start re(^\* :bridle_file:`\w)

* :bridle_file:`boards/waveshare/rp2350/waveshare_rp2350_can_rp2350a_m33_defconfig`

.. zephyr-keep-sorted-stop

Board Configurations
====================

The Waveshare RP2350 boards can be configured for the following different
use cases.

.. tabs::

   .. group-tab:: RP2350-CAN

      .. rubric:: :command:`west build -b waveshare_rp2350_can/rp2350a/m33`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2350_can/rp2350a/m33 -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.


Connections and IOs
===================

The `Waveshare wiki`_ has detailed information about board connections.
Download the different schematics or datasheets as linked above per board
for more details. The pinout diagrams can also be found there.

System Clock
============

The `RP2350A <RP2350 SoC_>`_ MCU is configured to use the 12㎒ external crystal
with the on-chip PLL generating the 150㎒ system clock. The internal AHB and
APB units are set up in the same way as the upstream `Raspberry Pi Pico C/C++
SDK`_ libraries.

GPIO (PWM) Ports
================

The `RP2350A <RP2350 SoC_>`_ MCU has 1 GPIO cell which covers all I/O pads and
8 PWM function unit each with 2 channels beside a dedicated Timer unit. On
the |RP2350-CAN|, PWM4 channel B is available on the on-board user LED. But
the PWM operation is not enable by default. Only if
:kconfig:option:`CONFIG_PWM_RPI_PICO` is enabled then the first user LED is
driven by PWM4CHB instead of by GPIO. All channels of PWM0 until PWM7 are
available on the |Raspberry Pi Pico| header.

ADC/TS Ports
============

The `RP2350A <RP2350 SoC_>`_ MCU has 1 ADC with 4 channels and an additional
fifth channel for the on-chip temperature sensor (TS). The ADC channels 0-2
are available on the |Raspberry Pi Pico| header. On the |RP2350-CAN|, ADC
channel 3 will be used for internal on-board voltage monitoring.

The external voltage reference ADC_VREF can be used optional for the ADC
and is only available on the |Raspberry Pi Pico| header.

SPI Port
========

The `RP2350A <RP2350 SoC_>`_ MCU has 2 SPIs. To the edge connectors SPI0 is
connect to external devices over GP19 (MOSI), GP16 (MISO), GP18 (SCK), and
GP17 (CSn) on the |Raspberry Pi Pico| header.

I2C Port
========

The `RP2350A <RP2350 SoC_>`_ MCU has 2 I2Cs. To the edge connectors I2C0 and
I2C1 is connect to external devices over GP4 (I2C0_SDA), GP5 (I2C0_SCL),
GP14 (I2C1_SDA), and GP15 (I2C1_SCL) on the |Raspberry Pi Pico| header.

Serial Port
===========

The `RP2350A <RP2350 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART0)
is connected to external devices over GP0 (TX) and GP1 (RX) on the
|Raspberry Pi Pico| header and is the Zephyr console.

USB Device Port
===============

The `RP2350A <RP2350 SoC_>`_ MCU has a (native) USB device port that can be used
to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb` sample applications for more,
such as the :external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets
up a virtual serial port that echos characters back to the host PC.
As an alternative to the default Zephyr console on serial port the
Bridle :ref:`snippet-usb-console` can be used to enable
:external+zephyr:ref:`usb_device_cdc_acm` and switch the console to USB

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: RP2350-CAN

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2350_can_VID|, idProduct=\ |waveshare_rp2350_can_PID_CON|, bcdDevice=\ |waveshare_rp2350_can_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2350_can_PStr_CON|
               Manufacturer: |waveshare_rp2350_can_VStr|
               SerialNumber: B46993A480CF94B1

   .. zephyr-keep-sorted-stop

To integrate specific USB device functions that do not follow
a USB standard class, the following alternate identifier numbers
are available for the various Waveshare RP2040 and RP2350 boards
according to the `Raspberry Pi USB product ID list`_:

.. container:: twocol

   .. container:: leftside

      .. rubric:: RP2040

      :|rpi_waveshare_rp2040_zero_URB_PID|: |RP2040-Zero|
      :|rpi_waveshare_rp2040_plus_URB_PID|: |RP2040-Plus|
      :|rpi_waveshare_rp2040_lcd_0_96_URB_PID|: |RP2040-LCD-0.96|
      :|rpi_waveshare_rp2040_lcd_1_28_URB_PID|: RP2040-LCD-1.28
      :|rpi_waveshare_rp2040_one_URB_PID|: |RP2040-One|
      :|rpi_waveshare_pwr_mgmt_hat_b_one_URB_PID|: Power Management HAT (B)
      :|rpi_waveshare_rp2040_eth_URB_PID|: |RP2040-ETH|
      :|rpi_waveshare_rp2040_geek_URB_PID|: |RP2040-Geek|
      :|rpi_waveshare_rp2040_touch_lcd_1_28_URB_PID|: RP2040-Touch-LCD-1.28
      :|rpi_waveshare_rp2040_pizero_URB_PID|: RP2040-PiZero
      :|rpi_waveshare_rp2040_tiny_URB_PID|: |RP2040-Tiny|
      :|rpi_waveshare_rp2040_matrix_URB_PID|: |RP2040-Matrix|
      :|rpi_waveshare_rp2040_ble_URB_PID|: RP2040-BLE
      :|rpi_waveshare_pico_cam_a_URB_PID|: PICO-Cam-A

   .. container:: rightside

      .. rubric:: RP2350

      :|rpi_waveshare_rp2350_zero_URB_PID|: RP2350-Zero
      :|rpi_waveshare_rp2350_plus_URB_PID|: RP2350-Plus
      :|rpi_waveshare_rp2350_tiny_URB_PID|: RP2350-Tiny
      :|rpi_waveshare_rp2350_lcd_1_28_URB_PID|: RP2350-LCD-1.28
      :|rpi_waveshare_rp2350_touch_lcd_1_28_URB_PID|: RP2350-Touch-LCD-1.28
      :|rpi_waveshare_rp2350_one_URB_PID|: RP2350-One
      :|rpi_waveshare_rp2350_geek_URB_PID|: RP2350-Geek
      :|rpi_waveshare_rp2350_lcd_0_96_URB_PID|: RP2350-LCD-0.96

|nbsp|

Programmable I/O (PIO)
**********************

The `RP2350 SoC`_ comes with three PIO periherals. These are three simple
co-processors that are designed for I/O operations. The PIOs run a custom
instruction set, generated from a custom assembly language. PIO programs
are assembled using :program:`pioasm`, a tool provided by Raspberry Pi.
Further information can be found in the `Raspberry Pi Pico C/C++ SDK`_
document, section with title :emphasis:`"Using PIOASM, the PIO Assembler"`.

Zephyr does not (currently) assemble PIO programs. Rather, they should be
manually assembled and embedded in source code. An example of how this is done
can be found at :zephyr_file:`drivers/serial/uart_rpi_pico_pio.c` or
:zephyr_file:`drivers/spi/spi_rpi_pico_pio.c`.

Programming and Debugging
*************************

Flashing
========

Using UF2
---------

If you don't have an SWD adapter, you can flash the Waveshare RP2350 boards
with a UF2 file. By default, building an app for this board will generate a
:file:`build/zephyr/zephyr.uf2` file. If the board is powered on with the
:kbd:`BOOTSEL` button pressed, it will appear on the host as a mass
storage device:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |rpi_VID|, idProduct=\ |rpi_rp2350_PID|, bcdDevice=\ |rpi_rp2350_BCD|
         USB device strings: Mfr=1, Product=2, SerialNumber=0
         Product: |rpi_rp2350_PStr|
         Manufacturer: |rpi_VStr|
         SerialNumber: A0231978E046

The UF2 file should be drag-and-dropped or copied on command line to the
device, which will then flash the Waveshare RP2350 board.

Each `RP2350 SoC`_ ships the `UF2 compatible <UF2 bootloader_>`_ bootloader
pico-bootrom-rp2350_, a native support in silicon. The full source for the
RP2350 bootrom at pico-bootrom-rp2350_ includes versions A2, A3 and A4 of
the bootrom, which correspond to the same silicon revisions, respectively.

Note that every time you build a program for the RP2350, the Pico SDK selects
and creates an appropriate image definition and/or partition table block with
attributes and precedes it in the firmware. Further information can be found
in the `RP2350 Datasheet`_, sections with title :emphasis:`"Bootrom"` and
:emphasis:`"Processor Controlled Boot Sequence"`.

Using SEGGER JLink
------------------

You can flash the Waveshare RP2350 boards with a SEGGER JLink debug probe as
described in
:external+zephyr:ref:`Building, Flashing and Debugging <west-flashing>`.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :build-dir: waveshare_rp2350
      :board: waveshare_rp2350_can/rp2350a/m33
      :flash-args: -r jlink
      :west-args: -p
      :goals: flash

Using OpenOCD
-------------

To use `PicoProbe`_ or `Raspberry Pi Debug Probe`_, you must configure
:program:`udev`. Create a file in :file:`/etc/udev.rules.d` with any name,
and write the line below:

   .. container:: highlight highlight-none notranslate literal-block

      .. parsed-literal::

         ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="0004", MODE="660", GROUP="plugdev", TAG+="uaccess"
         ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="000c", MODE="660", GROUP="plugdev", TAG+="uaccess"

This example is valid for the case that the user joins to :code:`plugdev`
groups.

The |RP2350-CAN| has an SWD interface that can be used to program and debug
the on board RP2350. This interface can be utilized by OpenOCD. To use it
with the RP2350, OpenOCD version 0.12.0 or later is needed. If you are using
a Debian based system (including RaspberryPi OS, Ubuntu, and more), using the
`pico_setup.sh`_ script is a convenient way to set up the forked version of
OpenOCD. Depending on the interface used (such as JLink), you might need to
checkout to a branch that supports this interface, before proceeding. Build
and install OpenOCD as described in the README.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :build-dir: waveshare_rp2350
      :board: waveshare_rp2350_can/rp2350a/m33
      :gen-args: \
                 -DOPENOCD=/usr/local/bin/openocd \
                 -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
                 -DWAVESHARE_RP2350_DEBUG_ADAPTER=picoprobe
      :west-args: -p
      :flash-args: -r openocd
      :goals: flash

Set the environment variables :strong:`OPENOCD` to
:file:`/usr/local/bin/openocd` and :strong:`OPENOCD_DEFAULT_PATH` to
:file:`/usr/local/share/openocd/scripts`. This should work with the OpenOCD
that was installed with the default configuration. This configuration also
works with an environment that is set up by the `pico_setup.sh`_ script.

:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` specifies what debug adapter is
used for debugging. If :strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` was not
assigned, :dfn:`cmsis-dap` is used by default. The other supported adapters
are :dfn:`picoprobe`, :dfn:`raspberrypi-swd`, :dfn:`jlink` and
:dfn:`blackmagicprobe`. How to connect :dfn:`picoprobe` and
:dfn:`raspberrypi-swd` is described in `Getting Started Guide with Raspberry
Pi Pico`_. Any other SWD debug adapter maybe also work with this configuration.
The value of :strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` is cached, so it can
be omitted from :program:`west flash` and :program:`west debug` if it was
previously set while running :program:`west build`.
:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` is used in an argument to OpenOCD as
:code:`"source [find interface/${WAVESHARE_RP2350_DEBUG_ADAPTER}.cfg]"`. Thus,
:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` needs to be assigned the file name of
the debug adapter.

You can also flash the board with the following command that directly calls
OpenOCD (assuming a SEGGER JLink adapter is used):

.. code-block:: console

   $ openocd -f interface/jlink.cfg    \
             -c 'transport select swd' \
             -f target/rp2350.cfg      \
             -c "adapter speed 2000"   \
             -c 'targets rp2350.core0' \
             -c 'program path/to/zephyr.elf verify reset exit'

Debugging
=========

The SWD interface can also be used to debug the board. To achieve this, you can
either use SEGGER JLink or OpenOCD.

Using SEGGER JLink
------------------

Use a SEGGER JLink debug probe and follow the instruction in
:external+zephyr:ref:`Building, Flashing and Debugging <west-debugging>`.

Using OpenOCD
-------------

Install OpenOCD as described for flashing the board.

Here is an example for debugging the
:external+zephyr:zephyr:code-sample:`blinky` application.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :build-dir: waveshare_rp2350
      :board: waveshare_rp2350_can/rp2350a/m33
      :maybe-skip-config:
      :gen-args: \
                 -DOPENOCD=/usr/local/bin/openocd \
                 -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
                 -DWAVESHARE_RP2350_DEBUG_ADAPTER=raspberrypi-swd
      :west-args: -p
      :flash-args: -r openocd
      :goals: debug
      :host-os: unix

As with flashing, you can specify the debug adapter by specifying
:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` at :program:`west build` time.
No needs to specify it at :program:`west debug` time.

You can also debug with OpenOCD and gdb launching from command-line.
Run the following command:

.. code-block:: console

   $ openocd -f interface/jlink.cfg    \
             -c 'transport select swd' \
             -f target/rp2350.cfg      \
             -c "adapter speed 2000"   \
             -c 'targets rp2350.core0'

On another terminal, run:

.. code-block:: console

   $ gdb-multiarch

Inside gdb, run:

.. code-block:: console

   (gdb) tar ext :3333
   (gdb) file path/to/zephyr.elf

You can then start debugging the board.

More Samples
************

LED Blinky and Fade
===================

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: RP2350-CAN

      .. rubric:: Green User LED Blinky by GPIO

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

         .. rubric:: On ARM Cortex-M33

         .. zephyr-app-commands::
            :app: zephyr/samples/basic/blinky
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/m33
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

         .. rubric:: On Hazard3 RISC-V (RV32IMAC+)

         .. zephyr-app-commands::
            :app: zephyr/samples/basic/blinky
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/hazard3
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

      .. rubric:: Green User LED Blinky by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`pwm-blinky`.

         .. rubric:: On ARM Cortex-M33

         .. zephyr-app-commands::
            :app: zephyr/samples/basic/blinky_pwm
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/m33
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

         .. rubric:: On Hazard3 RISC-V (RV32IMAC+)

         .. zephyr-app-commands::
            :app: zephyr/samples/basic/blinky_pwm
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/hazard3
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

      .. rubric:: Green User LED Fade by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`fade-led`.

         .. rubric:: On ARM Cortex-M33

         .. zephyr-app-commands::
            :app: zephyr/samples/basic/fade_led
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/m33
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

         .. rubric:: On Hazard3 RISC-V (RV32IMAC+)

         .. zephyr-app-commands::
            :app: zephyr/samples/basic/fade_led
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/hazard3
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

   .. zephyr-keep-sorted-stop

Hello Shell with USB-CDC/ACM Console
====================================

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: RP2350-CAN

      .. rubric:: Hello Shell

      See also Bridle sample: :ref:`helloshell-sample`.

         .. rubric:: On ARM Cortex-M33

         .. zephyr-app-commands::
            :app: bridle/samples/helloshell
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/m33
            :snippets: "usb-console"
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

         .. rubric:: On Hazard3 RISC-V (RV32IMAC+)

         .. zephyr-app-commands::
            :app: bridle/samples/helloshell
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/hazard3
            :snippets: "usb-console"
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

      .. include:: rp2350-can/helloshell.rsti

   .. zephyr-keep-sorted-stop

CANnectivity
============

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: RP2350-CAN

      See also how to :external+cannectivity:doc:`building` the
      CANnectivity USB to CAN application firmware. The USB
      :external+zephyr:ref:`Device Firmware Upgrade <dfu>` (DFU)
      via the `MCUboot`_ bootloader is not and will never be
      supported. The UF2 bootloader is perfect for firmware updates.

         .. rubric:: On ARM Cortex-M33

         .. zephyr-app-commands::
            :app: cannectivity/app
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/m33
            :conf: "prj_usbd_next_release.conf"
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

         .. rubric:: On Hazard3 RISC-V (RV32IMAC+)

         .. zephyr-app-commands::
            :app: cannectivity/app
            :build-dir: waveshare_rp2350
            :board: waveshare_rp2350_can/rp2350a/hazard3
            :conf: "prj_usbd_next_release.conf"
            :west-args: -p
            :flash-args: -r uf2
            :goals: flash
            :compact:

      .. include:: rp2350-can/cannectivity.rsti

   .. zephyr-keep-sorted-stop

References
**********

.. target-notes::
