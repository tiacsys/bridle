.. _waveshare_pico_10dof_imu_sensor:

Waveshare Pico 10-DOF IMU Sensor
#################################

The `Waveshare Pico 10-DOF IMU Sensor`_ shield is a :bbk:`pico sized` multi
sensor module designed for the :ref:`zephyr:rpi_pico` and gives the ability
to collect environmental data like temperature and air pressure. It can also
be used to build a robot that can detect motion and orientation.
It communicates with the Raspberry Pi Pico over I2C.

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

   * - .. rubric:: `LPS22HB`_
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Measuring:
          absolute barometric air pressure with ambient temperature (TP).
       Pressure resolution:
          24-bit
       Pressure range:
          260~1260㍱ (resolution is 0.25㍱, error ±1㍱)
          @ :bbl:`3.3V/~0.012㎃`
       Temperature resolution:
          16-bit
       Temperature range:
          -40~+85℃ (resolution is 0.01°C, error ±1.5℃)

     - |nbsp|
     - .. literalinclude:: ../boards/rpipico_r3.dtsi
          :caption: LPS22HB in boards/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :dedent: 1
          :emphasize-lines: 3-4
          :linenos:
          :start-at: lps22hb@5c {
          :end-at: };

       - Sensor I2C address: :code:`0x5c`
       - Devicetree compatible: :dtcompatible:`st,lps22hb-press`

   * - .. rubric:: `MPU-9250`_ with `AK8963`_ (`ICM-20948`_ with `AK09916`_)
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
          @ :bbl:`3.3V/~0.45㎃`
       Gyroscope resolution:
          16-bit
       Gyroscope range (configurable):
          angular velocity: ±250, ±500, ±1000, ±2000°/ₛ
          @ :bbl:`3.3V/~3.20㎃`
       Magnetometer resolution:
          16-bit
       Magnetometer range:
          flux: ±4800µT (±4900µT)
          @ :bbl:`3.3V/~0.28㎃`
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
          :start-at: mpu9250@68 {
          :end-at: };

       - Sensor I2C address: :code:`0x68`
       - Devicetree compatible: :dtcompatible:`invensense,mpu9250`

       :brd:`NOT YET SUPPORTED`, because of missing driver

       - Devicetree compatible: :dtcompatible:`invensense,icm20948`

   * - .. rubric:: `RT9193-33`_ (and `RT9193-18`_)
     - .. rubric:: Default Setup
     - .. rubric:: Devicetree / Kconfig

   * - Ultra-low noise, ultra-fast CMOS LDO regulator for 3.3V

       - Low Dropout of 220㎷ @ 300㎃
       - Standby current < 0.01μA when shutdown
       - Quick start-up (typically 50㎲)
       - Output voltage accuracy ±2%
       - Up to 300㎃ max output current
       - Output current limit protection at 360~400㎃
       - Thermal limit protection at 165°C

     - |nbsp|
     - |nbsp|

Revision Distinction
====================

.. rubric:: LPS22HB

.. list-table::
   :align: center
   :width: 100%
   :widths: 50, 50

   * - .. rubric:: Revision 2.1
     - .. rubric:: Revision 1

   * - .. literalinclude:: ../boards/waveshare_pico_10dof_imu_sensor_r2/rpipico_r3.dtsi
          :caption: LPS22HB in boards/waveshare_pico_10dof_imu_sensor_r2/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 2
          :linenos:
          :start-at: &wsptdis_sens_tp {
          :end-at: };

     - .. literalinclude:: ../boards/waveshare_pico_10dof_imu_sensor_r1/rpipico_r3.dtsi
          :caption: LPS22HB in boards/waveshare_pico_10dof_imu_sensor_r1/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 2
          :linenos:
          :start-at: &wsptdis_sens_tp {
          :end-at: };

.. rubric:: MPU-9250 (ICM-20948)

.. list-table::
   :align: center
   :width: 100%
   :widths: 50, 50

   * - .. rubric:: Revision 2.1
     - .. rubric:: Revision 1

   * - .. literalinclude:: ../waveshare_pico_10dof_imu_sensor_r2.conf
          :caption: MPU-9250 in waveshare_pico_10dof_imu_sensor_r2.conf
          :language: cfg
          :encoding: ISO-8859-1
          :linenos:
          :start-at: CONFIG_MPU9250_TRIGGER_NONE=
          :end-at: CONFIG_MPU9250_TRIGGER_NONE=

       .. literalinclude:: ../boards/waveshare_pico_10dof_imu_sensor_r2/rpipico_r3.dtsi
          :caption: MPU-9250 in boards/waveshare_pico_10dof_imu_sensor_r2/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 2-3
          :linenos:
          :start-at: &wsptdis_sens_dof {
          :end-at: };

     - .. literalinclude:: ../waveshare_pico_10dof_imu_sensor_r1.conf
          :caption: MPU-9250 in waveshare_pico_10dof_imu_sensor_r1.conf
          :language: cfg
          :encoding: ISO-8859-1
          :linenos:
          :start-at: CONFIG_MPU9250_TRIGGER_NONE=
          :end-at: CONFIG_MPU9250_TRIGGER_NONE=

       .. literalinclude:: ../boards/waveshare_pico_10dof_imu_sensor_r1/rpipico_r3.dtsi
          :caption: MPU-9250 in boards/waveshare_pico_10dof_imu_sensor_r1/rpipico_r3.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 2-3
          :linenos:
          :start-at: &wsptdis_sens_dof {
          :end-at: };

       :bbl:`INTERIME SUPPORT`, because of missing correct driver for ICM-20948.

Utilization
***********

Sensing Subsystem
=================

The shield is ready for using with the Zephyr :ref:`zephyr:sensing_api`.
The interface is disabled for default and can be enabled by an application
overlay :file:`app.overlay` (see :ref:`zephyr:application`).

.. list-table::
   :align: center
   :width: 100%
   :widths: 50, 50

   * - .. rubric:: Sensing Interface on Shield Level
     - .. rubric:: Overlay Content on Application Level

   * - .. literalinclude:: ../waveshare_pico_10dof_imu_sensor.dtsi
          :caption: Sensing Interface in waveshare_pico_10dof_imu_sensor.dtsi
          :language: DTS
          :encoding: ISO-8859-1
          :tab-width: 4
          :emphasize-lines: 3-4,7-9
          :linenos:
          :prepend: / {
          :start-at: wsptdis_sensing: wsptdis-sensing {

     - - for the interface:
            :devicetree:`&wsptdis_sensing { status = "okay"; };`
       - for the accelerometer sensor:
            :devicetree:`&wsptdis_accel { status = "okay"; };`

Programming
===========

Set ``-DSHIELD=<shield_name_with_rev>`` to the right shield revision when you
invoke ``west build`` or ``cmake`` in your Zephyr application. For example:

- for :strong:`Rev2.1`: ``-DSHIELD=waveshare_pico_10dof_imu_sensor_r2``
- for :strong:`Rev1`: ``-DSHIELD=waveshare_pico_10dof_imu_sensor_r1``

The following examples use the shield in revision 2.1. If these should be used
for revision 1, the variable ``SHIELD`` must be adapted accordingly.

.. tabs::

   .. group-tab:: Raspberry Pi Pico

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_10dof_imu_sensor-helloshell
         :board: rpi_pico
         :shield: waveshare_pico_10dof_imu_sensor_r2
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

   .. group-tab:: Raspberry Pi Pico W

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_10dof_imu_sensor-helloshell
         :board: rpi_pico_w
         :shield: waveshare_pico_10dof_imu_sensor_r2
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

   .. group-tab:: Waveshare RP2040-LCD-0.96

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_10dof_imu_sensor-helloshell
         :board: waveshare_rp2040_lcd_0_96
         :shield: waveshare_pico_10dof_imu_sensor_r2
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

   .. group-tab:: Waveshare RP2040-Plus

      .. rubric:: on standard ``4㎆`` revision

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_10dof_imu_sensor-helloshell
         :board: waveshare_rp2040_plus
         :shield: waveshare_pico_10dof_imu_sensor_r2
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. rubric:: on extended ``16㎆`` revision

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :build-dir: waveshare_pico_10dof_imu_sensor-helloshell
         :board: waveshare_rp2040_plus@16mb
         :shield: waveshare_pico_10dof_imu_sensor_r2
         :goals: flash
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :tool: all

      .. include:: helloshell.rsti

More Samples
************

LPS22HB Pressure and Temperature Sensor
=======================================

This sample shows how to use the :ref:`Sensors API <zephyr:sensor_api>`
driver for the STM LPS22HB MEMS pressure sensor. See also Zephyr sample:
:ref:`zephyr:lps22hb`.

.. zephyr-app-commands::
   :app: zephyr/samples/sensor/lps22hb
   :build-dir: waveshare_pico_10dof_imu_sensor-lps22hb
   :board: rpi_pico
   :shield: waveshare_pico_10dof_imu_sensor_r2
   :goals: flash
   :west-args: -p -S usb-console
   :flash-args: -r uf2

The Default Shield Sample
=========================

See also :ref:`waveshare_pico_10dof_imu_sensor_sample` in Bridle.

.. zephyr-app-commands::
   :app: bridle/samples/waveshare_pico_10dof_imu_sensor
   :build-dir: waveshare_pico_10dof_imu_sensor
   :board: rpi_pico
   :shield: waveshare_pico_10dof_imu_sensor_r2
   :goals: flash
   :west-args: -p -S usb-console
   :flash-args: -r uf2

References
**********

.. target-notes::
