.. _gs_installing_os:

Supported operating systems
###########################

|BRIDLE| supports Linux, macOS, and Microsoft Windows for development.
In the :ref:`gs_recommended_versions` section you will find a detailed
list of the operating system support levels (Tier 1 to 3).

However, there are some **Zephyr features that are currently only
available on Linux, including:**

.. rubric:: Native host execution:

* |zephyr:board:native_posix|
* |zephyr:connectivity:networking:with:host| (`net-tools`_)

.. rubric:: Native host simulation:

* |zephyr:board:native_sim|
* |zephyr:connectivity:networking:with:native_sim|
  – virtual network between host and multiple simulations (`net-tools`_)
* |zephyr:connectivity:networking:with:native_sim_eth_bridge|
  – bridged Ethernet network between multiple simulations (`net-tools`_)
* |zephyr:boards:bsim| – `BabbleSim`_
  – BLE stack and IEEE 802.15.4 radio protocol simulation (2.4GHz ISM band)

  * |zephyr:board:nrf52_bsim|
  * |zephyr:board:nrf5340bsim|
  * |zephyr:board:nrf54l15bsim|

* |zephyr:connectivity:bluetooth:bluez| – `BlueZ`_
* |zephyr:connectivity:bluetooth:qemu_native| – `BlueZ`_
  – real Bluetooth controller exported from host into `QEMU`_ runtimes

  * Using the Host System Bluetooth Controller
  * Using a Zephyr-based BLE Controller
  * HCI Tracing

* |zephyr:connectivity:bluetooth:virtual_posix| – `BlueZ`_
  – virtual Bluetooth controller connected over an HCI TCP server

  * Android Emulator

* |zephyr:connectivity:bluetooth:ctlr_bluez| – `BlueZ`_
  – use Zephyr Bluetooth controller on host (simulated or emulated)

.. rubric:: Native host emulation:

* |zephyr:boards:qemu| boards for emulation
* |zephyr:connectivity:networking:with:qemu|
* |zephyr:connectivity:networking:with:eth_qemu|
  – virtual network between host and multiple `QEMU`_ runtimes
* |zephyr:connectivity:networking:with:user_qemu|
  – SLiRP user network backend
* |zephyr:connectivity:networking:with:ieee802154_qemu|
  – IEEE 802.15.4 link layer over UART between multiple `QEMU`_ runtimes

.. rubric:: Common host networking:

* |zephyr:connectivity:networking:with:multiple_instances|
  – virtual network between multiple Zephyr instances (simulated or emulated)

.. rubric:: Test framework:

As a result of native execution, simulation and emulation as listed above,
the Zephyr built-in test environment can only be reasonably used on Linux.

* :external+zephyr:ref:`test-framework`

  * Zephyr Test Framework (Ztest)

    * Integration testing
    * Unit testing

  * Zephyr stress test framework (Ztress)
  * Shuffling Test Sequence
  * Mocking via `Fake Function Framework <FFF_>`_

* :external+zephyr:ref:`twister_script`

.. note::

   .. _gs_update_os:

   Before you start setting up the toolchain, install available updates
   for your operating system.

.. admonition:: Comment and position statement
   :class: attention

   We recommend that you use Linux as your development platform of choice.

   MacOS is still a good alternative. However, with Microsoft Windows you will
   find a development environment that is extremely sluggish and complicated
   to maintain. Replication on a second or third system is extremely difficult
   and may even be impossible. There are no reliable tools for this and the
   behavior of Microsoft Windows cannot be predicted. In addition, Microsoft
   Windows currently still harbors the highest security risks in the area of
   cyber security – time to switch!
