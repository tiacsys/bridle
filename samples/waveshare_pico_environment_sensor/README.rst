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

.. parsed-literal::
   :class: highlight-console notranslate

   [00:00:00.001,000] <dbg> BME280: bme280_chip_init: ID OK
   [00:00:00.009,000] <dbg> BME280: bme280_chip_init: "bme280\ @\ 76" OK
   [00:00:00.260,000] <dbg> SGP40: sgp40_init: Selftest succeeded!
   [00:00:00.335,000] <dbg> MPU9250: ak8963_fetch_adj: Adjustment values 1774 1774 1709
   \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
   [00:00:00.501,000] :byl:`<wrn> udc_rpi: BUS RESET`
   [00:00:00.590,000] :byl:`<wrn> udc_rpi: BUS RESET`
   \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
   [00:00:04.347,000] <inf> wspes_sample: ICM20948: Found device "mpu9250\ @\ 68", getting sensor data
   [00:00:04.347,000] <inf> wspes_sample: BME280: Found device "bme280\ @\ 76", getting sensor data
   [00:00:04.347,000] <inf> wspes_sample: SGP40: Found device "sgp40\ @\ 59", getting sensor data
   [00:00:06.349,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:06.385,000] <inf> wspes_sample: DOF: -0.244209 0.053869 -9.913192 XYZ-Accel. [m/s/s]
   [00:00:06.385,000] <inf> wspes_sample: DOF: 0.017186 0.000266 0.007993 XYZ-Gyro. [rad/s]
   [00:00:06.385,000] <inf> wspes_sample: DOF: -0.026610 0.917158 -0.955331 XYZ-Magn. [uG]
   [00:00:06.386,000] <inf> wspes_sample: DOF: 27.74 Temp. [C]
   [00:00:06.386,000] <inf> wspes_sample: THP: 100.42 AirPr. [hPa]
   [00:00:06.386,000] <inf> wspes_sample: THP: 24.93 Temp. [C]
   [00:00:06.386,000] <inf> wspes_sample: THP: 58.971 RH [%]
   [00:00:06.386,000] <inf> wspes_sample: VOC: 26 Gas [a.u.]
   [00:00:08.388,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:08.424,000] <inf> wspes_sample: DOF: -0.253786 0.056862 -9.917382 XYZ-Accel. [m/s/s]
   [00:00:08.424,000] <inf> wspes_sample: DOF: 0.017986 0.000799 0.007860 XYZ-Gyro. [rad/s]
   [00:00:08.424,000] <inf> wspes_sample: DOF: -0.024836 0.911836 -0.946786 XYZ-Magn. [uG]
   [00:00:08.424,000] <inf> wspes_sample: DOF: 27.82 Temp. [C]
   [00:00:08.424,000] <inf> wspes_sample: THP: 100.42 AirPr. [hPa]
   [00:00:08.424,000] <inf> wspes_sample: THP: 24.97 Temp. [C]
   [00:00:08.424,000] <inf> wspes_sample: THP: 58.723 RH [%]
   [00:00:08.424,000] <inf> wspes_sample: VOC: 24795 Gas [a.u.]
   [00:00:10.426,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:10.489,000] <inf> wspes_sample: DOF: -0.254983 0.059256 -9.923966 XYZ-Accel. [m/s/s]
   [00:00:10.489,000] <inf> wspes_sample: DOF: 0.017453 0.000399 0.007194 XYZ-Gyro. [rad/s]
   [00:00:10.489,000] <inf> wspes_sample: DOF: -0.015966 0.910062 -0.962167 XYZ-Magn. [uG]
   [00:00:10.489,000] <inf> wspes_sample: DOF: 27.90 Temp. [C]
   [00:00:10.489,000] <inf> wspes_sample: THP: 100.42 AirPr. [hPa]
   [00:00:10.489,000] <inf> wspes_sample: THP: 25.04 Temp. [C]
   [00:00:10.490,000] <inf> wspes_sample: THP: 58.438 RH [%]
   [00:00:10.490,000] <inf> wspes_sample: VOC: 25663 Gas [a.u.]

The `SGP40 Datasheet`_ states that the raw sensor signal for the SGP40 is
proportional to the logarithm of the sensors resistance, hence the VOC Gas
value is labeled as [a.u.] (arbitrary units) in the example.
