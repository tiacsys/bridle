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

  * |zephyr:board:native_posix|
  * |zephyr:board:native_sim|
  * |zephyr:board:qemu_x86|
  * |zephyr:board:qemu_cortex_r5|
  * |zephyr:board:qemu_cortex_m0|
  * |zephyr:board:qemu_cortex_m3|
  * ARM Cortex-A9 Emulation (``qemu_cortex_a9``)
  * |zephyr:board:qemu_cortex_a53|
  * |zephyr:board:qemu_kvm_arm64|
  * |zephyr:board:qemu_arc|
  * |zephyr:board:qemu_malta|
  * |zephyr:board:qemu_riscv32e|
  * |zephyr:board:qemu_riscv32|
  * |zephyr:board:qemu_riscv64|
  * |zephyr:board:qemu_xtensa|
  * |zephyr:board:qemu_leon3|
  * |zephyr:board:qemu_nios2|
  * |zephyr:board:nucleo_f303re| (NUCLEO-F303RE)
  * |zephyr:board:nucleo_f401re| (NUCLEO-F401RE)
  * |zephyr:board:nucleo_f413zh| (NUCLEO-F413ZH)
  * |zephyr:board:nucleo_f746zg| (NUCLEO-F746ZG)
  * |zephyr:board:nucleo_f767zi| (NUCLEO-F767ZI)
  * |zephyr:board:mimxrt1010_evk|
  * |zephyr:board:mimxrt1060_evk|
  * |zephyr:board:arduino_zero| or Bridle's |bridle:board:arduino_zero|
  * |bridle:board:seeeduino_cm0|
  * |bridle:board:seeeduino_lotus|
  * |zephyr:board:seeeduino_xiao| or Bridle's |bridle:board:xiao_samd21|
  * |zephyr:board:rpi_pico|
  * |bridle:board:waveshare_rp2040|

Building and Running
********************

This project outputs 'Hello World! I'm THE SHELL' to the console. It can be
built and executed as emulation in |zephyr:board:qemu_x86| as follows:

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :build-dir: helloshell-qemu_x86
   :board: qemu_x86
   :west-args: -p
   :goals: run
   :host-os: unix

Also it can be built and executed on following targets:

* As |zephyr:board:native_posix|, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-native_posix
     :board: native_posix
     :west-args: -p
     :goals: run
     :host-os: unix

  .. hint:: Connect a terminal emulator to the given pseudotty or start the
     application directly with the autoconnect argument:

     .. code-block:: console

        ./build/helloshell-native_posix/zephyr/zephyr.exe -attach_uart

* As emulation in |zephyr:board:qemu_cortex_m3|, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-qemu_cortex_m3
     :board: qemu_cortex_m3
     :west-args: -p
     :goals: run
     :host-os: unix

  .. hint:: Exit QEMU by pressing :kbd:`CTRL+A` :kbd:`x`.

* On |zephyr:board:nucleo_f746zg| board, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

Further you can deside either to run in a basic or fancy command set
mode:

* On |zephyr:board:nucleo_f746zg| board, basic command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :conf: prj-minimal.conf
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

* On |zephyr:board:nucleo_f746zg| board, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :conf: prj.conf
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

Sample Output
=============

(text in bold is a command input, text in angle brackets are keys to press)

.. parsed-literal::
   :class: highlight-console notranslate

   Hello World! I'm THE SHELL from nucleo_f746zg


   :bgn:`uart:~$` **<Tab>**
     :bcy:`adc        bridle     clear      dac        device     devmem     eeprom`
     :bcy:`flash      gpio       hello      help       history    hwinfo     i2c`
     :bcy:`kernel     led        log        pwm        regulator  rem        resize`
     :bcy:`retval     rtc        sensor     shell      timer`

   :bgn:`uart:~$` **help**
   Please press the <Tab> button to see all available commands.
   You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
   You can try to call commands with <-h> or <--help> parameter for more information.

   Shell supports following meta-keys:
     Ctrl + (a key from: abcdefklnpuw)
     Alt  + (a key from: bf)
   Please refer to shell documentation for more details.

   Available commands:
     adc        : ADC commands
     bridle     : Bridle commands.
     clear      : Clear screen.
     dac        : DAC shell commands
     device     : Device commands
     devmem     : Read/write physical memory
                  Usage:
                  Read memory at address with optional width:
                  devmem address [width]
                  Write memory at address with mandatory width and value:
                  devmem address <width> <value>
     eeprom     : EEPROM shell commands
     flash      : Flash shell commands
     gpio       : GPIO commands
     hello      : say hello
     help       : Prints the help message.
     history    : Command history.
     hwinfo     : HWINFO commands
     i2c        : I2C commands
     kernel     : Kernel commands
     led        : LED commands
     log        : Commands for controlling logger
     pwm        : PWM shell commands
     regulator  : Regulator playground
     rem        : Ignore lines beginning with 'rem '
     resize     : Console gets terminal screen size or assumes default in case the
                  readout fails. It must be executed after each terminal width
                  change to ensure correct text display.
     retval     : Print return value of most recent command
     sensor     : Sensor commands
     shell      : Useful, not Unix-like shell commands.
     timer      : Timer commands

   :bgn:`uart:~$` **hello -h**
   hello - say hello
   :bgn:`uart:~$` **hello**
   Hello from shell.

   :bgn:`uart:~$` **kernel version**
   Zephyr version |zephyr_version_number_em|

   :bgn:`uart:~$` **bridle version**
   Bridle version |version_number_em|

   :bgn:`uart:~$` **bridle version long**
   Bridle version |longversion_number_em|

   :bgn:`uart:~$` **bridle info**
   Zephyr: |zephyr_release_number_em|
   Bridle: |release_number_em|

   :bgn:`uart:~$` **kernel uptime**
   Uptime: 327750 ms

   :bgn:`uart:~$` **kernel cycles**
   cycles: 3586181929 hw cycles

   :bgn:`uart:~$` **kernel threads**
   Scheduler: 498 since last call
   Threads:
    0x20010e58
           options: 0x0, priority: -16 timeout: 0
           state: pending, entry: 0x8002339
           stack size 2048, unused 1920, usage 128 / 2048 (6 %)

   \*0x20010ac0 shell_uart
           options: 0x0, priority: 14 timeout: 0
           state: queued, entry: 0x8004c59
           stack size 2048, unused 1016, usage 1032 / 2048 (50 %)

    0x20011728 sysworkq
           options: 0x1, priority: -1 timeout: 0
           state: pending, entry: 0x800ebfd
           stack size 1024, unused 848, usage 176 / 1024 (17 %)

    0x200105c0 logging
           options: 0x0, priority: 14 timeout: 0
           state: pending, entry: 0x8002a21
           stack size 768, unused 584, usage 184 / 768 (23 %)

    0x200114c8 idle
           options: 0x1, priority: 15 timeout: 0
           state: , entry: 0x8014571
           stack size 320, unused 256, usage 64 / 320 (20 %)

   :bgn:`uart:~$` **kernel stacks**
   0x20010e58                                  (real size 2048):   unused 1920     usage  128 / 2048 ( 6 %)
   0x20010ac0 shell_uart                       (real size 2048):   unused  944     usage 1104 / 2048 (53 %)
   0x20011728 sysworkq                         (real size 1024):   unused  848     usage  176 / 1024 (17 %)
   0x200105c0 logging                          (real size  768):   unused  584     usage  184 /  768 (23 %)
   0x200114c8 idle                             (real size  320):   unused  256     usage   64 /  320 (20 %)
   0x20015e80 IRQ 00                           (real size 2048):   unused 1816     usage  232 / 2048 (11 %)

   :bgn:`uart:~$` **_**
