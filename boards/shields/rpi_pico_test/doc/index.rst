.. _rpi_pico_test_shield:

Raspberry Pi Pico TEST Shields
##############################

This simple shields are well suited for teaching and training to learn how to
access GPIO, PWM or ADC signals and how to use the associated Zephyr APIs. As a
demo board you can test if all pins of the Pico are in good condition. As an
expansion board, this module contains LEDs, buttons, and a basic ADC function to
get you started. It is a simple expansion board for Raspberry Pi Pico beginners.

.. toctree::
   :caption: Supported Shields
   :maxdepth: 1
   :glob:

   **/index

Utilization
***********

This shields can only be used with a development board, shield, or snippet that
provides a configuration for the serial console over USB device, because the
default serial device node :dts:`&rpipico_serial` (a.k.a. :dts:`&pico_serial`)
will be disable completely and can't be used anymore for serial communication
such as logging or shell access. The same applies also to the other buses such
as I2C or SPI.
