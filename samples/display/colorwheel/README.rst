.. _colorwheel-sample:

Color wheel
###########

Animate a circular HSV color space projection that spins around the centre of an
RGB LED matrix, using the Display driver API.

Overview
********

This sample paints a color wheel onto an RGB LED matrix: the hue of each pixel
follows its polar angle around the centre, so a full rainbow wraps once around
the middle, while saturation rises with the radius. A bright white core in the
centre blooms into fully saturated color towards the corners, and the whole
wheel slowly spins. It drives the panel through the
:external+zephyr:ref:`Display driver API <display_api>` rather than the LED
strip API of the :external+zephyr:ref:`LED subsystem <led_api>`, so the same
binary runs on panels of different geometry, wiring order and pixel format
without any board specific code.

The panel is taken from the :dts:`chosen { zephyr,display = ...; };` node, which
on all supported boards resolves to a :dts:`led-strip-matrix` device on top of a
WS2812 compatible LED strip. That driver maps a rectangular frame buffer onto
the serpentine or circulative pixel order of the physical strip.

Color model
===========

A color wheel is much easier to express in `HSL and HSV`_ than in RGB: hue is
the angle, saturation is the radius, and value sets the brightness of the whole
panel. The sample computes every pixel in HSV and converts it to RGB in
:bridle_file:`samples/display/colorwheel/src/hsv.c`.

Each pixel is placed in a polar coordinate system centred on the panel, and the
HSV values computed as follows:

.. code-block:: none

   hue(x, y)        = atan2(y - cy, x - cx) + phase
   saturation(x, y) = 255 * dist((x, y), centre) / (corner_radius * scale)
   value(x, y)      = CONFIG_COLORWHEEL_MAX_BRIGHTNESS

where ``(cx, cy)`` is the centre of the panel and the radius is normalised
against a fraction of the corner distance, in percent, set by
``CONFIG_COLORWHEEL_SAT_SCALE``, at which the ramp reaches full saturation.

Configuration options
*********************

The following sample-specific Kconfig options are used in this sample
(located in :bridle_file:`samples/display/colorwheel/Kconfig`):

.. options-from-kconfig::

.. important::

   Keep ``CONFIG_COLORWHEEL_MAX_BRIGHTNESS`` low. A WS2812B pixel draws up to 60
   ㎃ at full white according to the `WS2812B datasheet`_, so an 8×8 panel alone
   can draw more than 3.5 A, far beyond what a typical board's USB supply can
   deliver.

Requirements
************

An RGB LED matrix assigned to the ``zephyr,display`` chosen node, with a
pixel format of either RGB_888 or ARGB_8888. Either one of the following
development boards with an on-board matrix:

* |RP2350-Matrix| (Waveshare RP2350-Matrix), an 8×8 panel
* |RP2040-Matrix| (Waveshare RP2040-Matrix), a 5×5 panel

or a Raspberry Pi Pico compatible board carrying the following shield:

* |Waveshare Pico RGB LED| (Waveshare Pico-RGB-LED), a 16×10 panel

The sample supports the following platforms (located
in :bridle_file:`samples/display/colorwheel/tests.yaml`):

.. table-from-tests-yaml::

Building and Running
********************

.. zephyr-keep-sorted-start re(^\* \w)

* On |RP2350-Matrix| board, on ARM Cortex-M33:

  .. zephyr-app-commands::
     :app: bridle/samples/display/colorwheel
     :build-dir: colorwheel-waveshare_rp2350_matrix
     :board: waveshare_rp2350_matrix/rp2350a/m33
     :snippets: "usb-console"
     :west-args: -p
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

* On |RP2350-Matrix| board, on Hazard3 RISC-V (RV32IMAC+):

  .. zephyr-app-commands::
     :app: bridle/samples/display/colorwheel
     :build-dir: colorwheel-waveshare_rp2350_matrix
     :board: waveshare_rp2350_matrix/rp2350a/hazard3
     :snippets: "usb-console"
     :west-args: -p
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

* On |Waveshare Pico RGB LED| shield, on a Raspberry Pi Pico:

  .. zephyr-app-commands::
     :app: bridle/samples/display/colorwheel
     :build-dir: colorwheel-rpi_pico
     :board: rpi_pico/rp2040/bbe
     :shield: waveshare_pico_rgb_led
     :snippets: "usb-console"
     :west-args: -p
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

.. zephyr-keep-sorted-stop

Sample output
=============

The following output is logged on the UART console, here for the 8×8
panel of the |RP2350-Matrix| board:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* \*\*\*
      [00:00:00.003,000] <inf> colorwheel: Color wheel on a 8x8 RGB matrix, 4 bytes per pixel, 40 ms per frame

Troubleshooting
===============

The panel stays dark
   Check that the board assigns a matrix to the ``zephyr,display`` chosen
   node. The build fails when no such node exists, but a board that chooses
   a different kind of display reports an unsupported pixel format at run
   time instead.

The panel flickers or the board resets
   The LED strip is almost certainly browning out the supply. Lower
   ``CONFIG_COLORWHEEL_MAX_BRIGHTNESS``, or feed the panel from a supply
   that can carry the current.

The centre of the wheel is not white
   The centre should be a bright white core on any panel. If it is not, the
   matrix is most likely cropped by a ``width`` or ``height`` smaller than
   the physical panel, which moves the geometric centre off the true
   middle. Check the ``width`` and ``height`` properties of the matrix node
   against the panel.

Dependencies
************

This sample uses the following Zephyr libraries:

* :external+zephyr:ref:`display_api`:

  * ``include/zephyr/drivers/display.h``

* :external+zephyr:ref:`led_api`, by way of the LED strip matrix display
  driver
* :external+zephyr:ref:`kernel_api`:

  * ``include/zephyr/kernel.h``

Known issues and limitations
****************************

The sample redraws and rewrites the whole panel on every frame, even when
``CONFIG_COLORWHEEL_HUE_STEP`` is ``0`` and nothing has changed. This keeps
the code simple at the cost of some unnecessary traffic to the LED strip.

References
**********

.. target-notes::

.. _HSL and HSV: https://en.wikipedia.org/wiki/HSL_and_HSV
.. _WS2812B datasheet: https://www.world-semi.com/ws2812-family/
