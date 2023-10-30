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
  * :ref:`zephyr:native_sim`
  * :ref:`zephyr:qemu_x86`
  * :ref:`zephyr:qemu_cortex_r5`
  * :ref:`zephyr:qemu_cortex_m0`
  * :ref:`zephyr:qemu_cortex_m3`
  * ARM Cortex-A9 Emulation (``qemu_cortex_a9``)
  * :ref:`zephyr:qemu_cortex_a53`
  * :ref:`zephyr:qemu_kvm_arm64`
  * :ref:`zephyr:qemu_arc`
  * :ref:`zephyr:qemu_malta`
  * :ref:`zephyr:qemu_riscv32e`
  * :ref:`zephyr:qemu_riscv32`
  * :ref:`zephyr:qemu_riscv64`
  * :ref:`zephyr:qemu_xtensa`
  * :ref:`zephyr:qemu_leon3`
  * :ref:`zephyr:qemu_nios2`
  * :ref:`zephyr:nucleo_f303re_board` (NUCLEO-F303RE)
  * :ref:`zephyr:nucleo_f401re_board` (NUCLEO-F401RE)
  * :ref:`zephyr:nucleo_f413zh_board` (NUCLEO-F413ZH)
  * :ref:`zephyr:nucleo_f746zg_board` (NUCLEO-F746ZG)
  * :ref:`zephyr:nucleo_f767zi_board` (NUCLEO-F767ZI)
  * :ref:`zephyr:mimxrt1010_evk`
  * :ref:`zephyr:mimxrt1060_evk`
  * :ref:`zephyr:arduino_zero` or Bridle's :ref:`arduino_zero`
  * :ref:`seeeduino_lotus`
  * :ref:`zephyr:seeeduino_xiao` or Bridle's :ref:`seeed_xiao_samd21`
  * :ref:`zephyr:rpi_pico`
  * :ref:`waveshare_rp2040`

Building and Running
********************

This project outputs 'Hello World! I'm THE SHELL' to the console. It can be
built and executed as emulation in :ref:`zephyr:qemu_x86` as follows:

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :build-dir: helloshell-qemu_x86
   :board: qemu_x86
   :west-args: -p
   :goals: build run
   :host-os: unix

Also it can be built and executed on following targets:

* As :ref:`zephyr:native_posix`, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-native_posix
     :board: native_posix
     :west-args: -p
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
     :west-args: -p
     :goals: build run
     :host-os: unix

  .. hint:: Exit QEMU by pressing :kbd:`CTRL+A` :kbd:`x`.

* On :ref:`zephyr:nucleo_f746zg_board` board, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :board: nucleo_f746zg
     :west-args: -p
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
     :west-args: -p
     :goals: build flash
     :host-os: unix

* On :ref:`zephyr:nucleo_f746zg_board` board, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :conf: prj.conf
     :board: nucleo_f746zg
     :west-args: -p
     :goals: build flash
     :host-os: unix

Sample Output
=============

.. code-block:: console

   Hello World! I'm THE SHELL from nucleo_f746zg


   uart:~$ <Tab>
     adc        bridle     clear      dac        device     devmem     flash
     gpio       hello      help       history    hwinfo     i2c        kernel
     led        log        pwm        regulator  rem        resize     retval
     sensor     shell      timer

   uart:~$ help
   Please press the <Tab> button to see all available commands.
   You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
   You can try to call commands with <-h> or <--help> parameter for more information.

   Shell supports following meta-keys:
     Ctrl + (a key from: abcdefklnpuw)
     Alt  + (a key from: bf)
   Please refer to shell documentation for more details.

   Available commands:
     adc        :ADC commands
     bridle     :Bridle commands.
     clear      :Clear screen.
     dac        :DAC shell commands
     device     :Device commands
     devmem     :Read/write physical memory
                 Usage:
                 Read memory at address with optional width:
                 devmem address [width]
                 Write memory at address with mandatory width and value:
                 devmem address <width> <value>
     flash      :Flash shell commands
     gpio       :GPIO commands
     hello      :say hello
     help       :Prints the help message.
     history    :Command history.
     hwinfo     :HWINFO commands
     i2c        :I2C commands
     kernel     :Kernel commands
     led        :LED commands
     log        :Commands for controlling logger
     pwm        :PWM shell commands
     regulator  :Regulator playground
     rem        :Ignore lines beginning with 'rem '
     resize     :Console gets terminal screen size or assumes default in case the
                 readout fails. It must be executed after each terminal width
                 change to ensure correct text display.
     retval     :Print return value of most recent command
     sensor     :Sensor commands
     shell      :Useful, not Unix-like shell commands.
     timer      :Timer commands

   uart:~$ hello -h
   hello - say hello
   uart:~$ hello
   Hello from shell.

   uart:~$ kernel version
   Zephyr version 3.5.0

   uart:~$ bridle version
   Bridle version 3.5.0

   uart:~$ kernel uptime
   Uptime: 254707293 ms

   uart:~$ kernel cycles
   cycles: 4281597339 hw cycles

   uart:~$ kernel threads
   Scheduler: 328 since last call
   Threads:
    0x20021650 sysworkq
	   options: 0x0, priority: -1 timeout: 0
	   state: pending, entry: 0x800e4f9
	   stack size 1024, unused 832, usage 192 / 1024 (18 %)

   *0x20020a80 shell_uart
	   options: 0x0, priority: 14 timeout: 0
	   state: queued, entry: 0x8004e75
	   stack size 2048, unused 1016, usage 1032 / 2048 (50 %)

    0x20020588 logging
	   options: 0x0, priority: 14 timeout: 0
	   state: pending, entry: 0x8002bad
	   stack size 768, unused 584, usage 184 / 768 (23 %)

    0x200214c0 idle
	   options: 0x1, priority: 15 timeout: 0
	   state: , entry: 0x80134c3
	   stack size 320, unused 256, usage 64 / 320 (20 %)

   uart:~$ kernel stacks
   0x20021650 sysworkq   (real size 1024):	unused  832	usage  192 / 1024 (18 %)
   0x20020a80 shell_uart (real size 2048):	unused  944	usage 1104 / 2048 (53 %)
   0x20020588 logging    (real size  768):	unused  584	usage  184 /  768 (23 %)
   0x200214c0 idle       (real size  320):	unused  256	usage   64 /  320 (20 %)
   0x20025400 IRQ 00     (real size 2048):	unused 1684	usage  364 / 2048 (17 %)

   uart:~$ _
