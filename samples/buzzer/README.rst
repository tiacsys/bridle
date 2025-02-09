.. _buzzer-sample:

Buzzer
######

Drive a buzzer or speaker using the PWM API.

Overview
********

This is a sample app which drives a buzzer or speaker using the
:zephyr:ref:`PWM API <pwm_api>`.

The sample plays a short beep with 1108.73 ㎐ (music note `D♭₆`_) for the
time of a ⅛ `music note`_ at boot time and offers the special shell command
:program:`buzzer` for playing other jingles or short songs.

Requirements
************

The sample requires a buzzer or speaker whose signal pin is connected to a pin
driven by PWM. The buzzer or speaker must be defined in Devicetree using the
:dts:`pwm-buzzers` compatible (part of Bridle) and setting its node to the
alias :dts:`pwm-buzzer0`. You will need to do something like this:

   .. code-block:: devicetree

      / {
          aliases {
              pwm-buzzer0 = &pwm_buzzer0;
          };

          pwm_buzzers {
              compatible = "pwm-buzzers";
              status = "okay";

              pwm_buzzer0: pwm_buzzer0 {
                  pwms = <&pwm0 1 PWM_HZ(880) PWM_POLARITY_NORMAL>;
                  label = "PWM_BUZZER";
              };
          };
      };

Note that a commonly used period value is 880 ㎐, twice the concert pitch
frequency of 440 ㎐. See one of the following development boards:

  * |bridle:board:cytron_maker_rp2040|
  * |bridle:board:picoboy|

Building and Running
********************

* On |Maker Nano RP2040| board:

  .. zephyr-app-commands::
     :app: bridle/samples/buzzer
     :build-dir: buzzer-cytron_maker_nano_rp2040
     :board: cytron_maker_nano_rp2040
     :west-args: -p -S usb-console
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

* On |Maker Pi RP2040| board:

  .. zephyr-app-commands::
     :app: bridle/samples/buzzer
     :build-dir: buzzer-cytron_maker_pi_rp2040
     :board: cytron_maker_pi_rp2040
     :west-args: -p -S usb-console
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

* On |PicoBoy| board:

  .. zephyr-app-commands::
     :app: bridle/samples/buzzer
     :build-dir: buzzer-picoboy
     :board: picoboy
     :west-args: -p
     :flash-args: -r uf2
     :goals: flash
     :host-os: unix

Sample Output
=============

(text in bold is a command input, text in angle brackets are keys to press)

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      [00:00:00.003,000] <inf> buzzersh: Buzzer shell is ready!


      :bgn:`uart:~$` **<Tab>**
        :bcy:`bridle   buzzer   clear    device   devmem   gpio     help     history`
        :bcy:`kernel   log      pwm      rem      resize   retval   shell`

      :bgn:`uart:~$` **help**
      Please press the <Tab> button to see all available commands.
      You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
      You can try to call commands with <-h> or <--help> parameter for more information.

      Shell supports following meta-keys:
        Ctrl + (a key from: abcdefklnpuw)
        Alt  + (a key from: bf)
      Please refer to shell documentation for more details.

      Available commands:
        bridle   : Bridle commands.
        buzzer   : Buzzer related commands
        clear    : Clear screen.
        device   : Device commands
        devmem   : Read/write physical memory
                   Usage:
                   Read memory at address with optional width:
                   devmem address [width]
                   Write memory at address with mandatory width and value:
                   devmem address <width> <value>
        gpio     : GPIO commands
        help     : Prints the help message.
        history  : Command history.
        kernel   : Kernel commands
        log      : Commands for controlling logger
        pwm      : PWM shell commands
        rem      : Ignore lines beginning with 'rem '
        resize   : Console gets terminal screen size or assumes default in case the
                   readout fails. It must be executed after each terminal width change
                   to ensure correct text display.
        retval   : Print return value of most recent command
        shell    : Useful, not Unix-like shell commands.

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer -h**
      buzzer - Buzzer related commands
      Subcommands:
        info  :Get buzzer info
        beep  :Use buzzer to beep
        play  :Play one of predefined sounds

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer info**
      Warning: not yet implemented.

      :bgn:`uart:~$` **buzzer beep**

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer play**
      play - Play one of predefined sounds
      Subcommands:
        folksong   : Play the 'folksong' song
        xmastime   : Play the 'folksong' song
        funkytown  : Play the 'funkytown' song
        mario      : Play the 'mario' song
        golioth    : Play the 'golioth' song
        tiacsys    : Play the 'tiacsys' song

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer play folksong**

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer play xmastime**

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer play funkytown**

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer play mario**

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer play golioth**

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **buzzer play tiacsys**

References
**********

.. target-notes::

.. _D♭₆: https://en.wikipedia.org/wiki/D%E2%99%AD_(musical_note)
.. _music note: https://en.wikipedia.org/wiki/Musical_note
