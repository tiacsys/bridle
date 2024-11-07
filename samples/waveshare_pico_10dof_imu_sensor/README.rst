.. _waveshare_pico_10dof_imu_sensor-sample:


Waveshare Pico 10-DOF IMU Sensor Sample
#######################################

- TP: LPS22HB, I2C absolute barometric air pressure with temperature sensor
- DOF: MPU-9250 (ICM-20948), I2C accelerometer, gyroscope and magnetometer

Description
***********

This sample application periodically measures the ambient temperature and air
pressure from the TP device and the chip temperature, acceleration, angular
velocity and the terrestrial magnetism in all XYZ spatial coordinates from
the DOF device. The result is written to the console along with the time
since startup.

References
**********

- `LPS22HB sensor <LPS22HB_>`_ (`LPS22HB Datasheet`_)
- :strong:`Shield revision 2.1`: `MPU-9250 sensor <MPU-9250_>`_
  (`MPU-9250 Datasheet`_, `MPU-9250 Register Map`_)

  - `AK8963 sensor <AK8963>`_ (`AK8963 Datasheet`_)

- :strong:`Shield revision 1`: `ICM-20948 sensor <ICM-20948_>`_
  (`ICM-20948 Datasheet`_, `ICM-20948 Software User Guide`_)

  - `AK09916 sensor <AK09916>`_ (`AK09916 Datasheet`_)

Wiring
******

This sample uses all sensors controlled by using the I2C interface.

- connect supply: :strong:`VDD`, :strong:`GND`
- and interface: :strong:`SDA`, :strong:`SCL`.

The supply voltage can be in the 2.4V to 3.6V range. Depending on the baseboard
used, the :strong:`SDA` and :strong:`SCL` lines require Pull-Up resistors.

Building and Running
********************

This project outputs sensor data to the console. It requires a LPS22HB
and a MPU-9250 sensor. It should work with any platform featuring
a I2C peripheral interface. This example is usable with the Devicetree overlay
that comes with the :ref:`waveshare_pico_10dof_imu_sensor` shield for the
|zephyr:board:rpi_pico| board.

The following examples use the shield in revision 2.1. If these should be used
for revision 1, the variable :code:`SHIELD` must be adapted accordingly.

.. zephyr-app-commands::
   :app: bridle/samples/waveshare_pico_10dof_imu_sensor
   :board: rpi_pico
   :shield: waveshare_pico_10dof_imu_sensor_r2
   :build-dir: waveshare_pico_10dof_imu_sensor_r2
   :west-args: -p -S usb-console
   :flash-args: -r uf2
   :goals: flash

Sample Output
=============

.. parsed-literal::
   :class: highlight-console notranslate

   [00:00:00.067,000] <dbg> MPU9250: ak8963_fetch_adj: Adjustment values 1756 1762 1698
   \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
   [00:00:00.328,000] :byl:`<wrn> udc_rpi: BUS RESET`
   [00:00:00.408,000] :byl:`<wrn> udc_rpi: BUS RESET`
   \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
   [00:00:04.079,000] <inf> wsptdis_sample: MPU9250: Found device "**mpu9250@68**", getting sensor data
   [00:00:04.079,000] <inf> wsptdis_sample: DOF: Configured for triggered sampling.
   [00:00:04.079,000] <inf> wsptdis_sample: LPS22HB: Found device "**lps22hb@5c**", getting sensor data

   [00:00:04.080,000] <inf> wsptdis_sample: TP: 101.45 AirPr. [hPa]
   [00:00:04.080,000] <inf> wsptdis_sample: TP: 28.58 Temp. [C]
   [00:00:04.087,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:04.087,000] <inf> wsptdis_sample: DOF: 0.174776 0.377086 10.339359 XYZ-Accel. [m/s/s]
   [00:00:04.087,000] <inf> wsptdis_sample: DOF: -0.029843 0.015588 -0.023581 XYZ-Gyro. [rad/s]
   [00:00:04.087,000] <inf> wsptdis_sample: DOF: 0.200184 -0.052860 -0.254700 XYZ-Magn. [uG]
   [00:00:04.087,000] <inf> wsptdis_sample: DOF: 31.82 Temp. [C]

   [00:00:06.082,000] <inf> wsptdis_sample: TP: 101.45 AirPr. [hPa]
   [00:00:06.082,000] <inf> wsptdis_sample: TP: 28.65 Temp. [C]
   [00:00:06.096,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:06.096,000] <inf> wsptdis_sample: DOF: 0.178966 0.384867 10.322600 XYZ-Accel. [m/s/s]
   [00:00:06.096,000] <inf> wsptdis_sample: DOF: -0.030110 0.013056 -0.024248 XYZ-Gyro. [rad/s]
   [00:00:06.096,000] <inf> wsptdis_sample: DOF: 0.189648 -0.063432 -0.261492 XYZ-Magn. [uG]
   [00:00:06.096,000] <inf> wsptdis_sample: DOF: 31.93 Temp. [C]

   [00:00:08.083,000] <inf> wsptdis_sample: TP: 101.45 AirPr. [hPa]
   [00:00:08.083,000] <inf> wsptdis_sample: TP: 28.72 Temp. [C]
   [00:00:08.106,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:08.106,000] <inf> wsptdis_sample: DOF: 0.168192 0.387262 10.321403 XYZ-Accel. [m/s/s]
   [00:00:08.106,000] <inf> wsptdis_sample: DOF: -0.030243 0.013189 -0.024381 XYZ-Gyro. [rad/s]
   [00:00:08.106,000] <inf> wsptdis_sample: DOF: 0.198428 -0.054622 -0.242814 XYZ-Magn. [uG]
   [00:00:08.106,000] <inf> wsptdis_sample: DOF: 32.04 Temp. [C]
