.. _stk8ba58_3_axis_accelerometer-sample:

STK8BA58 3-Axis Accelerometer Sample
####################################

Get accelerometer data from an STK8BA58 sensor (polling & trigger mode).

Description
***********

This sample application periodically reads accelerometer data from the
STK8BA58 sensor and displays the sensor data on the console.

Requirements
************

This sample uses the STK8BA58, Sensortek MEMS system-in-package featuring
a 3-axis accelerometer sensor with digital output.

References
**********

- `STK8BA58 sensor <STK8BA58_>`_ (`STK8BA58 Datasheet`_)

API
===

   .. doxygengroup:: io_sensors_imu_stk8ba58
      :project: bridle

   .. doxygengroup:: STK8BA58
      :project: bridle

Building and Running
********************

The STK8BA58 sensor is unusual and only found on a few boards or shields.
In Zephyr there is no hardware with this sensor yet. In Bridle only two
variants of the |bridle:board:picoboy| can be used:

* |PicoBoy| (only polling, interrupt signal not connected)
* |PicoBoy Color Plus| (polling and trigger)

.. _stk8ba58-sample-picoboy:

Building on picoboy
===================

The |PicoBoy| includes an STK8BA58, but doesn't support the trigger mode. The
interrupt line is not connected.

.. zephyr-app-commands::
   :app: bridle/samples/stk8ba58
   :board: picoboy/rp2040
   :build-dir: picoboy-stk8ba58
   :west-args: -p
   :goals: flash

.. rubric:: Sample Output

.. parsed-literal::
   :class: highlight-console notranslate

   [00:00:00.002,000] <dbg> STK8BA58: stk8ba58_init: stk8ba58\ @\ 18: **chip id 0x87**
   [00:00:00.003,000] <dbg> STK8BA58: stk8ba58_init: stk8ba58\ @\ 18: pm: 7, odr: 5
   [00:00:00.003,000] <dbg> STK8BA58: stk8ba58_set_odr: stk8ba58\ @\ 18: set **odr to 250 Hz**, **bw to 125 Hz**
   [00:00:00.005,000] <dbg> STK8BA58: stk8ba58_init: stk8ba58\ @\ 18: range is 2
   [00:00:00.006,000] <dbg> STK8BA58: stk8ba58_set_range: stk8ba58\ @\ 18: set **range to 2g**, **gain to 0.98 mg/LSB**

   \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
   [00:00:00.250,000] :byl:`<wrn> udc_rpi: BUS RESET`
   [00:00:00.334,000] :byl:`<wrn> udc_rpi: BUS RESET`
   \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*

   [00:00:04.009,000] <dbg> STK8BA58: stk8ba58_set_range: stk8ba58\ @\ 18: set **range to 8g**, gain to **3.91 mg/LSB**

   Range at 80 m/s^2
   Polling at 0.5 Hz
   #1 @ 4009 ms: x 5.295395 , y -0.961051 , z -9.149213
   #2 @ 6013 ms: x 5.372279 , y -0.941830 , z -9.197265
   #3 @ 8015 ms: x 5.314616 , y -0.903388 , z -9.139602
   #4 @ 10018 ms: x 5.391500 , y -0.980272 , z -9.312591
   #5 @ 12020 ms: x 5.372279 , y -0.912999 , z -9.168433
   #6 @ 14022 ms: x 5.324226 , y -0.912999 , z -9.178044
   #7 @ 16025 ms: x 5.343447 , y -0.884167 , z -9.091549
   #8 @ 18027 ms: x 5.314616 , y -1.037935 , z -9.110771
   #9 @ 20029 ms: x 5.391500 , y -0.932220 , z -9.081939
   #10 @ 22032 ms: x 5.314616 , y -0.932220 , z -9.235707
   #11 @ 24034 ms: x 5.420332 , y -0.941830 , z -9.158823
   #12 @ 26036 ms: x 5.372279 , y -0.816893 , z -9.129991
   #13 @ 28039 ms: x 5.362668 , y -0.932220 , z -9.149213
   #14 @ 30041 ms: x 5.295395 , y -0.941830 , z -9.216485
   #15 @ 32043 ms: x 5.372279 , y -0.864946 , z -9.158823

.. _stk8ba58-sample-pbcp:

Building on picoboy_color_plus
==============================

The |PicoBoy Color Plus| includes an STK8BA58 with connected interrupt line.

.. zephyr-app-commands::
   :app: bridle/samples/stk8ba58
   :board: picoboy_color_plus/rp2350a/m33
   :build-dir: picoboy-stk8ba58
   :west-args: -p
   :goals: flash

.. rubric:: Sample Output

.. parsed-literal::
   :class: highlight-console notranslate

   [00:00:00.001,000] <dbg> STK8BA58: stk8ba58_init: stk8ba58\ @\ 18: **chip id 0x87**
   [00:00:00.001,000] <dbg> STK8BA58: stk8ba58_trigger_init: stk8ba58\ @\ 18: int on **gpio@40028000.22**
   [00:00:00.001,000] <dbg> STK8BA58: stk8ba58_set_pm: stk8ba58\ @\ 18: set **pm to low-power**, **sleep 25ms**
   [00:00:00.001,000] <dbg> STK8BA58: stk8ba58_init: stk8ba58\ @\ 18: pm: 7, odr: 5
   [00:00:00.001,000] <dbg> STK8BA58: stk8ba58_set_odr: stk8ba58\ @\ 18: set **odr to 250 Hz**, **bw to 125 Hz**
   [00:00:00.002,000] <dbg> STK8BA58: stk8ba58_init: stk8ba58\ @\ 18: range is 2
   [00:00:00.002,000] <dbg> STK8BA58: stk8ba58_set_range: stk8ba58\ @\ 18: set **range to 2g**, **gain to 0.98 mg/LSB**

   \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
   [00:00:00.488,000] :byl:`<wrn> udc_rpi: BUS RESET`
   [00:00:00.584,000] :byl:`<wrn> udc_rpi: BUS RESET`
   \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*

   [00:00:04.004,000] <dbg> STK8BA58: stk8ba58_set_range: stk8ba58\ @\ 18: set **range to 8g**, gain to **3.91 mg/LSB**
   [00:00:04.004,000] <dbg> STK8BA58: stk8ba58_set_odr: stk8ba58\ @\ 18: set **odr to 15.63 Hz**, **bw to 7.81 Hz**
   [00:00:04.004,000] <dbg> STK8BA58: stk8ba58_set_pm: stk8ba58\ @\ 18: set **pm to low-power**, **sleep 1000ms**
   [00:00:04.005,000] <dbg> STK8BA58: stk8ba58_init_interrupt: stk8ba58\ @\ 18: int1: enable **push-pull mode**
   [00:00:04.006,000] <dbg> STK8BA58: stk8ba58_init_interrupt: stk8ba58\ @\ 18: int1: enable **active-high polarity**

   Range at 80 m/s^2
   Waiting for triggers
   #1 @ 4116 ms: x -1.441577 , y 4.632269 , z -9.110771
   #2 @ 4226 ms: x -1.460798 , y 4.613048 , z -9.139602
   #3 @ 4335 ms: x -1.451188 , y 4.622658 , z -9.129991
   #4 @ 4444 ms: x -1.451188 , y 4.632269 , z -9.110771
   #5 @ 4554 ms: x -1.451188 , y 4.613048 , z -9.129991
   #6 @ 4663 ms: x -1.441577 , y 4.613048 , z -9.120381
   #7 @ 4772 ms: x -1.460798 , y 4.632269 , z -9.139602
   #8 @ 4882 ms: x -1.460798 , y 4.622658 , z -9.120381
   #9 @ 4991 ms: x -1.470409 , y 4.613048 , z -9.129991
   #10 @ 5100 ms: x -1.451188 , y 4.613048 , z -9.139602
   #11 @ 5209 ms: x -1.451188 , y 4.632269 , z -9.110771
   #12 @ 5319 ms: x -1.441577 , y 4.622658 , z -9.120381
   #13 @ 5428 ms: x -1.431967 , y 4.613048 , z -9.129991
   #14 @ 5537 ms: x -1.451188 , y 4.622658 , z -9.129991
   #15 @ 5647 ms: x -1.431967 , y 4.651490 , z -9.129991
