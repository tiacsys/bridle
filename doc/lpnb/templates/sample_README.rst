.. _sample:

Sample template
###############

.. note:: Sections with character :sup:`*` on end of name are optional.

The XYZ sample application demonstrates how to work with X in the rhythm
of the Y that is played by Z.

.. tip:: Explain what this example demonstrates in one, max two sentences
   (full sentences, not sentence fragments). You can go into more detail
   in the next section.

Overview
********

You can use this sample application as a starting point to implement
your own XYZ thing.

The sample applicaton uses the ``:ref:RST link`` library to control the X.
In addition, it uses the ``:ref:RST link`` Y access and hooks up to some
internet service to download cool Z sequences.

.. tip:: Continue the explanation on what this example is about. What does
   it show, and why should users try it out? What is the practical use? How
   can users extend this example? What libraries are used? When linking,
   link to the conceptual documentation of other modules - these will in
   turn link to or contain the API documentation.

Some title\ :sup:`*`
====================

.. note:: Add subsections for technical details. Give them a suitable title
   (sentence style capitalization, thus only the first word capitalized).

The sample application repeatedly calls function ABC, which ...

.. tip:: Do not state what people can see and understand from looking at
   the code. Instead, clarify general concepts or explain parts of the
   implementation that might be unintuitive for some reason. If there's
   nothing important to point out, do not include any subsections.

Requirements
************

* One of the following development boards:

  * :ref:`zephyr:nucleo_f746zg_board` (NUCLEO-F746ZG)

* A Y account.
* A Z ball.

.. tip:: Unless the sample is meant to go upstream, require a specific board,
   not "any board with Ethernet". Be specific - "any Ethernet board" will also
   mean all boards with Ethernet, but without LED power drivers ... When
   listing the supported boards, give both the name (ST Nucleo F746ZG board)
   and the board number (NUCLEO-F746ZG).

Wiring\ :sup:`*`
****************

Connect PIN1 to PIN2, then cut the connection again.

User interface\ :sup:`*`
************************

Button 1:
   Start or stop the XYZ show.

.. tip:: Add Button and LED assignments here, plus other information
   related to the user interface.

Building and Running
********************

.. |sample path| replace:: :file:`samples/XXX`

.. include:: /includes/build_and_run.txt

Testing
=======

After programming the sample to your board, test it by performing the
following steps:

#. Connect to the board with some tool.
#. UART settings.
#. Press a button on the board.
#. Look at the flashing lights.
#. And so on ...

Sample output\ :sup:`*`
=======================

The following output is logged on [UART console|RTT]::

   whatever

Troubleshooting\ :sup:`*`
=========================

If the X do not start working with Y, check if the Z is valid enough.

Dependencies\ :sup:`*`
**********************

This sample uses the following |LPNB| libraries:

* :ref:`customservice_readme`

In addition, it uses the following Zephyr libraries:

* ``include/console.h``
* :ref:`zephyr:kernel_api`:

  * ``include/kernel.h``

.. tip:: If possible, link to the respective library. If there is no
   documentation for the library, include the path.

Known issues and limitations\ :sup:`*`
**************************************

The sample only works with good Z.

References\ :sup:`*`
********************

* Z chapter in the Ethernet Spec (-> always link)
* Z ball datasheet

.. tip:: Do not include links to documents that are common to all or many of
   samples. For example, the Ethernet Spec or the DK user guides are always
   important, but shouldn't be listed. Include specific links, like a chapter
   in the Ethernet Spec if the sample demonstrates the respective feature, or
   a link to the hardware pictures in the DK user guide if there is a lot of
   wiring required, or specific information about the feature that is
   presented in the sample.
