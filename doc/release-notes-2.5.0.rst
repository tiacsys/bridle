.. _bridle_release_notes_250:

|BRIDLE| 2.5.0 Release Notes (Working draft)
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
     - v2.5-branch
     - v2.5.0
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
     - | tiacsys/v2.5-branch
       | (v2.5-branch)
     - v2.5.0


Supported boards
****************

* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* INITIAL PROJECT SETUP on |TIAC| `DevZone`_

Build Infrastructure
====================

* Created first draft CI/CD pipeline with GitHub Actions and their
  workflows:

  - QA Integration Test
  - QA Compliance Check
  - QA License Check
  - QA Manifest Check and Labeler
  - Documentation Build and Publish

Documentation
=============

* Created first draft including documentation for selected samples
  and libraries.
