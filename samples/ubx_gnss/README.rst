.. _ubx_gnss-sample:

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
:dts:`ubxlib-uart0` must exist that point towards this UART port. Also a
single GPIO line for the module reset signal have to define. To fulfil this
requirement, this sample application comes with a generic application overlay
:file:`app.overlay` that should be usable with all boards that provies an
Arduino UNO R3 edge connector. For :dts:`ubxlib-uart0 = /* … */` the
standard Arduino UART on **D0** (*RX*) and **D1** (*TX*) will be used
(:dts:`ubxlib-uart0 = &arduino_serial`;). The reset signal will be controlled
by **D8** (*IO8*) and is mapped in :dts:`gpios = <&arduino_header 14 /* … */>`.
To ensure to use the correct GPIO line for the module reset signal, the example
provides the only locally usable Devicetree binding :file:`reset-switch.yaml`.
This specifies the Devicetree compatibility string :yaml:`"reset-switch"` (see
line :yaml:`compatible: "reset-switch"`) with the required :yaml:`gpios:`
property.

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

.. rubric:: Nordic nRF9160 DK (nRF9160)

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: nrf9160dk/nrf9160
   :build-dir: nrf9160dk_nrf9160-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: Nordic nRF52840 DK (nRF52840)

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: nrf52840dk/nrf52840
   :build-dir: nrf52840dk_nrf52840-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: ST Nucleo L496ZG

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: nucleo_l496zg
   :build-dir: nucleo_l496zg-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: ST Nucleo F413ZH

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: nucleo_f413zh
   :build-dir: nucleo_f413zh-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: ST Nucleo F767ZI

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: nucleo_f767zi
   :build-dir: nucleo_f767zi-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: NXP MIMXRT1170-EVKB (CM7)

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: mimxrt1170_evk@B/mimxrt1176/cm7
   :build-dir: mimxrt1170_evkb_cm7-ubx_gnss
   :west-args: -p
   :flash-args: -r pyocd
   :goals: flash
   :compact:

.. rubric:: NXP MIMXRT1060-EVK

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: mimxrt1060_evk@B//qspi
   :build-dir: mimxrt1060_evk-ubx_gnss
   :west-args: -p
   :flash-args: -r pyocd
   :goals: flash
   :compact:

.. rubric:: NXP MIMXRT1010-EVK (experimental)

.. zephyr-app-commands::
   :app: bridle/samples/ubx_gnss
   :board: mimxrt1010_evk
   :build-dir: mimxrt1010_evk-ubx_gnss
   :gen-args: -DCONFIG_LOG=n
   :west-args: -p -S usb-console
   :flash-args: -r pyocd
   :goals: flash
   :compact:

It is more luck than sense that this example works on this extremely poorly
equipped board. The word *"works"* should also not be overrated. This board
requires special care when using and maintaining the code base.

   .. admonition:: Insufficient UART interfaces
      :class: danger

      First of all, there is a lack of sufficient UART interfaces. The
      user must decide whether he wants to use the one available LPUART1
      as a console via the on-board debug adapter (the factory default)
      or whether he needs it for his own purposes on the Arduino edge
      connector. For this example, the later is the case and it is
      extremely important that the two jumpers **JP31** for TX and
      **JP32** for RX are removed so that there is no longer an active
      connection to the on-board debug adapter (isolation). This also
      removes the channel for the standard console and the on-board USB
      device at **J9** must be used as an alternative. This in turn means
      that Zephyr needs the USB device software stack with the USB-CDC/ACM
      class driver for VCOM access to the shell enabled.

      **Note:** the :program:`west build` parameter :code:`-S usb-console`.

   .. admonition:: Low on-board memory
      :class: warning

      The :file:`ubxlib` software stack **is extremely memory-intensive**
      and **requires at least 16 kB RAM for the memory heap**
      (:kconfig:option:`CONFIG_HEAP_MEM_POOL_SIZE`). That alone is already
      25% of the available RAM in this system. Together with the necessary
      USB device software stack and the USB-CDC/ACM class driver, there is
      hardly anything left for additional functions. This means that the
      **Zephyr shell** can only be **used in the absolute minimum
      configuration** (:kconfig:option:`CONFIG_SHELL_MINIMAL`\ :code:`=y`)
      and the **Zephyr logging system must be omitted completely**
      (:kconfig:option:`CONFIG_LOG`\ :code:`=n`).

      **Note:** the :program:`CMake` parameter :code:`-DCONFIG_LOG=n` must
      be considered for this when calling :program:`west build`.

   .. admonition:: Disabled runtime stacks
      :class: note

      As a result of the limited memory capacity, important other runtime
      stacks must also be reduced. That are in summary:

      .. list-table::
         :align: center
         :width: 75%
         :widths: 50, 50
         :header-rows: 1

         * - Board specific configuration
           - Context and meaning

         * - .. literalinclude:: boards/mimxrt1010_evk.conf
                :caption: boards/mimxrt1010_evk.conf
                :language: cfg
                :encoding: ISO-8859-1
                :start-after: # zephyr-keep-sorted-start
                :end-before: # zephyr-keep-sorted-stop

           - :Dynamic Memory Pool:
                | left on :bgn:`16384`
                | (:kconfig:option:`CONFIG_HEAP_MEM_POOL_SIZE`)

             :Main Context:
                | from :ign:`4096` to :brd:`3456`
                | (:kconfig:option:`CONFIG_MAIN_STACK_SIZE`)

             :Interrupt Serive Routines:
                | from :ign:`2048` to :brd:`1024`
                | (:kconfig:option:`CONFIG_ISR_STACK_SIZE`)

             :System Worker Queue:
                | from :ign:`1024` to :brd:`512`
                | (:kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`)

             :USB-CDC/ACM Worker Queue:
                | from :ign:`1024` to :brd:`512`
                | (:kconfig:option:`CONFIG_USB_WORKQUEUE_STACK_SIZE`)

             :USB-CDC/ACM Ring Buffer:
                | from :ign:`1024` to :brd:`512`
                | (:kconfig:option:`CONFIG_USB_CDC_ACM_RINGBUF_SIZE`)

      With this :u:`heuristically determined memory configuration`, the main
      functions of this *"simple"* example can be used. One exception is the
      shell command :console:`gnss single`. The subsequent function call stack
      may grow to a point where the reduced ISR or main stack overflows and,
      in the absence of further Zephyr functionality, the CPU simply stops
      in a :u:`critical exception – with no visible notification to the user`.
      This is a very dynamic effect and difficult to predict, **but it happens
      very often**.

Example console session
=======================

After power-on or hard reset, the GNSS module will be initialized
automatically. There is a simple Shell command for some standard
evaluation steps:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* \*\*\*
      [00:00:02.021,000] <inf> main: GNSS Device is ready!

      :bgn:`uart:~$` **gnss -h**
      gnss - GNSS related commands
      Subcommands:
        single  :Get a one-shot position estimate
        stream  :Start or stop streaming of position estimates
        reset   :Reset GNSS module
        ttff    :Measure TTFF

.. rubric:: Reset GNSS module:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **gnss reset**

The on-module LED for PPS signaling goes off and comes back to blink
after TTFF.

.. rubric:: Measure TTFF:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **gnss ttff**
      Run 1 of 1: Acquired fix after 32.26s
      ---------------
      Avg. TTFF: 32.26

The on-module LED for PPS signaling goes off and comes back to blink
after TTFF.

It is also possible to run several TTFF measurements sequentially. If
there is also a good receiving range and a reliable position already
exists, the TTFF will be correspondingly low:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **gnss ttff 10**
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

.. rubric:: Get a one-shot position estimate:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **gnss single**
      Found position estimate after 0.8s: (lat, lon): (50.922432, 11.600015), alt: 192.05m, radius: 1.48m (15 SV used)

.. rubric:: Start or stop streaming of position estimates:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **gnss stream start**
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

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **gnss stream stop**
      [00:01:28.905,000] <inf> main: Found position estimate: (lat, lon): (50.922470, 11.599995), alt: 192.22m, radius: 1.50m (18 SV used)
      [00:01:29.709,000] <inf> main: Found position estimate: (lat, lon): (50.922470, 11.599994), alt: 192.12m, radius: 1.50m (18 SV used)

References
**********

.. target-notes::

.. _`u-blox M10 device`: https://www.u-blox.com/en/product/ubx-m10050-chip
.. _`SparkFun MAX-M10S Breakout`: https://www.sparkfun.com/products/18037
