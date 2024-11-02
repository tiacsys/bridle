.. _app_build_system:

Build and configuration system
##############################

.. contents::
   :local:
   :depth: 2

The |BRIDLE| build and configuration system is based on the one from the
|ZEPHYR|, with some additions.

Zephyr's build and configuration system
***************************************

Zephyr's build and configuration system uses the following building blocks
as a foundation:

* CMake, the cross-platform build system generator.
* Kconfig, a powerful configuration system also used in the Linux kernel.
* Devicetree, a hardware description language that is used to describe the
  hardware that |BRIDLE| is to run on.

Since the build and configuration system used by |BRIDLE| comes from the
|ZEPHYR|, references to the original |ZEPHYR| documentation are provided here
in order to avoid duplication. See the following links for information about
the different building blocks mentioned above:

* :zephyr:ref:`application` is a complete guide to application development
  with Zephyr, including the build and configuration system.
* :zephyr:ref:`cmake-details` describes in-depth the usage of CMake for
  Zephyr-based applications.
* :zephyr:ref:`application-kconfig` contains a guide for Kconfig usage
  in applications.
* :zephyr:ref:`set-devicetree-overlays` explains how to use devicetree
  and its overlays to customize an application's devicetree.

|BRIDLE| additions
******************

|BRIDLE| adds some functionality on top of the |ZEPHYR| build and configuration
system. Those additions are automatically included into the |ZEPHYR| build
system using a :zephyr:ref:`cmake_build_config_package`.

You must be aware of these additions when you start writing your own
Bridle applications.

* |BRIDLE| provides an additional set of :file:`*.cmake` module files that
  are automatically included when using the |ZEPHYR| CMake package in the
  :file:`CMakeLists.txt` file of your application::

    find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

  Also it is possible and the **default use case** to using the
  Bridle CMake package (that automatically includes the |ZEPHYR|)
  in the :file:`CMakeLists.txt` file of your application::

    find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})

* |BRIDLE| allows you to
  :ref:`create custom build type files <gs_modifying_build_types>` instead
  of using a single :file:`prj.conf` file.

.. * The |BRIDLE| build system extends Zephyr's with support for multi-image builds.
..   You can find out more about these in the :ref:`ug_multi_image` section.
.. * |BRIDLE| adds a partition manager, responsible for partitioning the available flash memory.
