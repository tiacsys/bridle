.. _bridle_release_notes_260:

|BRIDLE| 2.6.0 Release Notes (Working draft)
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
     - v2.6-branch
     - v2.6.0
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
     - | tiacsys/v2.6-branch
       | (v2.6-branch)
     - v2.6.0


Supported boards
****************

* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v2.6

Build Infrastructure
====================

Take over the new principles to build documentations from Zephyr:

* Control different build targets over one central (template)
  cmake funktion to create comparable documentation set rules.
* With help of the new Sphinx extension *inventory_builder* each
  documentation set can build their own inventory object file to
  be able to split one document into multiple smaller documents
  and use intersphinx for inter-link resolution of all references.
* Known warnings now will be filterd by the new Sphinx extention
  *warnings_filter* as provided with Zephyr and not anymore outside
  the Sphinx build runner anywhere on CI/CD or cmake level.
* All scattered documentation sources are no longer merged by cmake
  in the build folder but by the new Sphinx plugin *external_content*.

Documentation
=============

Use our own Sphinx theme PyPi package, `sphinx-tsn-theme`_, forked
from `sphinx-ncs-theme`_.

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`39` - [FCR] Bump to Zephyr v2.6
