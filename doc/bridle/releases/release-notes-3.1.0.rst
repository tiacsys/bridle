.. _bridle_release_notes_310:

|BRIDLE| 3.1.0 Release Notes
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
     - v3.1-branch
     - v3.1.0
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
     - | tiacsys/v3.1-branch
       | (v3.1-branch)
     - v3.1.0


Supported boards
****************

* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.1

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Refactoring to to support the new searchable Kconfig documentation.
* Merge search index to find tags from all docsets within each docset.
* Restructure CMake integration for most of all docsets.
* Extend CMake package configuration to support ``find_package("Bridle")``.
* Introduce new :zephyr:ref:`west` command extension: ``west bridle-export``.
* Split and differentiate the Bridle boilerplate: defaults, doc, version.
* Provide a first version of a common CMake find script for Sphinx.
* Provide a first version of an Zyphyr SDK version guard.
* Extend the Zephyr Build Configuration CMake package with many sequences
  copied from the corresponding Zephyr CMake scripts.

Documentation
=============

1. Renamed references to :zephyr:ref:`kconfig` in the
   :ref:`magpie_f777ni_board` page.
#. Update all documented output messages.

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`59` - [FCR] Bump to Zephyr v3.1
