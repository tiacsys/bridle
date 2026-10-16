.. image:: /images/seeed_grove.png
   :align: right

.. _grove_led_shield:

Grove LED Shields
#################

Bridle supports a couple of different LED shields carrying Seeed Studio
`Grove System`_ connectors. Please download and read through the
`Preface - Getting Started`_ and `Introduction to Grove`_ before
use the product. Also have a look on the SiPEED Wiki page about the
`Grove standard interfaces`_.

Seeed Studio LED Shields
************************

Variants and Versions
=====================

Here find the comparison between various variants and versions of Seeed Studio
LED Shields:

+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| Parameter             | LED Button V1.0 | LED Socket Kit V1.3 / V1.0 | LED V1.1   | Variable Color LED V1.1 / V1.0 |
+=======================+=================+============================+============+================================+
| Release Date          | Jun 2018        | Oct 2015 / Feb 2013        | Apr 2011   | Sep 2017 / Apr 2011            |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| Operation Voltage     | 3.3V or 5V      | 3.3V or 5V                 | 3.3V or 5V | 5V only                        |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| Operation Temperature |                 |                            |            |                                |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| Grove Connectors      | 1               | 1                          | 1          | 1                              |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| Digital Ports         | 1               | 1                          | 1          | 1                              |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| Analog Ports          |                 |                            |            |                                |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| UART Ports            |                 |                            |            |                                |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| I2C Ports             |                 |                            |            |                                |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+
| SPI Ports             |                 |                            |            |                                |
+-----------------------+-----------------+----------------------------+------------+--------------------------------+

.. toctree::
   :caption: Supported Grove LED Shields
   :maxdepth: 1
   :glob:

   **/index

Utilization
***********

Requirements
============

This shield can only be used with a development board or shield that provides
a configuration for `Grove System`_ connectors with `Grove Digital Layout`_
and defines the device tree phandle ``grove_gpios`` and ``grove_pwms`` as an
|Laced Grove Signal Interface|.

Programming
===========

Set ``-DSHIELD=grove_led_dX`` or ``-DSHIELD=grove_pwm_led_dX`` when you invoke
``west build``, wherein ``X`` corresponds to the ordinal number of Grove signal
from the |Laced Grove Signal Interface|. For example:

#. :ref:`grove_base_shield_v2` on |zephyr:board:mimxrt1060_evk|
   for **GPIO driven LED** on Grove ``D5``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v2-grove_led_d5
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v2 grove_led_d5"
      :goals: flash
      :west-args: -p
      :host-os: unix

#. :ref:`grove_base_shield_v2` on |zephyr:board:mimxrt1060_evk|
   for **PWM driven LED** on Grove ``D5``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v2-grove_pwm_led_d5
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v2 grove_pwm_led_d5"
      :goals: flash
      :west-args: -p
      :host-os: unix

#. :ref:`grove_base_shield_v13` or :ref:`grove_base_shield_v12` on
   |zephyr:board:mimxrt1060_evk| for **GPIO driven LED** on Grove ``D5``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v1-grove_led_d5
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v1 grove_led_d5"
      :goals: flash
      :west-args: -p
      :host-os: unix

#. :ref:`grove_base_shield_v13` or :ref:`grove_base_shield_v12` on
   |zephyr:board:mimxrt1060_evk| for **GPIO driven LED** on Grove ``D5``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v1-grove_pwm_led_d5
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v1 grove_pwm_led_d5"
      :goals: flash
      :west-args: -p
      :host-os: unix

References
**********

.. target-notes::
