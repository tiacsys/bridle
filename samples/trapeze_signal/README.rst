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
The units were adjusted to fit the requirements. This consists primarily of using *steps/s* for motor speed and using time in s instead of 
counter ticks to measure time.

Thus the acceleration is :math:`a = \frac{v^{2}}{2*accel\_steps}`.
With this the first period duration is :math:`t_0=\sqrt{\frac{2*1\ step}{a}}` (with pulse duration half of that).

Thus the calculation for the duration of period :math:`n` is :math:`t_n=t_0(\sqrt{n+1}-\sqrt{n})`

As this calculation is very expensive, an approximation based on a Taylor series is used above a certain :math:`n`:

:math:`\sqrt{1\pm \frac{1}{n}}=1\pm\frac{1}{2n}-\frac{1}{8n^2}+O\left( \frac{1}{n^3} \right)`

This is used in :math:`\frac{t_n}{t_{n+1}}=\frac{t_0(\sqrt{n+1}-\sqrt{n})}{t_0(\sqrt{n}-\sqrt{n-1})}=\frac{\sqrt{1+\frac{1}{n}}-1}{1-\sqrt{1-\frac{1}{n}}}`

Resulting in 
   .. math::
      \frac{t_n}{t_{n-1}}=\frac{4n-1}{4n+1}

To get an iterative algorithm from this, the equation needs to be solved for :math:`t_n` (acceleration) and :math:`t_{n-1}` for deceleration.

Acceleration:
   .. math::
      \frac{t_n}{t_{n-1}}=\frac{4n-1}{4n+1}

      t_n=t_{n-1}\frac{4n-1}{4n+1}=t_{n-1}\left( \frac{4n-1+4n+1-4n-1}{4n+1} \right)

      t_n=t_{n-1}\left( \frac{4n+1}{4n+1}-\frac{2}{4n+1} \right)=t_{n-1}\left( 1-\frac{2}{4n+1} \right) = t_{n-1}-\frac{2t_{n-1}}{4n+1}

Deceleration:
   .. math::
      \frac{t_{n-1}}{t_{n}}=\frac{4n+1}{4n-1}

      t_{n-1}=t_{n}\frac{4n+1}{4n-1}=t_{n}\left( \frac{4n+1+4n-1-4n+1}{4n-1} \right)

      t_{n-1}=t_{n}\left( \frac{4n-1}{4n-1}+\frac{2}{4n-1} \right)=t_{n}\left( 1+\frac{2}{4n-1} \right) = t_{n}+\frac{2t_{n}}{4n-1}