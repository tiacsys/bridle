.. _magpie_f777ni_helloshell-sample:

Hello Shell
###########

Overview
********

See :ref:`helloshell-sample` for the original description.

.. _magpie_f777ni_helloshell-sample-requirements:

Requirements
************

The TiaC Magpie with already configured UART console support.

Building and Running
********************

Build and flash Hello Shell as follows:

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :build-dir: helloshell-magpie_f777ni
   :board: magpie_f777ni
   :west-args: -p
   :goals: flash
   :host-os: unix

After flashing and the board has booted, you will be presented with a shell
prompt. All shell commands are available and would looks like:

(text in bold is a command input, text in angle brackets are keys to press)

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      Hello World! I'm THE SHELL from magpie_f777ni


      :bgn:`uart:~$` **<Tab>**
        :bcy:`adc        bridle     clear      dac        device     devmem     eeprom`
        :bcy:`flash      gpio       hello      help       history    hwinfo     i2c`
        :bcy:`kernel     led        log        pwm        regulator  rem        resize`
        :bcy:`retval     sensor     shell      timer`

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

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **hello -h**
      hello - say hello
      :bgn:`uart:~$` **hello**
      Hello from shell.

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **hwinfo devid**
      Length: 12
      ID: 0x9e6b44aea1e2b8980c4d32a6

      :bgn:`uart:~$` **kernel version**
      Zephyr version |zephyr_version_number_em|

      :bgn:`uart:~$` **bridle version**
      Bridle version |shortversion_number_em|

      :bgn:`uart:~$` **bridle version long**
      Bridle version |longversion_number_em|

      :bgn:`uart:~$` **bridle info**
      Zephyr: |zephyr_release_number_em|
      Bridle: |release_number_em|

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **device list**
      devices:
      - rcc\ @\ 40023800 (READY)
        DT node labels: rcc
      - reset-controller (READY)
        DT node labels: rctl
      - interrupt-controller\ @\ 40013c00 (READY)
        DT node labels: exti
      - gpio\ @\ 40022800 (READY)
        DT node labels: gpiok
      - gpio\ @\ 40022400 (READY)
        DT node labels: gpioj
      - gpio\ @\ 40022000 (READY)
        DT node labels: gpioi
      - gpio\ @\ 40021C00 (READY)
        DT node labels: gpioh
      - gpio\ @\ 40021800 (READY)
        DT node labels: gpiog
      - gpio\ @\ 40021400 (READY)
        DT node labels: gpiof
      - gpio\ @\ 40021000 (READY)
        DT node labels: gpioe
      - gpio\ @\ 40020C00 (READY)
        DT node labels: gpiod
      - gpio\ @\ 40020800 (READY)
        DT node labels: gpioc
      - gpio\ @\ 40020400 (READY)
        DT node labels: gpiob
      - gpio\ @\ 40020000 (READY)
        DT node labels: gpioa
      - serial\ @\ 40007800 (READY)
        DT node labels: uart7
      - serial\ @\ 40004c00 (READY)
        DT node labels: uart4 tmph_serial1 tmph_serial
      - rtc\ @\ 40002800 (READY)
        DT node labels: rtc
      - adc\ @\ 40012200 (READY)
        DT node labels: adc3 tmph_adc
      - flash-controller\ @\ 40023c00 (READY)
        DT node labels: flash
      - i2c\ @\ 40006000 (READY)
        DT node labels: i2c4 tmph_i2c1 tmph_i2c
      - i2c\ @\ 40005800 (READY)
        DT node labels: i2c2
      - pwm (READY)
        DT node labels: pwm8 tmph_pwms
      - spi\ @\ 40013400 (READY)
        DT node labels: spi4 tmph_spi1 tmph_spi
      - leds (READY)

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **history**
      [  0] history
      [  1] device list
      [  2] bridle info
      [  3] bridle version long
      [  4] bridle version
      [  5] kernel version
      [  6] hwinfo devid
      [  7] hello
      [  8] hello -h
      [  9] help

Simple GPIO Operations
======================

.. rubric:: Switch user LED 2 on and off

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **gpio get gpio@40021800 12**
      0

      :bgn:`uart:~$` **gpio conf gpio@40021800 12 oh0**

      :bgn:`uart:~$` **gpio set gpio@40021800 12 1**
      :bgn:`uart:~$` **gpio set gpio@40021800 12 0**

      :bgn:`uart:~$` **gpio blink gpio@40021800 12**
      Hit any key to exit

.. rubric:: Switch user LED 1 on and off (via LED API)

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **led on leds 0**
      leds: turning on LED 0

      :bgn:`uart:~$` **led off leds 0**
      leds: turning off LED 0

Simple ADC Acquisition
======================

.. rubric:: Read 12-bit from ADC3/IN9

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **adc adc@40012200 acq_time 1 tick**
      :bgn:`uart:~$` **adc adc@40012200 resolution 12**

      :bgn:`uart:~$` **adc adc@40012200 read 9**
      read: 370

      :bgn:`uart:~$` **adc adc@40012200 print**
      adc\ @\ 40012200:
      Gain: 1
      Reference: INTERNAL
      Acquisition Time: 0
      Channel ID: 9
      Differential: 0
      Resolution: 12

Simple RTC Alarm
================

.. rubric:: Oneshot for 1 second by alarm channel 0

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **timer oneshot rtc@40002800 0 1000**
      :bgn:`rtc@40002800: Alarm triggered`

Simple Flash Access and Test
============================

.. rubric:: Print HEX Dump

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **flash read flash-controller@40023c00 17e02 40**
      00017E02: 6d 61 67 70 69 65 5f 66  37 37 37 6e 69 00 48 65 \|magpie_f 777ni.He\|
      00017E12: 6c 6c 6f 20 57 6f 72 6c  64 21 20 49 27 6d 20 54 \|llo Worl d! I'm T\|
      00017E22: 48 45 20 53 48 45 4c 4c  20 66 72 6f 6d 20 25 73 \|HE SHELL  from %s\|
      00017E32: 0a 00 28 75 6e 73 69 67  6e 65 64 29 20 63 68 61 \|..(unsig ned) cha\|

.. rubric:: Erase, Write and Verify

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **flash read flash-controller@40023c00 3c000 40**
      0003C000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
      0003C010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
      0003C020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
      0003C030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

      :bgn:`uart:~$` **flash test flash-controller@40023c00 3c000 1000 2**
      Erase OK.
      Write OK.
      Verified OK.
      Erase OK.
      Write OK.
      Verified OK.
      Erase-Write-Verify test done.

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **flash read flash-controller@40023c00 3c000 40**
      0003C000: 00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f \|........ ........\|
      0003C010: 10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f \|........ ........\|
      0003C020: 20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f \| !"#$%&' ()*+,-./\|
      0003C030: 30 31 32 33 34 35 36 37  38 39 3a 3b 3c 3d 3e 3f \|01234567 89:;<=>?\|

      :bgn:`uart:~$` **flash page_info 3c000**
      Page for address 0x3c000:
      start offset: 0x20000
      size: 131072
      index: 4

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **flash erase flash-controller@40023c00 3c000 1000**
      Erase success.

      :bgn:`uart:~$` **flash read flash-controller@40023c00 3c000 40**
      0003C000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
      0003C010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
      0003C020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
      0003C030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

Simple I2C Operations
=====================

.. rubric:: Scan I2C bus 2

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **i2c scan i2c@40005800**
           0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
      00:             -- -- -- -- -- -- -- -- -- -- -- --
      10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      20: 20 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
      30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      40: 40 41 42 43 44 45 46 -- -- -- -- -- -- -- -- --
      50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      70: -- -- -- -- -- -- -- --
      9 devices found on i2c\ @\ 40005800

.. rubric:: Configure GPIO pins on first IO expander to output

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **i2c read_byte i2c@40005800 20 0**
      Output: 0xc0

      :bgn:`uart:~$` **i2c read_byte i2c@40005800 20 3**
      Output: 0xff

      :bgn:`uart:~$` **i2c write_byte i2c@40005800 20 3 0**
      :bgn:`uart:~$` **i2c read_byte i2c@40005800 20 3**
      Output: 0x0

.. rubric:: Setup GPIO pins on first IO expander to output

* each odd GPIO to high(1)
* each even GPIO to low(0)

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **i2c read_byte i2c@40005800 20 1**
      Output: 0xff

      :bgn:`uart:~$` **i2c write_byte i2c@40005800 20 1 0x55**
      :bgn:`uart:~$` **i2c read_byte i2c@40005800 20 1**
      Output: 0x55

      :bgn:`uart:~$` **i2c read_byte i2c@40005800 20 0**
      Output: 0x55
