.. _x_grove_testbed_shield:

Grove wiring for tests
######################

Overview
********

This shield is less a plug-on module in the conventional sense than more
a wiring for interconnection of certain signals. It can be used to run most
samples from Zephyr  and Bridle that require special ``aliases`` or ``chosen``
entries on device tree level or other specific Kconfig setups.

Requirements
************

This shield requires a board, maybe with additional connected shields, which
provides a configuration that allows:

- one of |LED Shields| for digital data output line, optional with PWM
- one of |Button Shields| for digital data input line

When the board is not equipped with the required shield connectors, but
instead an |Arduino R3| header, then the |Base Shield V2| can be plugged
in between.

.. note::
   Sometimes boards declare standard headers like |Arduino R3| but not define
   all connections. Make sure that the board you are using have all definitions
   to avoid build errors (see :ref:`shields` for more details).

Supported variations
====================

+-------------------------+-----------+--------------------+
| Modules                 | Port Type | |Base Shield V2|   |
+=========================+===========+====================+
| |LED Shields|           | |digital| | :strong:`D6` (PWM) |
+-------------------------+-----------+--------------------+
| |Buzzer Shields|        | |digital| | :strong:`D5` (PWM) |
+-------------------------+-----------+--------------------+
| |OLED Shields|          | |i2c|     | :strong:`I2C`      |
+-------------------------+-----------+--------------------+
| |Button Shields|        | |digital| | :strong:`D4`       |
+-------------------------+-----------+--------------------+
| |Potentiometer Shields| | |analog|  | :strong:`A0`       |
+-------------------------+-----------+--------------------+
| |Sound Sensor Shields|  | |analog|  | :strong:`A2`       |
+-------------------------+-----------+--------------------+
| |Light Sensor Shields|  | |analog|  | :strong:`A3`       |
+-------------------------+-----------+--------------------+
| |THEnv Sensor Shields|  | |digital| | :strong:`D3`       |
+-------------------------+-----------+--------------------+
| |AirPr Sensor Shields|  | |i2c|     | :strong:`I2C`      |
+-------------------------+-----------+--------------------+
| |Acc3Ax Sensor Shields| | |i2c|     | :strong:`I2C`      |
+-------------------------+-----------+--------------------+

.. hint::
   The |Base Shield V2| together with all the sensors and actuators can be
   easily replaced by the |Arduino Sensor Kit|_ as also done in the examples
   below.

   * Fritzing part file (Arduino Sensor Kit – Base):
     :download:`fzp/arduino_sensor_kit_base.fzpz`

.. |digital| replace:: `Grove Digital Layout`_
.. |analog| replace:: `Grove Analog Layout`_
.. |uart| replace:: `Grove UART Layout`_
.. |i2c| replace:: `Grove I2C Layout`_

.. |Base Shield V2| replace:: :ref:`grove_base_shield_v2`
.. |LED Shields| replace:: :ref:`grove_led_shield`
.. |OLED Shields| replace::
   :strikethrough:`Grove OLED Shields` :emphasis:`(not yet)`
.. |Buzzer Shields| replace::
   :strikethrough:`Grove Buzzer Shields` :emphasis:`(not yet)`
.. |Button Shields| replace:: :ref:`grove_button_shield`
.. |Potentiometer Shields| replace::
   :strikethrough:`Grove Rotary Potentiometer Shields` :emphasis:`(not yet)`
.. |Sound Sensor Shields| replace::
   :strikethrough:`Grove Sound Sensor Shields` :emphasis:`(not yet)`
.. |Light Sensor Shields| replace::
   :strikethrough:`Grove Light Sensor Shields` :emphasis:`(not yet)`
.. |THEnv Sensor Shields| replace::
   :strikethrough:`Grove Temperature & Humidity Sensor Shields` :emphasis:`(not yet)`
.. |AirPr Sensor Shields| replace::
   :strikethrough:`Grove Air Pressure Sensor Shields` :emphasis:`(not yet)`
.. |Acc3Ax Sensor Shields| replace::
   :strikethrough:`Grove 3-Axis Accelerator Sensor Shields` :emphasis:`(not yet)`

.. |Arduino R3| replace::
   :ref:`Arduino R3 <devicetree:dtbinding_arduino_header_r3>`

.. |Arduino Sensor Kit| replace:: :strong:`Arduino Sensor Kit – Base`
.. _`Arduino Sensor Kit`:
   https://www.seeedstudio.com/Arduino-Sensor-Kit-Base-p-4743.html

Wiring Schematics
*****************

* Fritzing project file: :download:`x_grove_testbed.fzz`

.. image:: img/x_grove_testbed_bb.svg
   :alt: Common Wiring Schematics
   :align: center

* Fritzing part file (Grove Base Shield – V2): :download:`fzp/grove_base_shield_v2.fzpz`
* Fritzing part file (Grove LED Socket Kit): :download:`fzp/grove_led_socket_kit.fzpz`
* Fritzing part file (Grove Button): :download:`fzp/grove_button.fzpz`

Build and Programming
*********************

Set ``-DSHIELD=<shield designation>`` when you invoke ``west build``.
For example:

.. zephyr-app-commands::
   :app: <sample_folder>
   :build-dir: <sample_name>-x_grove_testbed
   :board: <board_name>
   :shield: "<shield_name_with_grove_connectors> grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
   :goals: build flash
   :west-args: -p always
   :host-os: unix
   :tool: all

.. tabs::

   .. group-tab:: STMicroelectronics

      .. tabs::

         .. group-tab:: ST Nucleo F303RE

            This is based on the Zephyr board :ref:`nucleo_f303re_board`.

            * Diagrams.Net project file: :download:`x_grove_testbed.drawio`

            .. image:: img/x_grove_testbed_stmb1136_bb.svg
               :alt: ST Nucleo F303RE Wiring Schematics
               :align: center

            .. tabs::

               .. group-tab:: LED Blinky

                  This is based on the Zephyr sample :ref:`blinky-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/blinky
                     :build-dir: blinky-nucleo_f303re-x_grove_testbed
                     :board: nucleo_f303re
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Fade

                  This is based on the Zephyr sample :ref:`fade-led-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/fade_led
                     :build-dir: fade-nucleo_f303re-x_grove_testbed
                     :board: nucleo_f303re
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Button

                  This is based on the Zephyr sample :ref:`button-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/button
                     :build-dir: button-nucleo_f303re-x_grove_testbed
                     :board: nucleo_f303re
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

         .. group-tab:: ST Nucleo F401RE

            This is based on the Zephyr board :ref:`nucleo_f401re_board`.

            * Diagrams.Net project file: :download:`x_grove_testbed.drawio`

            .. image:: img/x_grove_testbed_stmb1136_bb.svg
               :alt: ST Nucleo F401RE Wiring Schematics
               :align: center

            .. tabs::

               .. group-tab:: LED Blinky

                  This is based on the Zephyr sample :ref:`blinky-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/blinky
                     :build-dir: blinky-nucleo_f401re-x_grove_testbed
                     :board: nucleo_f401re
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Fade

                  This is based on the Zephyr sample :ref:`fade-led-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/fade_led
                     :build-dir: fade-nucleo_f401re-x_grove_testbed
                     :board: nucleo_f401re
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Button

                  This is based on the Zephyr sample :ref:`button-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/button
                     :build-dir: button-nucleo_f401re-x_grove_testbed
                     :board: nucleo_f401re
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

         .. group-tab:: ST Nucleo F413ZH

            This is based on the Zephyr board :ref:`nucleo_f413zh_board`.

            * Diagrams.Net project file: :download:`x_grove_testbed.drawio`

            .. image:: img/x_grove_testbed_stmb1137_bb.svg
               :alt: ST Nucleo F413ZH Wiring Schematics
               :align: center

            .. tabs::

               .. group-tab:: LED Blinky

                  This is based on the Zephyr sample :ref:`blinky-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/blinky
                     :build-dir: blinky-nucleo_f413zh-x_grove_testbed
                     :board: nucleo_f413zh
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Fade

                  This is based on the Zephyr sample :ref:`fade-led-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/fade_led
                     :build-dir: fade-nucleo_f413zh-x_grove_testbed
                     :board: nucleo_f413zh
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Button

                  This is based on the Zephyr sample :ref:`button-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/button
                     :build-dir: button-nucleo_f413zh-x_grove_testbed
                     :board: nucleo_f413zh
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

         .. group-tab:: ST Nucleo F767ZI

            This is based on the Zephyr board :ref:`nucleo_f767zi_board`.

            * Diagrams.Net project file: :download:`x_grove_testbed.drawio`

            .. image:: img/x_grove_testbed_stmb1137_bb.svg
               :alt: ST Nucleo F767ZI Wiring Schematics
               :align: center

            .. tabs::

               .. group-tab:: LED Blinky

                  This is based on the Zephyr sample :ref:`blinky-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/blinky
                     :build-dir: blinky-nucleo_f767zi-x_grove_testbed
                     :board: nucleo_f767zi
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Fade

                  This is based on the Zephyr sample :ref:`fade-led-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/fade_led
                     :build-dir: fade-nucleo_f767zi-x_grove_testbed
                     :board: nucleo_f767zi
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Button

                  This is based on the Zephyr sample :ref:`button-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/button
                     :build-dir: button-nucleo_f767zi-x_grove_testbed
                     :board: nucleo_f767zi
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 grove_pwm_led_d6 x_grove_testbed"
                     :goals: build flash
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

   .. group-tab:: NXP Semiconductors

      .. tabs::

         .. group-tab:: NXP MIMXRT1010-EVK

            This is based on the Zephyr board :ref:`mimxrt1010_evk`.

            * Diagrams.Net project file: :download:`x_grove_testbed.drawio`

            .. image:: img/x_grove_testbed_mimxrt1010_evk_bb.svg
               :alt: NXP MIMXRT1010-EVK Wiring Schematics
               :align: center

            .. note::
               The :ref:`mimxrt1010_evk` doesn't provide any PWM channel on the
               |Laced Grove Signal Interface| line :strong:`D6` for the output
               of a variable average value of voltage over time to the LED. Thus
               the Zephyr sample :ref:`fade-led-sample` is not supported.

               Should it be absolutely necessary to use a PWM channel, then this
               can only be carried out in this test bed assembly on lines
               :strong:`D8` or :strong:`D9`.

            .. tabs::

               .. group-tab:: LED Blinky

                  This is based on the Zephyr sample :ref:`blinky-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/blinky
                     :build-dir: blinky-mimxrt1010_evk-x_grove_testbed
                     :board: mimxrt1010_evk
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 x_grove_testbed"
                     :goals: build flash
                     :gen-args: -DBOARD_FLASH_RUNNER=pyocd
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Button

                  This is based on the Zephyr sample :ref:`button-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/button
                     :build-dir: button-mimxrt1010_evk-x_grove_testbed
                     :board: mimxrt1010_evk
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 x_grove_testbed"
                     :goals: build flash
                     :gen-args: -DBOARD_FLASH_RUNNER=pyocd
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

         .. group-tab:: NXP MIMXRT1060-EVK(B)

            This is based on the Zephyr board :ref:`mimxrt1060_evk`.

            * Diagrams.Net project file: :download:`x_grove_testbed.drawio`

            .. image:: img/x_grove_testbed_mimxrt1060_evk_bb.svg
               :alt: NXP MIMXRT1060-EVK(B) Wiring Schematics
               :align: center

            .. note::
               The :ref:`mimxrt1060_evk` doesn't provide any PWM channel on the
               |Laced Grove Signal Interface| line :strong:`D6` for the output
               of a variable average value of voltage over time to the LED. Thus
               the Zephyr sample :ref:`fade-led-sample` is not supported.

               Should it be absolutely necessary to use a PWM channel, then this
               can only be carried out in this test bed assembly on line
               :strong:`D2`.

            .. tabs::

               .. group-tab:: LED Blinky

                  This is based on the Zephyr sample :ref:`blinky-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/blinky
                     :build-dir: blinky-mimxrt1060_evkb-x_grove_testbed
                     :board: mimxrt1060_evkb
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 x_grove_testbed"
                     :goals: build flash
                     :gen-args: -DBOARD_FLASH_RUNNER=pyocd
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Button

                  This is based on the Zephyr sample :ref:`button-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/button
                     :build-dir: button-mimxrt1060_evkb-x_grove_testbed
                     :board: mimxrt1060_evkb
                     :shield: "seeed_grove_base_v2 grove_btn_d4 grove_led_d6 x_grove_testbed"
                     :goals: build flash
                     :gen-args: -DBOARD_FLASH_RUNNER=pyocd
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

   .. group-tab:: Raspberry Pi

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            This is based on the Zephyr board :ref:`rpi_pico`.

            * Diagrams.Net project file: :download:`x_grove_testbed.drawio`

            .. image:: img/x_grove_testbed_rpi_pico_bb.svg
               :alt: Raspberry Pi Pico Wiring Schematics
               :align: center

            .. tabs::

               .. group-tab:: LED Blinky

                  This is based on the Zephyr sample :ref:`blinky-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/blinky
                     :build-dir: blinky-rpi_pico-x_grove_testbed
                     :board: rpi_pico
                     :shield: "seeed_grove_rpipico_v1 grove_btn_d16 grove_led_d18 grove_pwm_led_d18 x_grove_testbed"
                     :goals: build flash
                     :gen-args: -DBOARD_FLASH_RUNNER=openocd -DRPI_PICO_DEBUG_ADAPTER=cmsis-dap -DOPENOCD=/opt/openocd-rp2040/bin/openocd -DOPENOCD_DEFAULT_PATH=/opt/openocd-rp2040/share/openocd/scripts
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Fade

                  This is based on the Zephyr sample :ref:`fade-led-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/fade_led
                     :build-dir: fade-rpi_pico-x_grove_testbed
                     :board: rpi_pico
                     :shield: "seeed_grove_rpipico_v1 grove_btn_d16 grove_led_d18 grove_pwm_led_d18 x_grove_testbed"
                     :goals: build flash
                     :gen-args: -DBOARD_FLASH_RUNNER=openocd -DRPI_PICO_DEBUG_ADAPTER=cmsis-dap -DOPENOCD=/opt/openocd-rp2040/bin/openocd -DOPENOCD_DEFAULT_PATH=/opt/openocd-rp2040/share/openocd/scripts
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

               .. group-tab:: LED Button

                  This is based on the Zephyr sample :ref:`button-sample`.

                  .. zephyr-app-commands::
                     :app: zephyr/samples/basic/button
                     :build-dir: button-rpi_pico-x_grove_testbed
                     :board: rpi_pico
                     :shield: "seeed_grove_rpipico_v1 grove_btn_d16 grove_led_d18 grove_pwm_led_d18 x_grove_testbed"
                     :goals: build flash
                     :gen-args: -DBOARD_FLASH_RUNNER=openocd -DRPI_PICO_DEBUG_ADAPTER=cmsis-dap -DOPENOCD=/opt/openocd-rp2040/bin/openocd -DOPENOCD_DEFAULT_PATH=/opt/openocd-rp2040/share/openocd/scripts
                     :west-args: -p always
                     :host-os: unix
                     :tool: all

.. |Laced Grove Signal Interface| replace::
   :ref:`Laced Grove Signal Interface <devicetree:dtbinding_seeed_grove_laced_if>`