.. _rpi_pico_clock_shield:

Raspberry Pi Pico Clock Shields
###############################

This is a collection of very versatile clocks due to its different feature sets
and sizes, the RGB capabilities and additional buttons and sensors. Nearly all
displays comes with a special LED controller wired over GPIO or other standard
serial buses up to the Raspberry Pi Pico. Additional momentary push buttons or
joysticks and a small buzzer are wired up over simple GPIO lines. Some shield
provide also a simple temperature sensor or Real-Time-Clock, mostly wired over
a dedicated I2C bus.

.. toctree::
   :caption: Supported Shields
   :maxdepth: 1
   :glob:

   **/index

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, the I2C1 bus on pins 9 to 10 and
some GPIO signals on pins 4 to 5, 14 to 22, 24 and 29 of this edge connector
must be free for communication with the buttons, buzzer, LEDs, RTC and sensors
on the shields. The ADC channel 0 on pin 31 must also be free for communication
with the on-shield LDR (photoresistor). The shields also provide the special
Devicetree labels :dts:`&rpipico_i2c_rtc`, :dts:`&clock_rtc`,
:dts:`&rpipico_pwm_buzzers` and :dts:`&clock_buzzer` for this
purpose.
