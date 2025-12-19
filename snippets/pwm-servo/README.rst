.. _snippet-pwm-servo:

PWM Servomotor Preset Snippet (pwm-servo)
#########################################

.. code-block:: console

   west build -S pwm-servo [...]

Overview
********

This snippet is quite board specific and prepares a dedicated PWM channel
exclusively for the standard :zephyr:code-sample:`servo-motor` sample from
Zephyr.

Board specific setups
=====================

Only selected boards are supported by this snippet. There is no basic
configuration.

Supported boards are:

.. zephyr-keep-sorted-start re(^\* .\w)

* Cytron |Maker Pi RP2040|
* |TiaC CoffeeCaller nRF52|

.. zephyr-keep-sorted-stop

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Cytron Maker Pi RP2040

      .. _snippet-pwm-servo-cytron-maker-pi-rp2040:

      Connect a servomotor :hwftlbl-act:`MG996R` to the first on-board PWM channel for servomotors, the 4×3 pin header block at position 19. See the board :ref:`positions diagram <cytron_maker_pi_rp2040_positions>` for details.

      The corresponding PWM pulse widths for a range of :b:`-90°` to :b:`+90°` (180°) are :bbl:`500 ㎲` to :bbl:`2,500 ㎲` with a :bbl:`period of 50 ㎐`. All these servomotor specific parameters are preset by the snippet :ref:`snippet-pwm-servo` that have to use to get access to this dedicated PWM channel together with the original Zephyr :zephyr:code-sample:`servo-motor` sample. Invoke :program:`west build` and :program:`west flash` with this snipped and optional mixed with others, for example:

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/servo_motor
         :build-dir: cytron_maker_rp2040
         :board: cytron_maker_pi_rp2040
         :snippets: "usb-console pwm-servo"
         :west-args: -p always
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. literalinclude:: boards/cytron_maker_pi_rp2040.overlay
         :caption: boards/cytron_maker_pi_rp2040.overlay
         :language: DTS
         :encoding: ISO-8859-1
         :emphasize-lines: 3-4
         :linenos:
         :start-at: servo:
         :end-at: };

   .. group-tab:: TiaC CoffeeCaller nRF52

      .. _snippet-pwm-servo-tiac-coffeecaller-nrf52:

      Connect a servomotor :hwftlbl-act:`MG996R` to the first on-board PWM channel for servomotors, the 4×3 pin header block (HDR1 and HDR2).

      The corresponding PWM pulse widths for a range of :b:`-90°` to :b:`+90°` (180°) are :bbl:`500 ㎲` to :bbl:`2,500 ㎲` with a :bbl:`period of 50 ㎐`. All these servomotor specific parameters are preset by the snippet :ref:`snippet-pwm-servo` that have to use to get access to this dedicated PWM channel together with the original Zephyr :zephyr:code-sample:`servo-motor` sample. Invoke :program:`west build` and :program:`west flash` with this snipped and optional mixed with others, for example:

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/servo_motor
         :build-dir: coffeecaller_nrf52
         :board: coffeecaller_nrf52/nrf52840
         :snippets: "pwm-servo"
         :west-args: -p always
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. literalinclude:: boards/coffeecaller_nrf52.overlay
         :caption: boards/coffeecaller_nrf52.overlay
         :language: DTS
         :encoding: ISO-8859-1
         :emphasize-lines: 3-4
         :linenos:
         :start-at: servo:
         :end-at: };

   .. zephyr-keep-sorted-stop

How to add support of a new board
*********************************

* add board devicetree overlay to this snippet;
* which add following options to the dedicated PWM node:

  - :dts:`compatible = "pwm-servo";`
  - :dts:`min-pulse = <PWM_USEC(500)>;`
  - :dts:`max-pulse = <PWM_USEC(2500)>;`
