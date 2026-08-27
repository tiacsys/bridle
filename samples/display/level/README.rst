.. _level-sample:

Level
#####

A digital spirit level on an RGB LED matrix, driven through the Display
driver API and fed from an accelerometer.

Overview
********

This sample turns the board into a digital spirit level. The on-board
accelerometer measures which way is down, and a bubble drawn on the RGB LED
matrix runs towards whichever edge of the board is raised, exactly like the
bubble in a vial. Hold the board flat and the bubble returns to the middle of
the panel.

The panel is driven through the :external+zephyr:ref:`Display driver API
<display_api>` and the sensor through the :external+zephyr:ref:`Sensor driver
API <sensor>`, so the same binary runs on panels of different geometry, wiring
order and pixel format without any board specific code. The panel is taken from
the :dts:`chosen { zephyr,display = ...; };` node, which on the supported board
resolves to a :dts:`led-strip-matrix` device on top of a WS2812 compatible LED
strip. The sensor is taken from the ``accel0`` alias; only the accelerometer is
used, since a level needs the drift-free reference that gravity provides and a
gyroscope does not.

Techniques worth knowing about:

* The acceleration vector is normalised against its own length, which turns the
  in-plane components into plain sines of the tilt angle, and is smoothed by a
  first order low pass filter before use.
* The bubble is rendered with sub-pixel accuracy: instead of snapping to the
  nearest pixel, its light is spread bilinearly over the up to four pixels it
  straddles.
* Since position runs out of resolution near the centre, the bubble also changes
  colour over a much tighter angle than it moves over, and latches to the near
  colour, with hysteresis, once the board is level.

Requirements
************

An RGB LED matrix assigned to the ``zephyr,display`` chosen node, with a pixel
format of either RGB_888 or ARGB_8888, **and** a 3-axis accelerometer assigned
to the ``accel0`` alias.

The sample supports the following platforms (located in
:bridle_file:`samples/display/level/tests.yaml`):

.. table-from-tests-yaml::

Configuration options
*********************

The following sample-specific Kconfig options are used in this sample
(located in :bridle_file:`samples/display/level/Kconfig`):

.. options-from-kconfig::

.. important::

   Keep ``CONFIG_LEVEL_BRIGHTNESS`` low. A WS2812B pixel draws up to 60 ㎃ at
   full white according to the `WS2812B datasheet`_, so an 8×8 panel alone can
   draw more than 3.5 A, far beyond what a typical board's USB supply can
   deliver.

Building and Running
********************

.. zephyr-keep-sorted-start re(^\* \w)

* On |RP2350-Matrix| board, on ARM Cortex-M33:

  .. zephyr-app-commands::
     :app: bridle/samples/display/level
     :build-dir: level-waveshare_rp2350_matrix
     :board: waveshare_rp2350_matrix/rp2350a/m33
     :snippets: "usb-console"
     :west-args: -p
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

* On |RP2350-Matrix| board, on Hazard3 RISC-V (RV32IMAC+):

  .. zephyr-app-commands::
     :app: bridle/samples/display/level
     :build-dir: level-waveshare_rp2350_matrix
     :board: waveshare_rp2350_matrix/rp2350a/hazard3
     :snippets: "usb-console"
     :west-args: -p
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

.. zephyr-keep-sorted-stop

Sample output
=============

The following output is logged on the UART console, here for the 8×8
panel of the |RP2350-Matrix| board lying nearly flat on the table:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* \*\*\*
      [00:00:00.003,000] <inf> level: Level on a 8x8 RGB matrix, 4 bytes per pixel, 40 ms per frame
      [00:00:00.003,000] <inf> level: Inertial sensor is qmi8658a\ @\ 6b, full scale tilt is 10 deg
      [00:00:00.003,000] <inf> level: Axis map: swap-xy yes, invert-x yes, invert-y no
      [00:00:00.003,000] <inf> level: Filter time constant is 100 ms, giving a weight of 0.330 per sample
      [00:00:00.003,000] <inf> level: Colour ramps below 1.0 deg, latches level below 0.5 deg, releases at 0.8 deg
      [00:00:02.010,000] <inf> level: accel  -0.569  -1.183  -9.630 m/s^2, \|a|  9.719
      [00:00:02.010,000] <inf> level: tilt  x +0.122 y -0.059, angle  7.76 deg
      [00:00:02.010,000] <inf> level: dot    5.95,  2.32, proximity 0.00

.. _level-axis-mapping:

Axis mapping
============

Nothing in the devicetree says how the sensor is oriented relative to the
panel, and a bubble floats towards the *raised* edge, the opposite of
where the gravity vector points. Both are folded into the
``CONFIG_LEVEL_AXIS_*`` options, defaulted per board:

.. list-table::
   :header-rows: 1

   * - Board
     - ``SWAP_XY``
     - ``INVERT_X``
     - ``INVERT_Y``
   * - |RP2350-Matrix|
     - yes
     - yes
     - no
   * - anything else
     - no
     - no
     - no

To bring up a new board:

#. Lay the board flat, LEDs up. Note where the corner test image puts its red
   pixel: that is the origin of the panel.
#. Build and flash with all three switches off. Raise the edge **closest
   to you** and watch the bubble:

   * It moves towards you: correct, leave the switches alone.
   * It moves away from you: set ``CONFIG_LEVEL_AXIS_INVERT_Y=y``.
   * It moves left or right instead: set ``CONFIG_LEVEL_AXIS_SWAP_XY=y``
     and repeat this step.

#. Raise the **left** edge. If the bubble moves right instead of left,
   set ``CONFIG_LEVEL_AXIS_INVERT_X=y``.
#. Record the result as a per board default in
   :bridle_file:`samples/display/level/Kconfig`.

The console prints the mapping in use at startup. Zephyr's
:dts:`sensor-axis-align` devicetree convention would be the proper home
for the hardware half of this mapping, but the ``qst,qmi8658a`` binding
does not support it yet.

Troubleshooting
===============

The panel stays dark
   Check that the board assigns a matrix to the ``zephyr,display`` chosen
   node. The build fails when no such node exists, but a board that chooses
   a different kind of display reports an unsupported pixel format at run
   time instead.

The corner colours are wrong or the image is mirrored
   The panel is not wired the way the matrix node describes. Review the
   ``circulative``, ``serpentine`` and ``color-mapping`` properties.

The dot runs the wrong way
   The sensor is not oriented the way the panel is. Work through
   :ref:`level-axis-mapping`.

The dot never leaves the middle, or pins to the rim at the slightest tilt
   ``CONFIG_LEVEL_FULL_SCALE_TILT`` is too large or too small for the way
   you are holding the board. The console reports the measured angle in
   degrees, so compare that against the configured full scale.

The bubble will not sit still, or lags behind your hand
   Adjust ``CONFIG_LEVEL_FILTER_TIME_CONSTANT``: raise it for
   steadiness, lower it for responsiveness. Set it to ``0`` to see the
   raw, unfiltered reading.

The colour flickers while the board is nearly level
   Raise ``CONFIG_LEVEL_LOCK_HYSTERESIS``. Set it to ``0`` once to see
   the flicker it is there to prevent.

Dependencies
************

This sample uses the following Zephyr libraries:

* :external+zephyr:ref:`display_api`:

  * ``include/zephyr/drivers/display.h``

* :external+zephyr:ref:`sensor`:

  * ``include/zephyr/drivers/sensor.h``

* :external+zephyr:ref:`led_api`, by way of the LED strip matrix display
  driver
* :external+zephyr:ref:`kernel_api`:

  * ``include/zephyr/kernel.h``

References
**********

.. target-notes::

.. _WS2812B datasheet: https://www.world-semi.com/ws2812-family/
