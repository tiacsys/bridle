.. _bridle_release_notes_320:

|BRIDLE| 3.2.0 Release Notes
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
     - v3.2-branch
     - v3.2.0
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
     - | tiacsys/v3.2-branch
       | (v3.2-branch)
     - v3.2.0


Supported boards
****************

* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.2

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Bump to required Zephyr SDK v0.15.2 and protect by Zyphyr SDK version guard.
* Update API terminology for I2C. Replaces 'master' with 'controller'
  and 'slave' with 'target'.
* Migrate all includes to <zephyr/...>.
* Introduce and migrate all includes to <bridle/...>.
* Remove label properties from devicetrees, they are not required anymore.
* Fix loopback test suites, missing prescaler value, SPI setup new ztest API.

Documentation
=============

1. Use Sphinx 5.x and breathe 4.34.x for documentation processing.
#. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.2, based on Zephyr v3.2 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`60` - [FCR] Bump to Zephyr v3.2
* :github:`68` - [BUG] Upgrade to Sphinx 5.x
