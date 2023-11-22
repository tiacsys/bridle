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

   * - :code:`seeed_xiao_samd21`
     - :code:`0x2886`
     - :code:`0x802F`
     - |Seeed Studio|_
     - |XIAO SAMD21 (CDC ACM)|, Seeeduino XIAO
     - `Seeeduino USB product ID list with SAMD21 CPU`_
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

.. _NXP Semiconductors: https://devicehunt.com/view/type/usb/vendor/1fc9
.. |NXP Semiconductors| replace:: :strong:`NXP Semiconductors`

.. |MIMXRT1010-EVK (CDC ACM)| replace::
   :ref:`MIMXRT1010-EVK (CDC ACM) <zephyr:mimxrt1010_evk>`

.. |MIMXRT1060-EVK (CDC ACM)| replace::
   :ref:`MIMXRT1060-EVK (CDC ACM) <zephyr:mimxrt1060_evk>`

.. _Arduino LLC: https://devicehunt.com/view/type/usb/vendor/2341
.. |Arduino LLC| replace:: :strong:`Arduino LLC`

.. |Arduino Zero (CDC ACM)| replace::
   :ref:`Arduino Zero (CDC ACM) <arduino_zero>`

.. _Seeed LLC: https://devicehunt.com/view/type/usb/vendor/2886
.. |Seeed LLC| replace:: :strong:`Seeed LLC`

.. |Seeeduino Lotus Cortex-M0+ (CDC ACM)| replace::
   :ref:`Seeeduino Lotus Cortex-M0+ (CDC ACM) <seeeduino_lotus>`

.. |Seeeduino Cortex-M0+ (CDC ACM)| replace::
   :ref:`Seeeduino Cortex-M0+ (CDC ACM) <seeeduino_cm0>`

.. _Seeed Studio: https://devicehunt.com/view/type/usb/vendor/2886
.. |Seeed Studio| replace:: :strong:`Seeed Studio`

.. |XIAO SAMD21 (CDC ACM)| replace::
   :ref:`XIAO SAMD21 (CDC ACM) <seeed_xiao_samd21>`

.. _Raspberry Pi: https://devicehunt.com/view/type/usb/vendor/2e8a
.. |Raspberry Pi| replace:: :strong:`Raspberry Pi`

.. |RPi Pico (CDC ACM)| replace::
   :ref:`RPi Pico (CDC ACM) <rpi_pico>`

.. |RPi Pico W (CDC ACM)| replace::
   :ref:`RPi Pico W (CDC ACM) <rpi_pico>`

.. _Waveshare (Raspberry Pi): https://devicehunt.com/view/type/usb/vendor/2e8a
.. |Waveshare (Raspberry Pi)| replace:: :strong:`Waveshare (Raspberry Pi)`

.. |RP2040-One (CDC ACM)| replace::
   :ref:`RP2040-One (CDC ACM) <waveshare_rp2040_one>`

.. |RP2040-Zero (CDC ACM)| replace::
   :ref:`RP2040-Zero (CDC ACM) <waveshare_rp2040_zero>`

.. |RP2040-Matrix (CDC ACM)| replace::
   :ref:`RP2040-Matrix (CDC ACM) <waveshare_rp2040_matrix>`

.. |RP2040-Tiny (CDC ACM)| replace::
   :ref:`RP2040-Tiny (CDC ACM) <waveshare_rp2040_tiny>`

.. |RP2040-ETH (CDC ACM)| replace::
   :ref:`RP2040-ETH (CDC ACM) <waveshare_rp2040_eth>`

.. |RP2040-LCD-0.96 (CDC ACM)| replace::
   :ref:`RP2040-LCD-0.96 (CDC ACM) <waveshare_rp2040_lcd_0_96>`

.. |RP2040-Plus (CDC ACM)| replace::
   :ref:`RP2040-Plus (CDC ACM) <waveshare_rp2040_plus>`

.. _Arduino USB product ID list with SAM3X CPU:
   https://github.com/arduino/ArduinoCore-sam/blob/master/boards.txt

.. _Arduino USB product ID list with SAMD21 CPU:
   https://github.com/arduino/ArduinoCore-samd/blob/master/boards.txt

.. _Seeeduino USB product ID list with SAMD21 CPU:
   https://github.com/Seeed-Studio/ArduinoCore-samd/blob/master/boards.txt

.. _Raspberry Pi USB product ID list:
   https://github.com/raspberrypi/usb-pid

.. |CDC ACM| replace:: :ref:`zephyr:usb_device_cdc_acm`

.. |Zephyr USB Vendor and Product identifiers| replace::
   Zephyr :ref:`zephyr:usb_device_vid_pid`

.. |zephyr,console| replace::
   :ref:`zephyr,console <zephyr:devicetree-zephyr-chosen-nodes>`
.. |zephyr,shell-uart| replace::
   :ref:`zephyr,shell-uart <zephyr:devicetree-zephyr-chosen-nodes>`
