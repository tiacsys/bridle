.. _snippet-usb-console:

USB Console Snippet (usb-console)
#################################

.. code-block:: console

   west build -S usb-console [...]

Overview
********

This snippet redirects serial console output to a |CDC ACM| UART. The USB
device which should be used is configured using :ref:`zephyr:devicetree`.

.. tsn-include:: connectivity/usb/device/usb_device.rst
   :docset: zephyr
   :start-after: Below is a description of the different use cases and some pitfalls.
   :end-before: CDC ACM UART node is supposed to be child of a USB device controller node.

.. tsn-include:: connectivity/usb/device/usb_device.rst
   :docset: zephyr
   :start-after: .. _usb_device_vid_pid:
   :end-before: Each USB :ref:`sample<usb-samples>` has its own unique Product ID.

Board specific identifiers
==========================

In the basic configuration, the standard Zephyr USB manufacturer and product
identification is used. However, manufacturer defined values can also be
specified as required.

.. list-table:: USB manufacturer and product identification
   :class: longtable
   :align: center
   :widths: 10, 5, 5, 15, 15, 40, 10
   :header-rows: 1
   :stub-columns: 3

   * - Board
     - VID
     - PID
     - Manufacturer
     - Product
     - Specifications and requirements
     - Chosen

   * - :code:`nucleo_f767zi`
     - :code:`0x0483`
     - :code:`0x5740`
     - |STMicroelectronics|_
     - |STM32F767ZI-NUCLEO (CDC ACM)|
     - `STMicroelectronics USB product ID from their Virtual COM Port`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`mimxrt1010_evk`
     - :code:`0x1FC9`
     - :code:`0x1011`
     - |NXP Semiconductors|_
     - |MIMXRT1010-EVK (CDC ACM)|
     - derived VID from part number MIMXRT1011DAE5A
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - | :code:`mimxrt1060_evk`
       | :code:`mimxrt1060_evkb`
       | :code:`mimxrt1060_evk_hyperflash`
     - :code:`0x1FC9`
     - :code:`0x1062`
     - |NXP Semiconductors|_
     - |MIMXRT1060-EVK (CDC ACM)|
     - derived VID from part number MIMXRT1062DVL6A
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`arduino_zero`
     - :code:`0x2341`
     - :code:`0x804D`
     - |Arduino LLC|_
     - |Arduino Zero (CDC ACM)|
     - `Arduino USB product ID list with SAMD21 CPU`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`seeeduino_lotus`
     - :code:`0x2886`
     - :code:`0x8026`
     - |Seeed LLC|_
     - |Seeeduino Lotus Cortex-M0+ (CDC ACM)|
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`seeeduino_cm0`
     - :code:`0x2886`
     - :code:`0x8027`
     - |Seeed LLC|_
     - |Seeeduino Cortex-M0+ (CDC ACM)|
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`seeeduino_xiao`
     - :code:`0x2886`
     - :code:`0x802F`
     - |Seeed LLC|_
     - :ref:`Seeed XIAO M0 (CDC ACM) <zephyr:seeeduino_xiao>`, Seeeduino XIAO
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`xiao_samd21`
     - :code:`0x2886`
     - :code:`0x802F`
     - |Seeed Studio|_
     - |XIAO SAMD21 (CDC ACM)|, Seeeduino XIAO
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`cytron_maker_nano_rp2040`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Cytron (Raspberry Pi)|_
     - |Maker Nano RP2040 (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`cytron_maker_pi_rp2040`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Cytron (Raspberry Pi)|_
     - |Maker Pi RP2040 (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`rpi_pico`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Raspberry Pi|_
     - |RPi Pico (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`rpi_pico_w`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Raspberry Pi|_
     - |RPi Pico W (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_one`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-One (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_zero`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-Zero (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_matrix`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-Matrix (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_tiny`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-Tiny (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_eth`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-ETH (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_lcd_0_96`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-LCD-0.96 (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_plus`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-Plus (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * - :code:`waveshare_rp2040_geek`
     - :code:`0x2E8A`
     - :code:`0x000A`
     - |Waveshare (Raspberry Pi)|_
     - |RP2040-Geek (CDC ACM)|, Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr,console|
       | |zephyr,shell-uart|

   * -
     - :code:`0x2FE3`
     - :code:`0x0004`
     - Zephyr Project
     - Console over USB CDC ACM
     - |Zephyr USB Vendor and Product identifiers|
     - | |zephyr,console|

How to add support of a new board
*********************************

* add board configuration and devicetree overlay to this snippet;
* which overwrites following options:

  - :kconfig:option:`CONFIG_USB_DEVICE_VID`
  - :kconfig:option:`CONFIG_USB_DEVICE_PID`
  - :kconfig:option:`CONFIG_USB_DEVICE_MANUFACTURER`
  - :kconfig:option:`CONFIG_USB_DEVICE_PRODUCT`
  - :kconfig:option:`CONFIG_USB_DEVICE_PRODUCT`

Requirements
************

Hardware support for:

- :kconfig:option:`CONFIG_USB_DEVICE_STACK`
- :kconfig:option:`CONFIG_SERIAL`
- :kconfig:option:`CONFIG_CONSOLE`
- :kconfig:option:`CONFIG_UART_CONSOLE`
- :kconfig:option:`CONFIG_UART_LINE_CTRL`

A devicetree node with node label ``zephyr_udc0`` that points to an enabled USB
device node with driver support. This should look roughly like this in
:ref:`your devicetree <zephyr:get-devicetree-outputs>`:

.. code-block:: DTS

   zephyr_udc0: usbd@deadbeef {
   	compatible = "vnd,usb-device";
        /* ... */
   };

References
**********

.. target-notes::
