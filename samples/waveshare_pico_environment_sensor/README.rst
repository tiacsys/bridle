.. _waveshare_pico_environment_sensor_sample:


Waveshare Pico Environment Sensor Sample
########################################

- THP: BME280, I2C temperature, humidity and air pressure sensor
- VOC: SGP40, I2C digital multipixel gas sensor
- DOF: ICM-20948 (MPU-9250), I2C accelerometer, gyroscope and magnetometer

Description
***********

This sample application periodically measures the ambient temperature, humidity
and air pressure from the THP device, a raw gas sensor value from the VOC device
and the chip temperature, acceleration, angular velocity and the terrestrial
magnetism in all XYZ spatial coordinates from the DOF device. The result is
written to the console along with the time since startup.

You can choose to use the on-chip T/RH compensation of the SGP40 by feeding the
values measured by the BME280 into it. This is enabled in the Application by
default, you can turn it off by setting :code:`APP_USE_COMPENSATION=n`.

References
**********

- `BME280 sensor <BME280_>`_ (`BME280 Datasheet`_)
- `SGP40 sensor <SGP40_>`_ (`SGP40 Datasheet`_)
- `ICM-20948 sensor <ICM-20948_>`_
  (`ICM-20948 Datasheet`_, `ICM-20948 Software User Guide`_)

  - `AK09916 sensor <AK09916>`_ (`AK09916 Datasheet`_)

- `MPU-9250 sensor <MPU-9250_>`_
  (`MPU-9250 Datasheet`_, `MPU-9250 Register Map`_)

  - `AK8963 sensor <AK8963>`_ (`AK8963 Datasheet`_)

Wiring
******

This sample uses all sensors controlled by using the I2C interface.

- connect supply: :strong:`VDD`, :strong:`GND`
- and interface: :strong:`SDA`, :strong:`SCL`.

The supply voltage can be in the 1.7V to 3.6V range. Depending on the baseboard
used, the :strong:`SDA` and :strong:`SCL` lines require Pull-Up resistors.

Building and Running
********************

This project outputs sensor data to the console. It requires a BME280, a SGP40
and a ICM-20948 (MPU-9250) sensor. It should work with any platform featuring
a I2C peripheral interface. This example is usable with the Devicetree overlay
that comes with the :ref:`waveshare_pico_environment_sensor` shield for the
:ref:`zephyr:rpi_pico` board.

.. zephyr-app-commands::
   :app: bridle/samples/waveshare_pico_environment_sensor
   :board: rpi_pico
   :shield: waveshare_pico_environment_sensor
   :flash-args: -r uf2
   :goals: build flash

Sample Output
=============

.. code-block:: console

   [00:00:00.001,000] <dbg> BME280: bme280_chip_init: ID OK
   [00:00:00.009,000] <dbg> BME280: bme280_chip_init: "bme280@76" OK
   [00:00:00.074,000] <dbg> MPU9250: ak8963_fetch_adj: Adjustment values 1774 1774 1709
   [00:00:00.335,000] <dbg> SGP40: sgp40_init: Selftest succeeded!
   *** Booting Zephyr OS build … … … ***
   [00:00:04.337,000] <inf> wpes_sample: ICM20948: Found device "mpu9250@68", getting sensor data
   [00:00:04.337,000] <inf> wpes_sample: BME280: Found device "bme280@76", getting sensor data
   [00:00:04.337,000] <inf> wpes_sample: SGP40: Found device "sgp40@59", getting sensor data
   [00:00:06.339,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   NOW: 00:00:06.375
   DOF: 31.55 Temp. [C] ; -0.111929 -0.207697 -9.982026 XYZ-Accel. [m/s/s] ; 0.011591 -0.002664 0.020517 XYZ-Gyro. [rad/s] ; 0.042576 0.954412 -1.001474 XYZ-Magn. [uG]
   THP: 29.03 Temp. [C] ; 34.301 RH [%] ; 100.85 AirPr. [hPa]
   VOC: 0 Gas [a.u.]
   [00:00:08.378,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   NOW: 00:00:08.414
   DOF: 31.59 Temp. [C] ; -0.113127 -0.204106 -9.987413 XYZ-Accel. [m/s/s] ; 0.011724 -0.001998 0.021716 XYZ-Gyro. [rad/s] ; 0.012418 0.952638 -0.989511 XYZ-Magn. [uG]
   THP: 29.04 Temp. [C] ; 34.188 RH [%] ; 100.85 AirPr. [hPa]
   VOC: 29909 Gas [a.u.]
   [00:00:10.417,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   NOW: 00:00:10.456
   DOF: 31.62 Temp. [C] ; -0.116718 -0.217274 -9.989208 XYZ-Accel. [m/s/s] ; 0.011724 -0.002531 0.021716 XYZ-Gyro. [rad/s] ; 0.035480 0.950864 -0.994638 XYZ-Magn. [uG]
   THP: 29.06 Temp. [C] ; 34.075 RH [%] ; 100.85 AirPr. [hPa]
   VOC: 30413 Gas [a.u.]

The `SGP40 Datasheet`_ states that the raw sensor signal for the SGP40 is
proportional to the logarithm of the sensors resistance, hence the VOC Gas
value is labeled as [a.u.] (arbitrary units) in the example.
