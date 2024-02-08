.. _gs_installing_os:

Supported operating systems
###########################

|BRIDLE| supports Linux, macOS, and Microsoft Windows for development.
However, there are some Zephyr features that are currently only available
on Linux, including:

* :ref:`zephyr:twister_script`
* :ref:`zephyr:native_posix`
* :ref:`zephyr:networking_with_native_sim` and
  :ref:`zephyr:networking_with_qemu` or
  :ref:`zephyr:networking_with_host` (net-tools)
* :ref:`zephyr:bluetooth_bluez` – `BlueZ`_
* :ref:`zephyr:nrf52_bsim` – `BabbleSim`_

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
