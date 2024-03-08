.. _waveshare_pico_10dof_imu_sensor_sample:


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
:ref:`zephyr:rpi_pico` board.

The following examples use the shield in revision 2.1. If these should be used
for revision 1, the variable ``SHIELD`` must be adapted accordingly.

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

.. code-block:: kmsg

   [00:00:00.075,000] <dbg> MPU9250: ak8963_fetch_adj: Adjustment values 1756 1762 1698
   *** Booting Zephyr OS build … … … ***
   [00:00:04.088,000] <inf> wsptdis_sample: MPU9250: Found device "mpu9250@68", getting sensor data
   [00:00:04.088,000] <inf> wsptdis_sample: DOF: Configured for triggered sampling.
   [00:00:04.088,000] <inf> wsptdis_sample: LPS22HB: Found device "lps22hb@5c", getting sensor data
   [00:00:04.089,000] <inf> wsptdis_sample: TP: 98.13 AirPr. [hPa]
   [00:00:04.090,000] <inf> wsptdis_sample: TP: 29.01 Temp. [C]
   [00:00:04.096,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:04.096,000] <inf> wsptdis_sample: DOF: 1.511339 -1.048062 10.103531 XYZ-Accel. [m/s/s]
   [00:00:04.096,000] <inf> wsptdis_sample: DOF: -0.031442 0.011591 -0.017453 XYZ-Gyro. [rad/s]
   [00:00:04.096,000] <inf> wsptdis_sample: DOF: 0.363492 0.096910 -0.378654 XYZ-Magn. [uG]
   [00:00:04.096,000] <inf> wsptdis_sample: DOF: 32.22 Temp. [C]
   [00:00:06.091,000] <inf> wsptdis_sample: TP: 98.12 AirPr. [hPa]
   [00:00:06.091,000] <inf> wsptdis_sample: TP: 29.04 Temp. [C]
   [00:00:06.105,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:06.105,000] <inf> wsptdis_sample: DOF: 1.508347 -1.046267 10.108917 XYZ-Accel. [m/s/s]
   [00:00:06.106,000] <inf> wsptdis_sample: DOF: -0.032508 0.010392 -0.017453 XYZ-Gyro. [rad/s]
   [00:00:06.106,000] <inf> wsptdis_sample: DOF: 0.354712 0.095148 -0.380352 XYZ-Magn. [uG]
   [00:00:06.106,000] <inf> wsptdis_sample: DOF: 32.29 Temp. [C]
   [00:00:08.092,000] <inf> wsptdis_sample: TP: 98.12 AirPr. [hPa]
   [00:00:08.092,000] <inf> wsptdis_sample: TP: 29.08 Temp. [C]
   [00:00:08.115,000] <dbg> MPU9250: mpu9250_sample_fetch: magn_st2: 16
   [00:00:08.115,000] <inf> wsptdis_sample: DOF: 1.510741 -1.045070 10.106523 XYZ-Accel. [m/s/s]
   [00:00:08.115,000] <inf> wsptdis_sample: DOF: -0.030643 0.012923 -0.017586 XYZ-Gyro. [rad/s]
   [00:00:08.115,000] <inf> wsptdis_sample: DOF: 0.365248 0.084576 -0.373560 XYZ-Magn. [uG]
   [00:00:08.115,000] <inf> wsptdis_sample: DOF: 32.34 Temp. [C]
