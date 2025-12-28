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
          :emphasize-lines: 3,5
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
          :emphasize-lines: 3,5
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
          :emphasize-lines: 3,5
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
          :emphasize-lines: 3-4,7-8
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

   .. zephyr-keep-sorted-start re(^\s{9}\.\. group-tab:: \w)

   .. group-tab:: Raspberry Pi Pico

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: rpi_pico
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. include:: helloshell.rsti

   .. group-tab:: Raspberry Pi Pico 2

      .. rubric:: On ARM Cortex-M33

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: rpi_pico2/rp2350a/m33
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. rubric:: On Hazard3 RISC-V (RV32IMAC+)

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: rpi_pico2/rp2350a/hazard3
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. include:: helloshell.rsti

   .. group-tab:: Raspberry Pi Pico 2W

      .. rubric:: On ARM Cortex-M33

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: rpi_pico2/rp2350a/m33/w
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console wifi-ip"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. include:: helloshell.rsti

   .. group-tab:: Raspberry Pi Pico W

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: rpi_pico/rp2040/w
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console wifi-ip"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. include:: helloshell.rsti

   .. group-tab:: Waveshare RP2040-LCD-0.96

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2040_lcd_0_96
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. include:: helloshell.rsti

   .. group-tab:: Waveshare RP2040-Plus

      .. rubric:: on standard ``4㎆`` revision

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2040_plus
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. rubric:: on extended ``16㎆`` revision

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2040_plus@16mb
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. include:: helloshell.rsti

   .. group-tab:: Waveshare RP2350-CAN

      .. rubric:: On ARM Cortex-M33

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2350_can/rp2350a/m33
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. rubric:: On Hazard3 RISC-V (RV32IMAC+)

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_environment_sensor-helloshell
         :board: waveshare_rp2350_can/rp2350a/hazard3
         :shield: "waveshare_pico_environment_sensor"
         :snippets: "usb-console"
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash

      .. include:: helloshell.rsti

   .. zephyr-keep-sorted-stop

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
   :shield: "waveshare_pico_environment_sensor"
   :snippets: "usb-console samples-sensor-bme280-tweaks"
   :west-args: -p
   :flash-args: -r uf2
   :goals: flash

The Default Shield Sample
=========================

See also :ref:`waveshare_pico_environment_sensor-sample` in Bridle.

.. zephyr-app-commands::
   :app: bridle/samples/waveshare_pico_environment_sensor
   :build-dir: waveshare_pico_environment_sensor
   :board: rpi_pico
   :shield: "waveshare_pico_environment_sensor"
   :snippets: "usb-console"
   :west-args: -p
   :flash-args: -r uf2
   :goals: flash

.. rubric:: Startup logging output on target

.. container:: highlight highlight-console notranslate no-copybutton

   .. parsed-literal::

      [00:00:00.003,000] <dbg> BME280: bme280_chip_init: ID OK
      [00:00:00.009,000] <dbg> BME280: bme280_chip_init: "bme280\ @\ 76" OK
      [00:00:00.259,000] <dbg> SGP40: sgp40_init: Selftest succeeded!
      [00:00:00.322,000] <dbg> MPU9250: ak8963_fetch_adj: Adjustment values 1774 1774 1709
      \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…*\*\*\*
      [00:00:00.333,000] <inf> wspes_sample: ICM20948: Found device "mpu9250\ @\ 68", getting sensor data
      [00:00:00.334,000] <inf> wspes_sample: BME280: Found device "bme280\ @\ 76", getting sensor data
      [00:00:00.334,000] <inf> wspes_sample: SGP40: Found device "sgp40\ @\ 59", getting sensor data
      [00:00:02.335,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
      [00:00:02.367,000] <inf> wspes_sample: DOF: -0.020351 0.013766 -9.950303 XYZ-Accel. [m/s/s]
      [00:00:02.367,000] <inf> wspes_sample: DOF: 0.025047 -0.002531 -0.003863 XYZ-Gyro. [rad/s]
      [00:00:02.367,000] <inf> wspes_sample: DOF: -0.106440 0.943768 -0.690436 XYZ-Magn. [uG]
      [00:00:02.367,000] <inf> wspes_sample: DOF: 30.04 Temp. [C]
      [00:00:02.367,000] <inf> wspes_sample: THP: 99.35 AirPr. [hPa]
      [00:00:02.367,000] <inf> wspes_sample: THP: 27.59 Temp. [C]
      [00:00:02.367,000] <inf> wspes_sample: THP: 46.418 RH [%]
      [00:00:02.367,000] <inf> wspes_sample: VOC: 6 Gas [a.u.]
      [00:00:04.368,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
      [00:00:04.400,000] <inf> wspes_sample: DOF: -0.016161 0.011971 -9.961077 XYZ-Accel. [m/s/s]
      [00:00:04.400,000] <inf> wspes_sample: DOF: 0.025180 -0.002131 -0.005062 XYZ-Gyro. [rad/s]
      [00:00:04.400,000] <inf> wspes_sample: DOF: -0.108214 0.934898 -0.681891 XYZ-Magn. [uG]
      [00:00:04.400,000] <inf> wspes_sample: DOF: 30.22 Temp. [C]
      [00:00:04.400,000] <inf> wspes_sample: THP: 99.35 AirPr. [hPa]
      [00:00:04.400,000] <inf> wspes_sample: THP: 27.59 Temp. [C]
      [00:00:04.400,000] <inf> wspes_sample: THP: 46.446 RH [%]
      [00:00:04.400,000] <inf> wspes_sample: VOC: 27835 Gas [a.u.]
      [00:00:06.401,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
      [00:00:06.433,000] <inf> wspes_sample: DOF: -0.023943 0.011971 -9.960478 XYZ-Accel. [m/s/s]
      [00:00:06.433,000] <inf> wspes_sample: DOF: 0.024647 -0.001598 -0.004796 XYZ-Gyro. [rad/s]
      [00:00:06.433,000] <inf> wspes_sample: DOF: -0.102892 0.947316 -0.680182 XYZ-Magn. [uG]
      [00:00:06.433,000] <inf> wspes_sample: DOF: 30.31 Temp. [C]
      [00:00:06.433,000] <inf> wspes_sample: THP: 99.35 AirPr. [hPa]
      [00:00:06.433,000] <inf> wspes_sample: THP: 27.59 Temp. [C]
      [00:00:06.433,000] <inf> wspes_sample: THP: 46.348 RH [%]
      [00:00:06.433,000] <inf> wspes_sample: VOC: 28379 Gas [a.u.]
      … … …

References
**********

.. target-notes::
