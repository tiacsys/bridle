.. _bridle_release_notes_270:

|BRIDLE| 2.7.0 Release Notes (Working draft)
############################################

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
     - v2.7-branch
     - v2.7.0
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
     - | tiacsys/v2.7-branch
       | (v2.7-branch)
     - v2.7.0


Supported boards
****************

* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v2.7

Build Infrastructure
====================

Take over the new principles to build documentations from Zephyr:

* The kconfig-role extension is now required.
* The Graphviz (dot) package is now required.

Documentation
=============

*NOT YET*

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`49` - Can't rebuild documentation
* :github:`53` - [FCR] Bump to Zephyr v2.7
