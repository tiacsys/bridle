.. _helloshell:

Hello Shell
###########

**This is a derived work from the original Zephyr "Hello World" example!**
**Most of the stuff in this README file needs to be redesigned and changed!**

Overview
********

A simple Hello World example that can be used with any supported board and
prints 'Hello World! I'm THE SHELL' to the console. This application can be
built into modes:

* basic command set
* fancy command set, with default enabled :option:`CONFIG_BRIDLE_CMD_HELLO`

Requirements
************

* One of the following development boards:

  * :ref:`zephyr:native_posix`
  * :ref:`zephyr:qemu_x86`
  * :ref:`zephyr:qemu_cortex_m3`
  * :ref:`zephyr:nucleo_f746zg_board` (NUCLEO-F746ZG)

Building and Running
********************

This project outputs 'Hello World! I'm THE SHELL' to the console. It can be
built and executed as emulation in :ref:`zephyr:qemu_x86` as follows:

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :build-dir: helloshell-qemu_x86
   :board: qemu_x86
   :goals: build run
   :host-os: unix

Also it can be built and executed on following targets:

* As :ref:`zephyr:native_posix`, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-native_posix
     :board: native_posix
     :goals: build run
     :host-os: unix

  .. hint:: Connect a terminal emulator to the given pseudotty or start the
     application directly with the autoconnect argument:

     .. code-block:: console

        ./build/helloshell-native_posix/zephyr/zephyr.exe -attach_uart

* As emulation in :ref:`zephyr:qemu_cortex_m3`, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-qemu_cortex_m3
     :board: qemu_cortex_m3
     :goals: build run
     :host-os: unix

  .. hint:: Exit QEMU by pressing :kbd:`CTRL+A` :kbd:`x`.

* On :ref:`zephyr:nucleo_f746zg_board` board, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :board: nucleo_f746zg
     :goals: build flash
     :host-os: unix

Further you can deside either to run in a basic or fancy command set
mode:

* On :ref:`zephyr:nucleo_f746zg_board` board, basic command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :conf: prj-minimal.conf
     :board: nucleo_f746zg
     :goals: build flash
     :host-os: unix

* On :ref:`zephyr:nucleo_f746zg_board` board, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :conf: prj.conf
     :board: nucleo_f746zg
     :goals: build flash
     :host-os: unix

Sample Output
=============

.. code-block:: console

   Hello World! I'm THE SHELL from nucleo_f746zg


   uart:~$ help
   Please press the <Tab> button to see all available commands.
   You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
   You can try to call commands with <-h> or <--help> parameter for more information.

   Shell supports following meta-keys:
     Ctrl + (a key from: abcdefklnpuw)
     Alt  + (a key from: bf)
   Please refer to shell documentation for more details.

   Available commands:
     adc      :ADC commands
     clear    :Clear screen.
     device   :Device commands
     flash    :Flash shell commands
     gpio     :GPIO commands
     hello    :say hello
     help     :Prints the help message.
     history  :Command history.
     hwinfo   :HWINFO commands
     i2c      :I2C commands
     kernel   :Kernel commands
     log      :Commands for controlling logger
     pwm      :PWM shell commands
     resize   :Console gets terminal screen size or assumes default in case the
               readout fails. It must be executed after each terminal width change
               to ensure correct text display.
     sensor   :Sensor commands
     shell    :Useful, not Unix-like shell commands.

   uart:~$ <Tab>
     clear    device   gpio     hello    help     history  kernel   log
     resize   shell

   uart:~$ hello -h
   hello - say hello
   uart:~$ hello
   Hello from shell.

   uart:~$ kernel version
   Zephyr version 2.5.0

   uart:~$ kernel uptime
   Uptime: 254707293 ms

   uart:~$ kernel cycles
   cycles: 4281597339 hw cycles

   uart:~$ kernel threads
   Threads:
   *0x20010318 shell_uart
           options: 0x0, priority: 14 timeout: 536937364
           state: queued
           stack size 2048, unused 1184, usage 864 / 2048 (42 %)

    0x20010260 logging
           options: 0x0, priority: 14 timeout: 536937180
           state: pending
           stack size 768, unused 664, usage 104 / 768 (13 %)

    0x200103d0 idle 00
           options: 0x1, priority: 15 timeout: 536937548
           state:
           stack size 320, unused 248, usage 72 / 320 (22 %)

   uart:~$ kernel stacks
   0x20010318 shell_uart (real size 2048): unused 1184     usage 864 / 2048 (42 %)
   0x20010260 logging    (real size 768):  unused 664      usage 104 / 768 (13 %)
   0x200103d0 idle 00    (real size 320):  unused 248      usage 72 / 320 (22 %)
   0x20011be0 IRQ 00     (real size 2048): unused 1560     usage 488 / 2048 (23 %)

   uart:~$ _
