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
* fancy command set, with default enabled :kconfig:option:`CONFIG_BRIDLE_CMD_HELLO`

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


   Please press the <Tab> button to see all available commands.
   You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
   You can try to call commands with <-h> or <--help> parameter for more information.

   Shell supports following meta-keys:
     Ctrl + (a key from: abcdefklnpuw)
     Alt  + (a key from: bf)
   Please refer to shell documentation for more details.

   Available commands:
     adc      :ADC commands
     bridle   :Bridle commands.
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
     adc      bridle   clear    device   flash    gpio     hello    help
     history  hwinfo   i2c      kernel   log      pwm      resize   sensor
     shell

   uart:~$ hello -h
   hello - say hello
   uart:~$ hello
   Hello from shell.

   uart:~$ kernel version
   Zephyr version 3.3.0

   uart:~$ bridle version
   Bridle version 3.3.1

   uart:~$ kernel uptime
   Uptime: 254707293 ms

   uart:~$ kernel cycles
   cycles: 4281597339 hw cycles

   uart:~$ kernel threads
   Threads:
    0x20020d28 sysworkq
           options: 0x0, priority: -1 timeout: 0
           state: pending, entry: 0x800b169
           stack size 1024, unused 864, usage 160 / 1024 (15 %)

   *0x200208f8 shell_uart
           options: 0x0, priority: 14 timeout: 0
           state: queued, entry: 0x80044b9
           stack size 2048, unused 1136, usage 912 / 2048 (44 %)

    0x20020840 logging
           options: 0x0, priority: 14 timeout: 0
           state: pending, entry: 0x8002555
           stack size 768, unused 664, usage 104 / 768 (13 %)

    0x20020bb0 idle 00
           options: 0x1, priority: 15 timeout: 0
           state: , entry: 0x800e501
           stack size 320, unused 272, usage 48 / 320 (15 %)

   uart:~$ kernel stacks
   0x20020d28 sysworkq   (real size 1024):	unused 864	usage 160 / 1024 (15 %)
   0x200208f8 shell_uart (real size 2048):	unused 1096	usage 952 / 2048 (46 %)
   0x20020840 logging    (real size 768):	unused 664	usage 104 / 768 (13 %)
   0x20020bb0 idle 00    (real size 320):	unused 272	usage 48 / 320 (15 %)
   0x20023580 IRQ 00     (real size 2048):	unused 1484	usage 564 / 2048 (27 %)

   uart:~$ _
