.. _waveshare_pico_environment_sensor-sample:


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
|zephyr:board:rpi_pico| board:

   .. zephyr-app-commands::
      :app: bridle/samples/waveshare_pico_environment_sensor
      :build-dir: waveshare_pico_environment_sensor
      :board: rpi_pico
      :shield: "waveshare_pico_environment_sensor"
      :snippets: "usb-console"
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash

Sample Output
=============

.. parsed-literal::
   :class: highlight-console notranslate

   [00:00:00.001,000] <dbg> BME280: bme280_chip_init: ID OK
   [00:00:00.010,000] <dbg> BME280: bme280_chip_init: "**bme280@76**" OK
   [00:00:00.260,000] <dbg> SGP40: sgp40_init: Selftest succeeded!
   [00:00:00.325,000] <dbg> MPU9250: ak8963_fetch_adj: Adjustment values 1774 1774 1709
   \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…*\*\*\*
   [00:00:00.337,000] <inf> wspes_sample: ICM20948: Found device "**mpu9250@68**", getting sensor data
   [00:00:00.337,000] <inf> wspes_sample: BME280: Found device "**bme280@76**", getting sensor data
   [00:00:00.337,000] <inf> wspes_sample: SGP40: Found device "**sgp40@59**", getting sensor data

   [00:00:02.339,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:02.372,000] <inf> wspes_sample: DOF: 0.287304 0.171783 -9.950303 XYZ-Accel. [m/s/s]
   [00:00:02.372,000] <inf> wspes_sample: DOF: 0.018785 -0.001732 0.007993 XYZ-Gyro. [rad/s]
   [00:00:02.373,000] <inf> wspes_sample: DOF: 0.051446 0.952638 -0.941659 XYZ-Magn. [uG]
   [00:00:02.373,000] <inf> wspes_sample: DOF: 29.30 Temp. [C]
   [00:00:02.373,000] <inf> wspes_sample: THP: 101.31 AirPr. [hPa]
   [00:00:02.373,000] <inf> wspes_sample: THP: 26.50 Temp. [C]
   [00:00:02.373,000] <inf> wspes_sample: THP: 51.318 RH [%]
   [00:00:02.373,000] <inf> wspes_sample: VOC: 20 Gas [a.u.]

   [00:00:04.375,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:04.407,000] <inf> wspes_sample: DOF: 0.303465 0.171185 -9.943719 XYZ-Accel. [m/s/s]
   [00:00:04.408,000] <inf> wspes_sample: DOF: 0.018519 -0.000666 0.007460 XYZ-Gyro. [rad/s]
   [00:00:04.408,000] <inf> wspes_sample: DOF: 0.053220 0.954412 -0.936532 XYZ-Magn. [uG]
   [00:00:04.408,000] <inf> wspes_sample: DOF: 29.41 Temp. [C]
   [00:00:04.408,000] <inf> wspes_sample: THP: 101.31 AirPr. [hPa]
   [00:00:04.408,000] <inf> wspes_sample: THP: 26.53 Temp. [C]
   [00:00:04.408,000] <inf> wspes_sample: THP: 51.238 RH [%]
   [00:00:04.408,000] <inf> wspes_sample: VOC: 28285 Gas [a.u.]

   [00:00:06.410,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:06.483,000] <inf> wspes_sample: DOF: 0.286705 0.164002 -9.949105 XYZ-Accel. [m/s/s]
   [00:00:06.483,000] <inf> wspes_sample: DOF: 0.019584 -0.000932 0.008393 XYZ-Gyro. [rad/s]
   [00:00:06.483,000] <inf> wspes_sample: DOF: 0.047898 0.956186 -0.938241 XYZ-Magn. [uG]
   [00:00:06.483,000] <inf> wspes_sample: DOF: 29.49 Temp. [C]
   [00:00:06.483,000] <inf> wspes_sample: THP: 101.31 AirPr. [hPa]
   [00:00:06.483,000] <inf> wspes_sample: THP: 26.60 Temp. [C]
   [00:00:06.484,000] <inf> wspes_sample: THP: 51.062 RH [%]
   [00:00:06.484,000] <inf> wspes_sample: VOC: 28789 Gas [a.u.]

The `SGP40 Datasheet`_ states that the raw sensor signal for the SGP40 is
proportional to the logarithm of the sensors resistance, hence the VOC Gas
value is labeled as [a.u.] (arbitrary units) in the example.
