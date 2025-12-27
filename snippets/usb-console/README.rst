.. _snippet-usb-console:

USB Console Snippet (usb-console)
#################################

.. code-block:: console

   west build -S usb-console [...]

Overview
********

This snippet redirects serial console output to a
:external+zephyr:ref:`usb_device_cdc_acm` UART. The USB device which
should be used is configured using :external+zephyr:ref:`devicetree`.

.. tsn-include:: connectivity/usb/device/usb_device.rst
   :docset: zephyr
   :start-after: Below is a description of the different use cases and some pitfalls.
   :end-before: CDC ACM UART node is supposed to be child of a USB device controller node.

.. tsn-include:: connectivity/usb/device/usb_device.rst
   :docset: zephyr
   :start-after: .. _usb_device_vid_pid:
   :end-before: The following Product IDs are currently used:

In the Zephyr documentation you will found a detailed and up to date list
of :external+zephyr:ref:`usb_device_vid_pid` as they would be used for each
single USB :external+zephyr:zephyr:code-sample-category:`sample <usb>`
without manipulation by this snippet. This snippet should only be applied to
applications similar to the
:external+zephyr:zephyr:code-sample:`usb-cdc-acm-console` example, no other!

Board specific identifiers
==========================

In the basic configuration, the standard Zephyr USB manufacturer and product
identification is used. However, manufacturer defined values can also be
specified as required.

.. list-table:: USB manufacturer and product identification
   :class: longtable
   :align: center
   :widths: 3, 3, 12, 15, 23, 34, 10
   :header-rows: 1
   :stub-columns: 2

   * - VID
     - PID
     - Board
     - Manufacturer
     - Product
     - Specifications and requirements
     - Chosen

   * - |magpie_f777ni_URB_VID|
     - |magpie_f777ni_URB_PID_CON|
     - :code:`magpie_f777ni`
     - |STMicroelectronics|_
     - |TiaC Magpie F777NI (CDC ACM)|
     - `STMicroelectronics USB product ID from their Virtual COM Port`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |nucleo_f767zi_URB_VID|
     - |nucleo_f767zi_URB_PID_CON|
     - :code:`nucleo_f767zi`
     - |STMicroelectronics|_
     - |STM32F767ZI-NUCLEO (CDC ACM)|
     - `STMicroelectronics USB product ID from their Virtual COM Port`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |vccgnd_bluepill_URB_VID|
     - |vccgnd_bluepill_URB_PID_CON|
     - | :code:`vccgnd_bluepill_stm32f103cb`
       | :code:`vccgnd_bluepill_stm32f103c8`
       | :code:`vccgnd_bluepill_stm32f072cb`
       | :code:`vccgnd_bluepill_stm32f072c8`
     - |STMicroelectronics|_
     - |VccGND BluePill (CDC ACM)|
     - `STMicroelectronics USB product ID from their Virtual COM Port`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |weact_bluepillplus_URB_VID|
     - |weact_bluepillplus_URB_PID_CON|
     - | :code:`weact_bluepillplus_stm32f103cb`
       | :code:`weact_bluepillplus_stm32f103c8`
       | :code:`weact_bluepillplus_ch32v203c8`
       | :code:`weact_bluepillplus_ch32v203c6`
     - |STMicroelectronics|_
     - |WeAct BluePill+ (CDC ACM)|
     - `STMicroelectronics USB product ID from their Virtual COM Port`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |mimxrt1010_evk_URB_VID|
     - |mimxrt1010_evk_URB_PID_CON|
     - :code:`mimxrt1010_evk`
     - |NXP Semiconductors|_
     - |MIMXRT1010-EVK (CDC ACM)|
     - derived VID from part number MIMXRT1011DAE5A
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |mimxrt1060_evk_URB_VID|
     - |mimxrt1060_evk_URB_PID_CON|
     - | :code:`mimxrt1060_evk@C/mimxrt1062/qspi`
       | :code:`mimxrt1060_evk@B/mimxrt1062/qspi`
       | :code:`mimxrt1060_evk@A/mimxrt1062/qspi`
       | :code:`mimxrt1060_evk/mimxrt1062/hyperflash`
     - |NXP Semiconductors|_
     - |MIMXRT1060-EVK (CDC ACM)|
     - derived VID from part number MIMXRT1062DVL6A
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |arduino_zero_URB_VID|
     - |arduino_zero_URB_PID_CON|
     - :code:`arduino_zero`
     - |Arduino LLC|_
     - |Arduino Zero (CDC ACM)|
     - `Arduino USB product ID list with SAMD21 CPU`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |seeeduino_lotus_URB_VID|
     - |seeeduino_lotus_URB_PID_CON|
     - :code:`seeeduino_lotus`
     - |Seeed LLC|_
     - |Seeeduino Lotus Cortex-M0+ (CDC ACM)|
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |seeeduino_cm0_URB_VID|
     - |seeeduino_cm0_URB_PID_CON|
     - :code:`seeeduino_cm0`
     - |Seeed LLC|_
     - |Seeeduino Cortex-M0+ (CDC ACM)|
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |seeeduino_xiao_URB_VID|
     - |seeeduino_xiao_URB_PID_CON|
     - :code:`seeeduino_xiao`
     - |Seeed LLC|_
     - | |Seeed XIAO M0 (CDC ACM)|,
       | Seeeduino XIAO
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |xiao_samd21_URB_VID|
     - |xiao_samd21_URB_PID_CON|
     - :code:`xiao_samd21`
     - |Seeed Studio|_
     - | |XIAO SAMD21 (CDC ACM)|,
       | Seeeduino XIAO
     - `Seeeduino USB product ID list with SAMD21 CPU`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |cytron_maker_nano_rp2040_URB_VID|
     - |cytron_maker_nano_rp2040_URB_PID_CON|
     - :code:`cytron_maker_nano_rp2040`
     - |Cytron (Raspberry Pi)|_
     - | |Maker Nano RP2040 (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |cytron_maker_pi_rp2040_URB_VID|
     - |cytron_maker_pi_rp2040_URB_PID_CON|
     - :code:`cytron_maker_pi_rp2040`
     - |Cytron (Raspberry Pi)|_
     - | |Maker Pi RP2040 (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |rpi_pico_URB_VID|
     - |rpi_pico_URB_PID_CON|
     - :code:`rpi_pico`
     - |Raspberry Pi|_
     - | |RPi Pico (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |rpi_pico_rp2040_w_URB_VID|
     - |rpi_pico_rp2040_w_URB_PID_CON|
     - :code:`rpi_pico/rp2040/w`
     - |Raspberry Pi|_
     - | |RPi Pico W (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |rpi_pico2_rp2350a_URB_VID|
     - |rpi_pico2_rp2350a_URB_PID_CON|
     - | :code:`rpi_pico2/rp2350a/hazard3`
       | :code:`rpi_pico2/rp2350a/m33`
     - |Raspberry Pi|_
     - | |RPi Pico 2 (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |rpi_pico2_rp2350a_w_URB_VID|
     - |rpi_pico2_rp2350a_w_URB_PID_CON|
     - :code:`rpi_pico2/rp2350a/m33/w`
     - |Raspberry Pi|_
     - | |RPi Pico 2W (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_one_URB_VID|
     - |waveshare_rp2040_one_URB_PID_CON|
     - :code:`waveshare_rp2040_one`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-One (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_zero_URB_VID|
     - |waveshare_rp2040_zero_URB_PID_CON|
     - :code:`waveshare_rp2040_zero`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-Zero (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_matrix_URB_VID|
     - |waveshare_rp2040_matrix_URB_PID_CON|
     - :code:`waveshare_rp2040_matrix`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-Matrix (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_tiny_URB_VID|
     - |waveshare_rp2040_tiny_URB_PID_CON|
     - :code:`waveshare_rp2040_tiny`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-Tiny (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_eth_URB_VID|
     - |waveshare_rp2040_eth_URB_PID_CON|
     - :code:`waveshare_rp2040_eth`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-ETH (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_lcd_0_96_URB_VID|
     - |waveshare_rp2040_lcd_0_96_URB_PID_CON|
     - :code:`waveshare_rp2040_lcd_0_96`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-LCD-0.96 (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_plus_URB_VID|
     - |waveshare_rp2040_plus_URB_PID_CON|
     - | :code:`waveshare_rp2040_plus`
       | :code:`waveshare_rp2040_plus@16MB`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-Plus (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2040_geek_URB_VID|
     - |waveshare_rp2040_geek_URB_PID_CON|
     - :code:`waveshare_rp2040_geek`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2040-Geek (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |waveshare_rp2350_can_URB_VID|
     - |waveshare_rp2350_can_URB_PID_CON|
     - | :code:`waveshare_rp2350_can/rp2350a/hazard3`
       | :code:`waveshare_rp2350_can/rp2350a/m33`
     - |Waveshare (Raspberry Pi)|_
     - | |RP2350-CAN (CDC ACM)|,
       | Raspberry Pi Pico SDK CDC UART
     - `Raspberry Pi USB product ID list`_
     - | |zephyr:devicetree:chosen:console|
       | |zephyr:devicetree:chosen:shell-uart|

   * - |zephyr_URB_VID|
     - |zephyr_URB_PID_CON|
     -
     - |Zephyr Project|_
     - :external+zephyr:zephyr:code-sample:`usb-cdc-acm-console`
     - Zephyr :external+zephyr:ref:`usb_device_vid_pid`
     - | |zephyr:devicetree:chosen:console|

How to add support of a new board
*********************************

* add board configuration and devicetree overlay to this snippet;
* which overwrites following options:

  - |CONFIG_CDC_ACM_SERIAL_VID|
  - |CONFIG_CDC_ACM_SERIAL_PID|
  - |CONFIG_CDC_ACM_SERIAL_MANUFACTURER_STRING|
  - |CONFIG_CDC_ACM_SERIAL_PRODUCT_STRING|

Requirements
************

Hardware support for:

   - |CONFIG_USB_DEVICE_STACK_NEXT|
   - |CONFIG_SERIAL|
   - |CONFIG_CONSOLE|
   - |CONFIG_UART_CONSOLE|
   - |CONFIG_UART_LINE_CTRL|

A devicetree node with node label ``zephyr_udc0`` that points to an enabled USB
device node with driver support. This should look roughly like this in
:external+zephyr:ref:`your devicetree <get-devicetree-outputs>`:

   .. code-block:: DTS

      zephyr_udc0: usbd@deadbeef {
           compatible = "vnd,usb-device";
           /* ... */
      };

References
**********

.. target-notes::
