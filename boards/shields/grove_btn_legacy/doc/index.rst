.. image:: /images/seeed_grove.png
   :align: right

.. _grove_button_shield:

Grove Button Shields
####################

Bridle supports a couple of different Button shields carrying Seeed Studio
`Grove System`_ connectors. Please download and read through the
`Preface - Getting Started`_ and `Introduction to Grove`_ before
use the product. Also have a look on the SiPEED Wiki page about the
`Grove standard interfaces`_.

Seeed Studio Button Shields
***************************

Variants and Versions
=====================

Here find the comparison between various variants and versions of Seeed Studio
Button Shields:

+-----------------------+------------------+-----------------+--------------+--------------+
| Parameter             | Dual Button V1.0 | LED Button V1.0 | Button V1.2  | Button V1.0  |
+=======================+==================+=================+==============+==============+
| Release Date          | Sep 2019         | Jun 2018        | Dec 2016     | Apr 2011     |
+-----------------------+------------------+-----------------+--------------+--------------+
| Operation Voltage     | 3.3V or 5V       | 3.3V or 5V      | 3.3V or 5V   | 3.3V or 5V   |
+-----------------------+------------------+-----------------+--------------+--------------+
| Operation Temperature |                  |                 | -25℃ to +70℃ | -25℃ to +70℃ |
+-----------------------+------------------+-----------------+--------------+--------------+
| Grove Connectors      | 1                | 1               | 1            | 1            |
+-----------------------+------------------+-----------------+--------------+--------------+
| Digital Ports         | 1                | 1               | 1            | 1            |
+-----------------------+------------------+-----------------+--------------+--------------+
| Analog Ports          |                  |                 |              |              |
+-----------------------+------------------+-----------------+--------------+--------------+
| UART Ports            |                  |                 |              |              |
+-----------------------+------------------+-----------------+--------------+--------------+
| I2C Ports             |                  |                 |              |              |
+-----------------------+------------------+-----------------+--------------+--------------+
| SPI Ports             |                  |                 |              |              |
+-----------------------+------------------+-----------------+--------------+--------------+

.. toctree::
   :caption: Supported Grove Button Shields
   :maxdepth: 1
   :glob:

   **/index

Utilization
***********

Requirements
============

This shield can only be used with a development board or shield that provides
a configuration for `Grove System`_ connectors with `Grove Digital Layout`_
and defines a device tree phandle ``grove_gpios`` as an
|Laced Grove Signal Interface|.

Programming
===========

Set ``-DSHIELD=grove_btn_dX`` when you invoke ``west build``, wherein ``X``
corresponds to the ordinal number of a signal from the
|Laced Grove Signal Interface|. For example:

.. rubric:: Grove LED Button V1.0

#. :ref:`grove_base_shield_v2` on |zephyr:board:mimxrt1060_evk|
   for **GPIO driven Button** on Grove ``D4``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v2-grove_btn_d4_inv
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v2 grove_btn_d4_inv"
      :goals: flash
      :west-args: -p
      :host-os: unix

#. :ref:`grove_base_shield_v13` or :ref:`grove_base_shield_v12` on
   |zephyr:board:mimxrt1060_evk| for **GPIO driven Button** on Grove ``D4``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v1-grove_btn_d4_inv
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v1 grove_btn_d4_inv"
      :goals: flash
      :west-args: -p
      :host-os: unix

.. rubric:: Grove Button V1.2 and V1.0

#. :ref:`grove_base_shield_v2` on |zephyr:board:mimxrt1060_evk|
   for **GPIO driven Button** on Grove ``D4``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v2-grove_btn_d4
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v2 grove_btn_d4"
      :goals: flash
      :west-args: -p
      :host-os: unix

#. :ref:`grove_base_shield_v13` or :ref:`grove_base_shield_v12` on
   |zephyr:board:mimxrt1060_evk| for **GPIO driven Button** on Grove ``D4``:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-seeed_grove_base_v1-grove_btn_d4
      :board: mimxrt1060_evk@B/mimxrt1062/qspi
      :shield: "seeed_grove_base_v1 grove_btn_d4"
      :goals: flash
      :west-args: -p
      :host-os: unix

References
**********

.. target-notes::
