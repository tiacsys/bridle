.. _gs_testing:

Testing a sample application
############################

.. contents::
   :local:
   :depth: 2

Follow the instructions in the testing section of the sample documentation
to ensure that the application runs as expected.

Information about the current state of the application is usually provided
through the LEDs or through UART, or through both. See the user interface
section of the sample documentation for description of the LED states or
available UART commands.

.. _testing_putty:

How to connect with PuTTY
*************************

To see the UART output, connect to the board hardware with a terminal emulator,
for example, PuTTY.

Connect with the following settings:

* Baud rate: 115200
* 8 data bits
* 1 stop bit
* No parity
* HW flow control: None

If you want to send commands via UART, make sure to configure the required line
endings and turn on local echo and local line editing:

.. TEMP-OFF for PDF with "rinoh"
.. .. figure:: /images/putty.svg
.. figure:: /images/putty.*
   :alt: PuTTY configuration for sending commands via UART

.. UART can also be used for logging purposes as one of the
   :ref:`logging backends <ug_logging_backends>`.
