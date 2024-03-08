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
   :build-dir: waveshare_pico_environment_sensor
   :west-args: -p -S usb-console
   :flash-args: -r uf2
   :goals: flash

Sample Output
=============

.. code-block:: kmsg

   [00:00:00.001,000] <dbg> BME280: bme280_chip_init: ID OK
   [00:00:00.009,000] <dbg> BME280: bme280_chip_init: "bme280@76" OK
   [00:00:00.084,000] <dbg> MPU9250: ak8963_fetch_adj: Adjustment values 1774 1774 1709
   [00:00:00.345,000] <dbg> SGP40: sgp40_init: Selftest succeeded!
   *** Booting Zephyr OS build … … … ***
   [00:00:04.347,000] <inf> wspes_sample: ICM20948: Found device "mpu9250@68", getting sensor data
   [00:00:04.347,000] <inf> wspes_sample: BME280: Found device "bme280@76", getting sensor data
   [00:00:04.347,000] <inf> wspes_sample: SGP40: Found device "sgp40@59", getting sensor data
   [00:00:06.349,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:06.385,000] <inf> wspes_sample: DOF: -1.920749 0.399831 -9.746795 XYZ-Accel. [m/s/s]
   [00:00:06.385,000] <inf> wspes_sample: DOF: 0.008660 -0.000266 0.022116 XYZ-Gyro. [rad/s]
   [00:00:06.385,000] <inf> wspes_sample: DOF: -0.136598 0.807170 -1.143321 XYZ-Magn. [uG]
   [00:00:06.385,000] <inf> wspes_sample: DOF: 30.51 Temp. [C]
   [00:00:06.385,000] <inf> wspes_sample: THP: 98.06 AirPr. [hPa]
   [00:00:06.385,000] <inf> wspes_sample: THP: 27.68 Temp. [C]
   [00:00:06.385,000] <inf> wspes_sample: THP: 41.224 RH [%]
   [00:00:06.385,000] <inf> wspes_sample: VOC: 2 Gas [a.u.]
   [00:00:08.387,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:08.423,000] <inf> wspes_sample: DOF: -1.926734 0.404620 -9.764153 XYZ-Accel. [m/s/s]
   [00:00:08.423,000] <inf> wspes_sample: DOF: 0.009192 -0.000399 0.023581 XYZ-Gyro. [rad/s]
   [00:00:08.424,000] <inf> wspes_sample: DOF: -0.131276 0.801848 -1.138194 XYZ-Magn. [uG]
   [00:00:08.424,000] <inf> wspes_sample: DOF: 30.60 Temp. [C]
   [00:00:08.424,000] <inf> wspes_sample: THP: 98.06 AirPr. [hPa]
   [00:00:08.424,000] <inf> wspes_sample: THP: 27.71 Temp. [C]
   [00:00:08.424,000] <inf> wspes_sample: THP: 41.128 RH [%]
   [00:00:08.424,000] <inf> wspes_sample: VOC: 30075 Gas [a.u.]
   [00:00:10.426,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:10.465,000] <inf> wspes_sample: DOF: -1.928530 0.401028 -9.756372 XYZ-Accel. [m/s/s]
   [00:00:10.465,000] <inf> wspes_sample: DOF: 0.009725 -0.000266 0.022782 XYZ-Gyro. [rad/s]
   [00:00:10.465,000] <inf> wspes_sample: DOF: -0.147242 0.810718 -1.129649 XYZ-Magn. [uG]
   [00:00:10.465,000] <inf> wspes_sample: DOF: 30.65 Temp. [C]
   [00:00:10.465,000] <inf> wspes_sample: THP: 98.06 AirPr. [hPa]
   [00:00:10.465,000] <inf> wspes_sample: THP: 27.76 Temp. [C]
   [00:00:10.465,000] <inf> wspes_sample: THP: 40.976 RH [%]
   [00:00:10.465,000] <inf> wspes_sample: VOC: 30669 Gas [a.u.]

The `SGP40 Datasheet`_ states that the raw sensor signal for the SGP40 is
proportional to the logarithm of the sensors resistance, hence the VOC Gas
value is labeled as [a.u.] (arbitrary units) in the example.
