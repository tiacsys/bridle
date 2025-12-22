.. _sc16is75x_bb_shield:

SC16IS75x Breakout Boards
#########################

This is a collection of very simple and often copied breakout boards as
Zephyr :external+zephyr:ref:`shield <shields>` based on the NXP SC16IS750_
or SC16IS752_ chip, a bridge from an :external+zephyr:ref:`I2C <i2c_api>`
or :external+zephyr:ref:`SPI <spi_api>` bus to a single or dual channel
:external+zephyr:ref:`UART <uart_api>` with integrated
:external+zephyr:ref:`GPIO <gpio_api>` controller. The origin of all
breakout boards was the BOB-09981_ (BOB-09745_) design from SparkFun
with the single-channel UART/GPIO bridge. This is available both as a
one-to-one clone and as a modified version with a two-channel UART/GPIO
bridge from |CJMCU|_ or |Q-Baihe|_.

Operation and connection
************************

All breakout boards contain only the essential components required to operate
the bridge IC. These are a crystal for clock provision, blocking capacitors,
important pull-up resistors and a small 3.3V power supply. Any additional
circuits or components required must be provided externally. The single channel
UART/GPIO breakout boards use the NXP SC16IS750_. The dual channel UART/GPIO
breakout boards use the NXP SC16IS752_. The user is free to select either an
I2C or an SPI bus to operate with the bridge IC. The selection is made via
the pin labeled ``I2C/SPI`` on one of the headers. See figures below.

All bridge ICs are interrupt-capable (``/IRQ``) and can be reset by a hardware
reset (``/RESET``). Breakout boards with a **SC16IS750** (*single channel*)
have a crystal with a fixed frequency of **14.7456MHz**. Breakout boards with
a **SC16IS752** (*dual channel*) have a crystal with a fixed frequency of
**1.8432MHz**.

SPI bus operation
=================

The SC16IS750 or SC16IS752 works in SPI bus operation mode when ``I2C/SPI``
set to **Low**.

.. list-table::
   :header-rows: 1
   :align: center

   * - .. image:: img/SC16IS750-BD-SPI.jpg
          :align: center
     - .. image:: img/SC16IS752-BD-SPI.jpg
          :align: center

   * - SC16IS750 on SPI bus
     - SC16IS752 on SPI bus

Multiple bridge ICs can be used by connecting the SPI ``/CS`` signal to
different outputs of the SPI host controller.

.. note::

   Despite what may be printed on the PCB, when using the SC16IS750 or
   SC16IS752 in SPI mode, the ``SDA`` pin should be held low or open,
   not high. Otherwise, interrupt handling may not function correctly.

I2C bus operation
=================

The SC16IS750 or SC16IS752 works in I2C bus operation mode when ``I2C/SPI``
set to **High**.

.. list-table::
   :header-rows: 1
   :align: center

   * - .. image:: img/SC16IS750-BD-I2C.jpg
          :align: center
     - .. image:: img/SC16IS752-BD-I2C.jpg
          :align: center

   * - SC16IS750 on I2C bus
     - SC16IS752 on I2C bus

Multiple bridge ICs can be operated on a single I2C host controller by
correctly wiring the I2C address select pins ``A0`` and ``A1``. See the
following table.

.. include:: i2c_address_selection.rsti

Supported Shields
*****************

Single-channel UART/GPIO bridge
===============================

.. tabs::

   .. group-tab:: SparkFun BOB-09745

      :brd:`OBSOLETE and UNSUPPORTED`, use BOB-09981 instead!

      .. image:: img/BOB-09745.jpg
         :align: center
         :width: 33%

      The BOB-09745_ is the original breakout board from SparkFun in the
      early first **revision v1.2** with a :brd:`12.2880MHz` crystal. This
      revision is not supported by this shield abstraction, as a
      :brd:`crystal` is populated :brd:`with an unsuitable value`!

      - `BOB-09745 Schematic`_
      - Git: https://github.com/sparkfun/SC16IS750_Breakout/tree/v_1.3
      - `SC16IS750 Datasheet`_

      .. warning::

         .. image:: img/BOB-09xxx-IRQ-fix.jpg
            :align: right

         The board contains a design defect resulting in the interrupt pin
         (``/IRQ``) of the SC16IS750 not being physically connected to the
         board outputs.

         See also: https://github.com/sparkfun/SC16IS750_Breakout/issues/1

         However, this error can be fixed by soldering a small wire bridge
         from pin 11 (``/IRQ``) of the SC16IS750, or rather the one side of
         the related pull-up resistor, to the pin header directly to the
         left side of it. See the enclosed illustration.

   .. group-tab:: SparkFun BOB-09981

      :byl:`SUPPORTED` but :brd:`FAULTY HARDWARE`

      .. image:: img/BOB-09981.jpg
         :align: center
         :width: 33%

      The BOB-09981_ is the original breakout board from SparkFun in the
      redesigned **revision v1.3** with a :bgn:`14.7456MHz` crystal to
      :bgn:`allow baud rates from 9600 up to 921600`.

      - `BOB-09981 Schematic`_
      - Git: https://github.com/sparkfun/SC16IS750_Breakout/tree/v_1.3
      - `SC16IS750 Datasheet`_

      .. warning::

         .. image:: img/BOB-09xxx-IRQ-fix.jpg
            :align: right

         The board contains a design defect resulting in the interrupt pin
         (``/IRQ``) of the SC16IS750 not being physically connected to the
         board outputs.

         See also: https://github.com/sparkfun/SC16IS750_Breakout/issues/1

         However, this error can be fixed by soldering a small wire bridge
         from pin 11 (``/IRQ``) of the SC16IS750, or rather the one side of
         the related pull-up resistor, to the pin header directly to the
         left side of it. See the enclosed illustration.

   .. group-tab:: CJMCU-750

      :byl:`SUPPORTED` but :brd:`FAULTY HARDWARE`

      .. image:: img/CJMCU-750.jpg
         :align: center
         :width: 33%

      The `CJMCU-750 <CJMCU_>`_ is a widely used clone based on the original
      SparkFun breakout board and :brd:`has the exact same design flaws!`

      - `SC16IS750 Datasheet`_

      .. warning::

         .. image:: img/CJMCU-750-IRQ-fix.jpg
            :align: right

         The unconnected interrupt line was copied from the faulty original
         design, the interrupt pin (``/IRQ``) of the SC16IS750 not being
         physically connected to the board outputs.

         See also: https://github.com/sparkfun/SC16IS750_Breakout/issues/1

         However, this error can be fixed by soldering a small wire bridge
         from pin 11 (``/IRQ``) of the SC16IS750, or rather the one side of
         the related pull-up resistor, to the pin header directly to the
         left side of it. See the enclosed illustration.

   .. group-tab:: Q-Baihe GT-SC16IS750

      :bgn:`SUPPORTED (best choice)`

      .. image:: img/GT-SC16IS750.jpg
         :align: center
         :width: 33%

      The `GT-SC16IS750`_ is a very rare clone based on the original SparkFun
      breakout board, **but with the missing interrupt line fixed!** This copy
      corresponds to the design **revision v1.4** from SparkFun.

      - `GT-SC16IS750 Schematic`_
      - Git: https://github.com/sparkfun/SC16IS750_Breakout/tree/v_1.4
      - `SC16IS750 Datasheet`_

Dual-channel UART/GPIO bridge
=============================

Derived from the single-channel breakout board, the new development from
|CJMCU|_ and its clones with an SC16IS752 are also supported. These feature
a dual-channel UART/GPIO bridge. All this boards coming with a **1.8432MHz**
crystal. There are no circuit documents for any of the dual-channel breakout
boards.

.. tabs::

   .. group-tab:: CJMCU-752

      .. image:: img/CJMCU-752.jpg
         :align: center
         :width: 33%

      - `SC16IS752 Datasheet`_

   .. group-tab:: WCMCU-752

      .. image:: img/WCMCU-752.jpg
         :align: center
         :width: 33%

      - `SC16IS752 Datasheet`_

Utilization
***********

The shield abstraction of these breakout boards is deliberately kept small.
It is purely for evaluating the necessary drivers and Devicetree bindings
on known integration platforms. Due to the large number of clones and the
associated PCB designations and product names, only two basic shield names
are used and extended by the respective short name of the serial peripheral
bus to be used. A special case is the suffix ``_noirq``. This is necessary
if a faulty single-channel breakout board **without interrupt line** is to
be used. The various connectors on the single and dual channel boards are
generally defined using their own Nyxus header bindings:

.. list-table::
   :stub-columns: 1
   :header-rows: 1
   :align: center

   * -
     - I2C shield names
     - SPI shield names
     - DTS header bindings

   * - SC16IS750
     - | ``cjmcu_750_i2c``
       | ``cjmcu_750_i2c_noirq``
     - | ``cjmcu_750_spi``
       | ``cjmcu_750_spi_noirq``
     - | :dtcompatible:`cjmcu,75x-hif-header`
       | :dtcompatible:`cjmcu,75x-gpio-header`

   * - SC16IS752
     - | ``cjmcu_752_i2c``
       | ``cjmcu_752_i2c_noirq``
     - | ``cjmcu_752_spi``
       | ``cjmcu_752_spi_noirq``
     - | :dtcompatible:`cjmcu,75x-hif-header`
       | :dtcompatible:`cjmcu,75x-gpio-header`

This shields can be used with any development board or shield that provides
a Devicetree node with the :dtcompatible:`cjmcu,75x-hif-header` property in
the compatibility. That is needed for GPIO mapping of the reset and optional
interrupt line. Users can rely on the :ref:`x_cjmcu_75x_shield` or create
their own interconnection shields with the necessary mappings in them.

Programming
===========

.. tabs::

   .. group-tab:: Single-channel UART/GPIO bridge (SC16IS750)

      .. tabs::

         .. group-tab:: SPI

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_750
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_750_spi"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

            .. rubric:: Interrupt disabled

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_750
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_750_spi_noirq"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

         .. group-tab:: I2C

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_750
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_750_i2c"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

            .. rubric:: Interrupt disabled

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_750
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_750_i2c_noirq"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

   .. group-tab:: Dual-channel UART/GPIO bridge (SC16IS752)

      .. tabs::

         .. group-tab:: SPI

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_752
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_752_spi"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

            .. rubric:: Interrupt disabled

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_752
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_752_spi_noirq"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

         .. group-tab:: I2C

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_752
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_752_i2c"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

            .. rubric:: Interrupt disabled

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: cjmcu_752
               :board: nucleo_f746zg
               :shield: "x_cjmcu_75x cjmcu_752_i2c_noirq"
               :west-args: -p
               :goals: flash
               :host-os: unix
               :compact:

References
**********

API
===

   .. doxygengroup:: mfd_interface_sc16is75x
      :project: bridle

   .. doxygengroup:: io_gpio_sc16is75x
      :project: bridle

   .. doxygengroup:: io_serial_sc16is75x
      :project: bridle

Links
=====

.. target-notes::
