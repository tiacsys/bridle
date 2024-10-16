.. _trapezesignal:

Trapeze Signal
###############

Overview
********
This sample provides an example of trapeze signal application using :ref:`Counter API <zephyr:counter_api>`.
It generates as signal with trapeze timings on a gpio port. The signal is intended for use with stepper
motors that are driven by a step signal. The sample was written for the drv84xx series of drivers, hence using their microstep resolution.


Requirements
************

This sample requires the support of a timer IP compatible with top interrupt.

This sample requires 1-3 gpio ports (2 can be disabled in code).

References
**********

- :ref:`nucleo_f767zi_board`


Building and Running
********************

 .. zephyr-app-commands::
    :app: bridle/samples/trapeze_signal
    :build-dir: trapeze_signal-nucleo_f767zi
    :board: nucleo_f767zi
    :goals: run
    :host-os: unix

Sample Output
*************

 .. code-block:: console

    Trapeze signal sample

    Finished

The trapeze signal will be outputted on the corresponding gpio port and can be detected for example via an led, stepper motor or oscilloscope.

Background
**********

The algorithm for this sample is based on *Generate stepper-motor speed profiles in real time* by David Austin from 2005.
