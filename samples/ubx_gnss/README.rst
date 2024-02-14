.. _ubx_gnss_sample:

Ubxlib GNSS Sample
##################

Overview
********

A sample application demonstrating how to integrate a u-blox GNSS device into
a Zephyr application. The example code is rigidly configured to work with an
`u-blox M10 device`_. It was tested with the `SparkFun MAX-M10S Breakout`_.

Requirements
************

The u-blox GNSS device must be connected via UART, and a Devicetree alias
:devicetree:`ubxlib-uart0` must exist that point towards this UART port. Also
a single GPIO line for the module reset signal have to define. To fulfil this
requirement, this sample application comes with a generic application overlay
:file:`app.overlay` that should be usable with all boards that provies an
Arduino UNO R3 edge connector. For :devicetree:`ubxlib-uart0` the standard
Arduino UART on D0 (RX) and D1 (TX) will be used
(:devicetree:`&arduino_serial`). The reset signal will be controlled by
D8 (GPIO) and is mapped to :devicetree:`<&arduino_header 14 /*…*/>`. To ensure
to use the correct GPIO line for the module reset signal, the example provides
the only locally usable Devicetree binding :file:`reset-switch.yaml`. This
specifies the Devicetree compatibility string :emphasis:`reset-switch`.

.. list-table::
   :align: center
   :width: 75%
   :widths: 50, 50
   :header-rows: 1

   * - Default application overlay
     - Binding for the module reset signal

   * - .. literalinclude:: app.overlay
          :caption: app.overlay
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 3-4,8
          :prepend: / {
          :start-at: reset_switch {

     - .. literalinclude:: dts/bindings/reset-switch.yaml
          :caption: reset-switch.yaml
          :language: yaml
          :encoding: ISO-8859-1
          :emphasize-lines: 3
          :start-at: description:

Regardless of this, it is still free and open to use a specific board overlay
to adapt these default settings to other hardware conditions.

Building and Running
********************

Build and flash for different boards
====================================

.. rubric:: ST Nucleo L496ZG

.. zephyr-app-commands::
   :zephyr-app: bridle/samples/ubx_gnss
   :board: nucleo_l496zg
   :build-dir: nucleo_l496zg-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: ST Nucleo F413ZH

.. zephyr-app-commands::
   :zephyr-app: bridle/samples/ubx_gnss
   :board: nucleo_f413zh
   :build-dir: nucleo_f413zh-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: ST Nucleo F767ZI

.. zephyr-app-commands::
   :zephyr-app: bridle/samples/ubx_gnss
   :board: nucleo_f767zi
   :build-dir: nucleo_f767zi-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: NXP MIMXRT1060-EVK

.. zephyr-app-commands::
   :zephyr-app: bridle/samples/ubx_gnss
   :board: mimxrt1060_evk
   :build-dir: mimxrt1060_evk-ubx_gnss
   :west-args: -p
   :flash-args: -r pyocd
   :goals: flash
   :compact:

Example console session
=======================

After power-on or hard reset, the GNSS module will be initialized automatically:

   .. code-block:: console

      *** Booting Zephyr OS build … ***
      [00:00:02.021,000] <inf> main: GNSS Device is ready!
      uart:~$ _

There is a simple Shell command for some standard evaluation steps:

   .. code-block:: console

      uart:~$ gnss -h
      gnss - GNSS related commands
      Subcommands:
        single  :Get a one-shot position estimate
        stream  :Start or stop streaming of position estimates
        reset   :Reset GNSS module
        ttff    :Measure TTFF
      uart:~$ _

Reset GNSS module:

   .. code-block:: console

      uart:~$ gnss reset
      uart:~$ _

   The on-module LED for PPS signaling goes off and comes back to blink
   after TTFF.

Measure TTFF:

   .. code-block:: console

      uart:~$ gnss ttff
      Run 1 of 1: Acquired fix after 32.26s
      ---------------
      Avg. TTFF: 32.26
      uart:~$ _

   The on-module LED for PPS signaling goes off and comes back to blink
   after TTFF.

   It is also possible to run several TTFF measurements sequentially. If
   there is also a good receiving range and a reliable position already
   exists, the TTFF will be correspondingly low:

   .. code-block:: console

      uart:~$ gnss ttff 10
      Run 1 of 10: Acquired fix after 0.23s
      Run 2 of 10: Acquired fix after 0.79s
      Run 3 of 10: Acquired fix after 1.00s
      Run 4 of 10: Acquired fix after 0.59s
      Run 5 of 10: Acquired fix after 0.81s
      Run 6 of 10: Acquired fix after 0.79s
      Run 7 of 10: Acquired fix after 0.80s
      Run 8 of 10: Acquired fix after 1.01s
      Run 9 of 10: Acquired fix after 0.58s
      Run 10 of 10: Acquired fix after 0.81s
      ---------------
      Avg. TTFF: 0.74

Get a one-shot position estimate:

   .. code-block:: console

      uart:~$ gnss single
      Found position estimate after 0.8s: (lat, lon): (50.922432, 11.600015), alt: 192.05m, radius: 1.48m (15 SV used)
      uart:~$ _

Start or stop streaming of position estimates:

   .. code-block:: console

      uart:~$ gnss stream start
      [00:01:15.687,000] <inf> main: Found position estimate: (lat, lon): (50.922447, 11.600006), alt: 192.64m, radius: 1.45m (17 SV used)
      [00:01:16.692,000] <inf> main: Found position estimate: (lat, lon): (50.922451, 11.600005), alt: 192.53m, radius: 1.45m (18 SV used)
      [00:01:17.697,000] <inf> main: Found position estimate: (lat, lon): (50.922451, 11.600004), alt: 192.63m, radius: 1.45m (18 SV used)
      [00:01:18.904,000] <inf> main: Found position estimate: (lat, lon): (50.922455, 11.600004), alt: 192.71m, radius: 1.46m (17 SV used)
      [00:01:19.658,000] <inf> main: Found position estimate: (lat, lon): (50.922455, 11.600004), alt: 192.80m, radius: 1.46m (18 SV used)
      [00:01:20.663,000] <inf> main: Found position estimate: (lat, lon): (50.922455, 11.600004), alt: 192.96m, radius: 1.46m (18 SV used)
      [00:01:21.667,000] <inf> main: Found position estimate: (lat, lon): (50.922455, 11.600003), alt: 192.89m, radius: 1.46m (18 SV used)
      [00:01:22.722,000] <inf> main: Found position estimate: (lat, lon): (50.922459, 11.600002), alt: 192.79m, radius: 1.47m (17 SV used)
      [00:01:23.929,000] <inf> main: Found position estimate: (lat, lon): (50.922459, 11.600001), alt: 192.92m, radius: 1.47m (18 SV used)
      [00:01:24.683,000] <inf> main: Found position estimate: (lat, lon): (50.922462, 11.600000), alt: 192.89m, radius: 1.48m (17 SV used)
      [00:01:25.688,000] <inf> main: Found position estimate: (lat, lon): (50.922462, 11.599999), alt: 192.77m, radius: 1.48m (18 SV used)
      [00:01:26.693,000] <inf> main: Found position estimate: (lat, lon): (50.922466, 11.599998), alt: 192.69m, radius: 1.48m (18 SV used)
      [00:01:27.697,000] <inf> main: Found position estimate: (lat, lon): (50.922466, 11.599996), alt: 192.49m, radius: 1.50m (18 SV used)
      uart:~$ gnss stream stop
      [00:01:28.905,000] <inf> main: Found position estimate: (lat, lon): (50.922470, 11.599995), alt: 192.22m, radius: 1.50m (18 SV used)
      [00:01:29.709,000] <inf> main: Found position estimate: (lat, lon): (50.922470, 11.599994), alt: 192.12m, radius: 1.50m (18 SV used)
      uart:~$ _

References
**********

.. target-notes::

.. _`u-blox M10 device`: https://www.u-blox.com/en/product/ubx-m10050-chip
.. _`SparkFun MAX-M10S Breakout`: https://www.sparkfun.com/products/18037
