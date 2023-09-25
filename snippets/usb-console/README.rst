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

   * - :code:`arduino_zero`
     - :code:`0x2341`
     - :code:`0x804D`
     - |Arduino LLC|_
     - |Arduino Zero (CDC ACM)|
     - `Arduino USB product ID list with SAMD21 CPU`_
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

.. _Arduino LLC: https://devicehunt.com/view/type/usb/vendor/2341
.. |Arduino LLC| replace:: :strong:`Arduino LLC`

.. |Arduino Zero (CDC ACM)| replace::
   :ref:`Arduino Zero (CDC ACM) <arduino_zero>`

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
