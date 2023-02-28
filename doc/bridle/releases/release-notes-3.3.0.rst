.. _bridle_release_notes_330:

|BRIDLE| 3.3.0 Release Notes (Working draft)
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
     - v3.3-branch
     - v3.3.0
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
       | picolibc
       | segger
       | tinycbor
       | tinycrypt
     - | tiacsys/v3.3-branch
       | (v3.3-branch)
     - v3.3.0


Supported boards
****************

* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.3

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Use device tree to configure RTC counter driver instead of Kconfig on STM32 for:

  * RTC source clock selection (use domain clock)
  * LSE drive capability (use lse property)

Documentation
=============

1. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.3, based on Zephyr v3.3 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`72` - [FCR] Bump to Zephyr v3.3
