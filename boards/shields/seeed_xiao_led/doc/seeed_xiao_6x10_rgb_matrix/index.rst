.. _seeed_xiao_6x10_rgb_matrix:

Seeed Studio XIAO (6x10 RGB) MATRIX
###################################

Overview
********

The `Seeed Studio XIAO MATRIX`_ is an LED matrix module designed for
|zephyr:board:xiao_rp2040|, which has 6 × RGB × 10 (60) full-color external
controlled constant current integrated LEDs, with embedded quality controller
IC and LED chip. It is a :bbl:`XIAO sized` clean-looking front panel. Some but
not all XIAO sized boards are currently supported, see status below.

:|okay|:

   .. admonition:: STATUS
      :class: hint dropdown

      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      |        | Board name                               | Build target                                    | XIAO connector | Known issues |
      +========+==========================================+=================================================+================+==============+
      | |okay| | |zephyr:board:xiao_ble|                  | | ``xiao_ble/nrf52840``                         |     |okay|     | - Revision   |
      |        |                                          | | ``xiao_ble/nrf52840/sense``                   |                |   *"sense"*  |
      |        |                                          |                                                 |                |   not tested |
      |        |                                          |                                                 |                |   on real    |
      |        |                                          |                                                 |                |   hardware.  |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:xiao_esp32c3|              | | ``xiao_esp32c3``                              |     |okay|     |              |
      |        |                                          | | ``xiao_esp32c3/esp32c3``                      |                |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      ||notyet|| |zephyr:board:xiao_esp32c6|              | |                                               |     |?|        |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      ||notyet|| |zephyr:board:xiao_esp32c6|              | |                                               |     |?|        |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:xiao_esp32s3|              | | ``xiao_esp32s3/esp32s3/procpu``               |     |okay|     | - Revision   |
      |        |                                          | | ``xiao_esp32s3/esp32s3/procpu/sense``         |                |   *"sense"*  |
      |        |                                          |                                                 |                |   not tested |
      |        |                                          |                                                 |                |   on real    |
      |        |                                          |                                                 |                |   hardware.  |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:xiao_mg24|                 | | ``xiao_mg24``                                 |     |okay|     |              |
      |        |                                          | | ``xiao_mg24/efr32mg24b220f1536im48``          |                |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      ||notyet|| |zephyr:board:xiao_nrf54l15|             | |                                               |     |?|        |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      ||notyet|| |zephyr:board:xiao_nrf54lm20a|           | |                                               |     |?|        |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      ||notyet|| |zephyr:board:xiao_nrf54lm20b|           | |                                               |     |?|        |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:xiao_ra4m1|                | | ``xiao_ra4m1``                                |     |warn|     | - Requires   |
      |        |                                          | | ``xiao_ra4m1/r7fa4m1ab3cne``                  |                |   hardware   |
      |        |                                          |                                                 |                |   hack.      |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:xiao_rp2040|               | | ``xiao_rp2040``                               |     |okay|     |              |
      |        |                                          | | ``xiao_rp2040/rp2040``                        |                |              |
      +--------+------------------------------------------+-------------------------------------------------+                |              |
      | |okay| | |bridle:board:xiao_rp2040|               | | ``xiao_rp2040/rp2040/bbe``                    |                |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:xiao_rp2350|               | | ``xiao_rp2350/rp2350a/hazard3_0``             |     |okay|     |              |
      |        |                                          | | ``xiao_rp2350/rp2350a/m33_0``                 |                |              |
      +--------+------------------------------------------+-------------------------------------------------+                |              |
      | |okay| | |bridle:board:xiao_rp2350|               | | ``xiao_rp2350/rp2350a/hazard3_0/bbe``         |                |              |
      |        |                                          | | ``xiao_rp2350/rp2350a/m33_0/bbe``             |                |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:xiao_stm32c5|              | | ``xiao_stm32c5``                              |     |okay|     |              |
      |        |                                          | | ``xiao_stm32c5/stm32c5a3xx``                  |                |              |
      +--------+------------------------------------------+-------------------------------------------------+                |              |
      | |okay| | |bridle:board:xiao_stm32c5|              | | ``xiao_stm32c5/stm32c5a3xx/bbe``              |                |              |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+
      | |okay| | |zephyr:board:seeeduino_xiao|            | | ``seeeduino_xiao``                            |     |warn|     | - Requires   |
      |        |                                          | | ``seeeduino_xiao/samd21g18a``                 |                |   hardware   |
      +--------+------------------------------------------+-------------------------------------------------+                |   hack.      |
      | |okay| | |bridle:board:seeeduino_xiao|            | | ``seeeduino_xiao/samd21g18a/bbe``             |                | - Bit-frame  |
      +--------+------------------------------------------+-------------------------------------------------+                |   errors, no |
      | |okay| | |bridle:board:xiao_samd21|               | | ``xiao_samd21``                               |                |   access to  |
      |        |                                          | | ``xiao_samd21/samd21g18a``                    |                |   first LED  |
      |        |                                          |                                                 |                |   in chain.  |
      |        |                                          |                                                 |                |   SPI driver |
      |        |                                          |                                                 |                |   faulty?    |
      +--------+------------------------------------------+-------------------------------------------------+----------------+--------------+

:|warn|:

   .. admonition:: HARDWARE HACK REQUIRED
      :class: warning dropdown toggle-shown

      The Shield always expects the required bitstream to be present at
      Pin :rpi-pico-pin:`1` of the XIAO connector, via the :rpi-pico-sys:`D0`
      data line. Unfortunately, the XIAO RA4M1 and XIAO SAMD21 (aka Seeeduino
      XIAO) boards do not provide an adequate output on this pin via their
      respective SoCs for hardware-accelerated output of the bitstream required
      for the digital RGB LEDs. The shield also does not provide an alternative
      connection, which is why a manual connection must be established between
      Pin :rpi-pico-pin:`11` and Pin :rpi-pico-pin:`1` on the XIAO connector.

      :brd:`Warning:` This carries the risk of short-circuiting I/O lines on
      the board or SoC and must be done with appropriate caution.
      To be on the safe side, you can prevent the connection to the SoC at
      Pin :rpi-pico-pin:`1` by making a slight mechanical adjustment to the
      board's pin headers (bending them).

      :XIAO RA4M1:

         .. image:: wiring_ra4m1.jpg
            :align: left
            :alt: Seeed Studio XIAO MATRIX for XIAO RA4M1 wiring

      :XIAO SAMD21 (aka Seeeduino XIAO):

         .. image:: wiring_samd21.jpg
            :align: left
            :alt: Seeed Studio XIAO MATRIX for XIAO SAMD21 (aka Seeeduino XIAO) wiring

      .. rubric:: Bit-frame errors have been observed on Atmel SAMD21 targets

      It looks like bits are being incorrectly "pushed" onto the COPI data
      line even when the LED chain has reached its end (the W2812 driver
      no longer wants to send any more bits). This is not surprising, as
      unlike standard SPI communication, there is no form of gating on the
      COPI data line via a chip select signal. It therefore remains to be
      investigated whether the Atmel SPI driver has a fundamental design
      issue or whether, for this specific use case, an additional gate via
      the SPI chip select must be added in hardware.


Hardware
========

.. include:: hardware.rsti

Positions
=========

.. include:: positions.rsti

Pinouts
=======

.. include:: pinouts.rsti

Basic Samples
*************

LED Blinky and Button
=====================

.. include:: led_button.rsti

Hello Shell on the USB Console (CDC/ACM)
========================================

.. include:: helloshell.rsti

More Samples
************

LED strip test pattern
======================

Drives an RGB LED strip that must defined by the shields Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

.. include:: ledstrip_test.rsti

LED Display Orientation and Bit Order Test
==========================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LED display and correct
RGB bit order.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. include:: display_test.rsti

More fancy LED Display samples in Bridle
========================================

Try out for yourself:

* :ref:`colorful-sample` |--| Draw an RGB color gradient on a display device.
* :ref:`colorwheel-sample` |--| Animate a circular HSV color space projection.

References
**********

.. target-notes::
