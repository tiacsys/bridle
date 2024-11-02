.. _snippet-samples-sensor-bme280-tweaks:

BME280 Sensor Sample Tweaks (samples-sensor-bme280-tweaks)
##########################################################

.. code-block:: console

   west build -S samples-sensor-bme280-tweaks [...]

Overview
********

Unfortunately, the example for the :zephyr:code-sample:`bme280` from the Zephyr
upstream repository binds such a sensor hard to the SPI bus regardless of board
and shield variations, although the |zephyr:board:rpi_pico| board has no such
sensor available. Thus, no matter what you try to change via shields, a BME280
sensor is always defined and activated on the SPI bus as soon as the board name
is set to :code:`rpi_pico`.

This tweak snippet now always deletes such an entry and should only be used
exclusively for the standard :zephyr:code-sample:`bme280` sample from Zephyr.

Board specific setups
=====================

Only selected boards are supported by this snippet. There is no basic
configuration.

Supported boards are:

* |zephyr:board:rpi_pico|

Raspberry Pi Pico
-----------------

.. _snippet-samples-sensor-bme280-tweaks-rpi-pico:

.. zephyr-app-commands::
   :app: zephyr/samples/sensor/bme280
   :board: rpi_pico
   :build-dir: rpi_pico
   :west-args: -p -S usb-console -S samples-sensor-bme280-tweaks
   :flash-args: -r uf2
   :goals: flash
   :compact:

.. literalinclude:: boards/rpi_pico.overlay
   :caption: boards/rpi_pico.overlay
   :language: DTS
   :encoding: ISO-8859-1
   :emphasize-lines: 2-3
   :linenos:
   :start-at: &spi0 {
   :end-at: };

How to add support of a new board
*********************************

* add board devicetree overlay to this snippet;
* which add the needed tweaks
