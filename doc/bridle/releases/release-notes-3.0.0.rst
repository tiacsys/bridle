.. _bridle_release_notes_300:

|BRIDLE| 3.0.0 Release Notes
############################

This project demonstrate the integration of |TIAC| support in open
source projects, like the Zephyr RTOS, with libraries and source code
for applications. It is not yet intended or supported by |TIAC| for
product development.

Highlights
**********

* Added proper build infrastructure.

.. note:: See the changelog and readme files in the component repositories
   for a detailed description of changes.

Repositories
************

.. list-table::
   :header-rows: 1

   * - Component
     - Imports
     - Branch
     - Tag
   * - `tiac-bridle`_
     -
     - v3.0-branch
     - v3.0.0
   * - | `tiac-zephyr`_
       | (`zephyr-core`_)
     - | canopennode
       | cmsis
       | civetweb
       | edtt
       | fatfs
       | hal_altera
       | hal_espressif
       | hal_stm32
       | hal_xtensa
       | libmetal
       | littlefs
       | loramac-node
       | lvgl
       | mbedtls
       | mcumgr
       | mipi-sys-t
       | net-tools
       | open-amp
       | openthread
       | segger
       | tinycbor
       | tinycrypt
     - | tiacsys/v3.0-branch
       | (v3.0-branch)
     - v3.0.0


Supported boards
****************

* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.0

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Complete independent handling of the Kconfig documentation.
* Restructure CMake integration for mos of all docsets.
* Use the Zephyr Build Configuration CMake package to load our own
  boilerplate automatically through ZephyrBuildConfig.cmake.

Documentation
=============

1. Renamed references to :ref:`canbus` in the :ref:`tiac_magpie_board` page.
#. Update all documentat output messages.

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`54` - [FCR] Bump to Zephyr v3.0
