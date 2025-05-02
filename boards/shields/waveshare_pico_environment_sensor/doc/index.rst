.. _waveshare_pico_environment_sensor:

Waveshare Pico Environment Sensor
#################################

The `Waveshare Pico Environment Sensor`_ shield is a :bbk:`pico sized` multi
sensor module designed for the |zephyr:board:rpi_pico| and gives the ability
to collect environmental data like temperature & humidity, air pressure,
ambient light intensity, VOC, UV rays, etc. It can also be used to build
a robot that can detect motion and orientation. It communicates with the
Raspberry Pi Pico over I2C.

Board Overview
**************

Hardware
========

.. include:: hardware.rsti

Positions
=========

.. include:: positions.rsti

Pinouts
=======

.. include:: pinouts.rsti

Components
==========

.. list-table::
   :align: center
   :width: 100%
   :widths: 33, 33, 33

   * - .. rubric:: `BME280`_
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Measuring:
          temperature, humidity and air pressure (THP).
       Temperature range:
          -40~+85℃ (resolution is 0.01°C, error ±1℃)
          @ :bbl:`3.3V/~0.350㎃`
       Humidity range:
          0~100%RH (resolution is 0.008%RH, error ±3%RH)
          @ :bbl:`3.3V/~0.340㎃`
       Pressure range:
          300~1100㍱ (resolution is 0.18㍱, error ±1㍱)
          @ :bbl:`3.3V/~0.714㎃`

     - |nbsp|
     - .. literalinclude:: ../boards/rpipico_r3.dtsi
          :caption: BME280 in boards/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :dedent: 1
          :emphasize-lines: 3-4
          :linenos:
          :start-at: wspes_sens_thp: bme280@76 {
          :end-at: };

       - Sensor I2C address: :code:`0x76`
       - Devicetree compatible: :dtcompatible:`bosch,bme280`

   * - .. rubric:: `SGP40`_
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Measuring:
          air quality, Volatile Organic Compounds (VOC)
          with on-chip humidity compensation support.
       Measuring range:
          0~1000 ㏙ ethanol equivalent
          @ :bbl:`3.3V/~2.6㎃`
       Limit condition:
          < 0.05 ㏙ ethanol equivalent OR
          < 10% preset concentration point (the larger one should prevail)
       Response time:
          < 10s (𝜏 63%)
       Start time:
          < 60s

     - |nbsp|
     - .. literalinclude:: ../boards/rpipico_r3.dtsi
          :caption: SGP40 in boards/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :dedent: 1
          :emphasize-lines: 3-4
          :linenos:
          :start-at: wspes_sens_voc: sgp40@59 {
          :end-at: };

       - Sensor I2C address: :code:`0x59`
       - Devicetree compatible: :dtcompatible:`sensirion,sgp40`

   * - .. rubric:: `TSL25911`_
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Measuring:
          ambient IR and visible light (ALS).
       Effective range:
          0~88000 ㏓
          @ :bbl:`3.3V/~3.9㎃`

     - |nbsp|
     - :brd:`NOT YET SUPPORTED`, because of missing driver

       - Sensor I2C address: :code:`0x29`
       - Devicetree compatible: :dtcompatible:`ams,tsl2591`

   * - .. rubric:: `LTR-390UV-01`_
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Measuring:
          ambient ultraviolet (UV) light (UVS).
       Response wavelength:
          280~430㎚
          @ :bbl:`3.3V/~0.3㎃`

     - |nbsp|
     - :brd:`NOT YET SUPPORTED`, because of missing driver

       - Sensor I2C address: :code:`0x53`
       - Devicetree compatible: :dtcompatible:`ltr,390uv-01`

   * - .. rubric:: `ICM-20948`_ with `AK09916`_ (`MPU-9250`_ with `AK8963`_)
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Measuring:
          motion and acceleration (9-DOF) with 3-axis accelerometer,
          3-axis gyroscope and 3-axis magnetometer (compass). Also
          measuring the internal chip temperature.
       Accelerometer resolution:
          16-bit
       Accelerometer range (configurable):
          acceleration: ±2, ±4, ±8, ±16g
          @ :bbl:`1.8V/~0.069㎃`
       Gyroscope resolution:
          16-bit
       Gyroscope range (configurable):
          angular velocity: ±250, ±500, ±1000, ±2000°/ₛ
          @ :bbl:`1.8V/~1.230㎃`
       Magnetometer resolution:
          16-bit
       Magnetometer range:
          flux: ±4900µT (±4800µT)
          @ :bbl:`1.8V/~0.090㎃`
       Temperature range:
          -40~+85℃ (resolution is 0.05°C, error ±3%)
          @ :bbl:`1.8V/~1.720㎃`

     - Accelerometer:
           - full scale (range) set to :bbl:`±2g`
           - digital low pass filter set to :bbl:`fₘ=5.05㎐`
           - 3㏈ with 32.48㎳ delay at sample rate fₛ=1㎑
       Gyroscope:
           - full scale (range) set to :bbl:`±250°/ₛ`
           - digital low pass filter set to :bbl:`fₘ=5㎐`
           - 3㏈ with 33.48㎳ delay at sample rate fₛ=1㎑
       Magnetometer:
           - yielding factor on-chip is :bbl:`0.14997558` (4912µT/32752µT⁻¹)
           - Zephyr unit is Gauss (10⁴T), so the sbsolute yielding factor
             for Zephyr sensor API is hard set to :bbl:`1499`
       Sample rate:
           - fₛ=1㎑ scaled by 1/(1+\ :bbl:`9`\ ) and set to :bbl:`fₛₒ=100㎐`

     - :bbl:`INTERIME SUPPORT`, because of obsolete component

       .. literalinclude:: ../boards/rpipico_r3.dtsi
          :caption: MPU-9250 in boards/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :dedent: 1
          :emphasize-lines: 3-4
          :linenos:
          :start-at: wspes_sens_dof: mpu9250@68 {
          :end-at: };

       .. literalinclude:: ../waveshare_pico_environment_sensor.conf
          :caption: MPU-9250 in waveshare_pico_environment_sensor.conf
          :language: cfg
          :encoding: ISO-8859-1
          :linenos:
          :start-at: CONFIG_MPU9250_TRIGGER_NONE=
          :end-at: CONFIG_MPU9250_TRIGGER_NONE=

       - Sensor I2C address: :code:`0x68`
       - Devicetree compatible: :dtcompatible:`invensense,mpu9250`

       :brd:`NOT YET SUPPORTED`, because of missing driver

       - Devicetree compatible: :dtcompatible:`invensense,icm20948`

   * - .. rubric:: `RT9193-33`_ and `RT9193-18`_
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Ultra-low noise, ultra-fast CMOS LDO regulator for 3.3V and 1.8V

       - Low Dropout of 220㎷ @ 300㎃
       - Standby current < 0.01μA when shutdown
       - Quick start-up (typically 50㎲)
       - Output voltage accuracy ±2%
       - Up to 300㎃ max output current
       - Output current limit protection at 360~400㎃
       - Thermal limit protection at 165°C

     - |nbsp|
     - |nbsp|

Utilization
***********

Sensing Subsystem
=================

The shield is ready for using with the Zephyr :external+zephyr:ref:`sensing`.
The interface is disabled for default and can be enabled by an application
overlay :file:`app.overlay` (see :external+zephyr:ref:`application`).

.. list-table::
   :align: center
   :width: 100%
   :widths: 50, 50

   * - .. rubric:: Sensing Interface on Shield Level
     - .. rubric:: Overlay Content on Application Level

   * - .. literalinclude:: ../waveshare_pico_environment_sensor.overlay
          :caption: Sensing Interface in waveshare_pico_environment_sensor.overlay
          :language: DTS
          :encoding: ISO-8859-1
          :tab-width: 4
          :emphasize-lines: 3-4,7-9
          :linenos:
          :prepend: / {
          :start-at: wspes_sensing: wspes-sensing {

     - - for the interface:
            :dts:`&wspes_sensing { status = "okay"; };`
       - for the accelerometer sensor:
            :dts:`&wspes_accel { status = "okay"; };`

Programming
===========

Set ``-DSHIELD=waveshare_pico_environment_sensor`` when you invoke
``west build`` or ``cmake`` in your Zephyr application. For example:

.. tabs::

   .. group-tab:: Raspberry Pi Pico

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: rpi_pico
         :shield: waveshare_pico_environment_sensor
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

   .. group-tab:: Raspberry Pi Pico W

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: rpi_pico/rp2040/w
         :shield: waveshare_pico_environment_sensor
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

   .. group-tab:: Waveshare RP2040-LCD-0.96

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2040_lcd_0_96
         :shield: waveshare_pico_environment_sensor
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

   .. group-tab:: Waveshare RP2040-Plus

      .. rubric:: on standard ``4㎆`` revision

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2040_plus
         :shield: waveshare_pico_environment_sensor
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. rubric:: on extended ``16㎆`` revision

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2040_plus@16mb
         :shield: waveshare_pico_environment_sensor
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

More Samples
************

BME280 Humidity and Pressure Sensor
===================================

This sample shows how to use the :external+zephyr:ref:`Sensors API <sensor>`
driver for the Bosch BME280 environmental sensor. See also Zephyr sample:
:external+zephyr:zephyr:code-sample:`bme280` and
:ref:`snippet-samples-sensor-bme280-tweaks`.

.. zephyr-app-commands::
   :app: zephyr/samples/sensor/bme280
   :build-dir: waveshare_pico_environment_sensor-bme280
   :board: rpi_pico
   :shield: waveshare_pico_environment_sensor
   :goals: flash
   :west-args: -p -S usb-console -S samples-sensor-bme280-tweaks
   :flash-args: -r uf2

The Default Shield Sample
=========================

See also :ref:`waveshare_pico_environment_sensor-sample` in Bridle.

.. zephyr-app-commands::
   :app: bridle/samples/waveshare_pico_environment_sensor
   :build-dir: waveshare_pico_environment_sensor
   :board: rpi_pico
   :shield: waveshare_pico_environment_sensor
   :goals: flash
   :west-args: -p -S usb-console
   :flash-args: -r uf2

References
**********

.. target-notes::
