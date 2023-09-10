.. _doc_styleguide:

Documentation style guide
#########################

|BRIDLE| documentation is written in two formats:

* doxygen for API documentation
* RST for conceptual documentation

RST style guide
***************

See Zephyr's :ref:`zephyr:doc_guidelines` for a short introduction to RST and,
most importantly, to the conventions used in Zephyr. More information about
RST is available in the `reStructuredText Primer`_ as part of the original
`Sphinx Documentation`_, and about the Sphinx documentation framework in the
`Li-Pro.Net Sphinx Primer`_.

The |BRIDLE| documentation follows the Zephyr style guide, and adds a few more
restrictive rules:

* Headings use sentence case, which means that the first word is capitalized,
  and the following words use normal capitalization.
* Do not use consecutive headings without intervening text.
* For readability reasons, start every sentence on a new line in the source
  files and do not add line breaks within the sentence. In the output,
  consecutive lines without blank lines in between are combined into one
  paragraph.

  .. note::

     For the conceptual documentation written in RST, you can have more than
     80 characters per line. The requirement for 80 characters per line applies
     only to the code documentation written in doxygen.

Hyperlinks
==========

All external links must be defined in the ``links.txt`` file. Do not define
them directly in the RST file. The reason for this is to allow for validating
all links in one central location and to make it easy to update breaking links.

Each link should be defined only once in ``links.txt``.

If the link text that is defined in ``links.txt`` does not fit in the context
where you use the link, you can override it by using the following syntax::

   `new link text <original link text_>`_

It is also possible to define more than one default link text for a link, which
can be useful if you frequently need a different link text::

   .. _`Link text one`:
   .. _`Link text two`: http://..

Diagrams
========

You can include Message Sequence Chart (MSC) diagrams in RST by using the
... t.b.d.

You can include Message Sequence Chart (MSC) diagrams in RST by using the
``.. msc::`` directive and including the MSC content, for example:

.. code-block:: python

   .. msc::
      hscale = "1.3";
      Module,Application;
      Module<<Application      [label="nemo_connect() returns successfully"];
      Module>>Application      [label="NEMO_LAB_TRANSPORT_CONNECTED"];
      Module>>Application      [label="NEMO_LAB_USER_ASSOCIATION_REQUEST"];
      Module<<Application      [label="nemo_user_associate()"];
      Module>>Application      [label="NEMO_LAB_USER_ASSOCIATED"];
      Module>>Application      [label="NEMO_LAB_READY"];
      Module>>Application      [label="NEMO_LAB_TRANSPORT_DISCONNECTED"];

This will generate the following output:

.. msc::
   hscale = "1.3";
   Module,Application;
   Module<<Application      [label="nemo_connect() returns successfully"];
   Module>>Application      [label="NEMO_LAB_TRANSPORT_CONNECTED"];
   Module>>Application      [label="NEMO_LAB_USER_ASSOCIATION_REQUEST"];
   Module<<Application      [label="nemo_user_associate()"];
   Module>>Application      [label="NEMO_LAB_USER_ASSOCIATED"];
   Module>>Application      [label="NEMO_LAB_READY"];
   Module>>Application      [label="NEMO_LAB_TRANSPORT_DISCONNECTED"];

Kconfig
=======

Kconfig options can be linked to from RST by using the ``:option:`` domain::

   :option:`CONFIG_DEBUG`

Breathe
=======

The Breathe Sphinx plugin provides a bridge between RST and doxygen.

The doxygen documentation is not automatically included in RST. Therefore,
every group must be explicitly added to an RST file.

.. code-block:: python
   :caption: Example of how to include a doxygen group

   .. doxygengroup:: nemo_lab_transport
      :project: bridle
      :members:

.. note::

   Including a group on a page does not include all its subgroups
   automatically. To include subgroups, list them on the page of the group
   they belong to.

The `Breathe documentation`_ contains information about what you can link to.

To link directly to a doxygen reference from RST, use the following
Breathe domains:

* Function: ``:cpp:func:``
* Structure: ``:c:type:``
* Enum (i.e. the list): ``:cpp:enum:``
* Enumerator (i.e. an item): ``:cpp:enumerator:``
* Macro: ``:c:macro:``
* Structure member: ``:cpp:member:``

.. note::

   The ``:cpp:enum:`` and ``:cpp:enumerator:`` domains do not generate a link
   due to `Breathe issue #437`_. As a workaround, use the following command::

      :cpp:enumerator:`ENUM_VALUE <DOXYGEN_GROUP::ENUM_VALUE>`

Special Roles
=============

|BRIDLE| provides its own predefined roles for specific formatting, which
are then later interpreted and rendered accordingly by the style sheets of
the various output formats. The available roles are specified in the
:bridle_file:`doc/bridle/roles.txt` file. The classes declared therein
must then be defined accordingly for HTML in the CSS files below
:bridle_file:`doc/_static/css`.

The following table shows just a few examples.

.. list-table::
   :header-rows: 1

   * - reStructuredText
     - rendered result
     - description

   * - :rst:`:rd:\`normal red\``
     - :rd:`normal red`
     - inline colorization in normal weight

   * - :rst:`:i:\`italic\``
     - :i:`italic`
     - inline italic style

   * - :rst:`:ign:\`italic green\``
     - :ign:`italic green`
     - inline colorization in italic style

   * - :rst:`:b:\`bold\``
     - :b:`bold`
     - inline bold weight

   * - :rst:`:bbl:\`bold blue\``
     - :bbl:`bold blue`
     - inline colorization in bold weight

   * - :rst:`:s:\`strikethrough\``
     - :s:`strikethrough`
     - inline strikethrough decoration

   * - :rst:`:syl:\`strikethrough yellow\``
     - :syl:`strikethrough yellow`
     - inline colorization in strikethrough decoration

   * - :rst:`:u:\`underline\``
     - :u:`underline`
     - inline underline decoration

   * - :rst:`:uwt:\`underline white\``
     - .. rst-class:: lightgray-box

          :uwt:`underline white`

     - inline colorization in underline decoration

   * - :rst:`:rst:\`:program:\\\`honkomat\\\`\``
     - :rst:`:program:\`honkomat\``
     - inline syntax highlighting for reStructuredText

   * - :rst:`:python:\`from pathlib import Path\``
     - :python:`from pathlib import Path`
     - inline syntax highlighting for Python

   * - :rst:`:c:\`int sum(int a, int b);\``
     - :c:`int sum(int a, int b);`
     - inline syntax highlighting for C/C++

   * - | :rst:`:hwftlbl:\`4㎆\``
       | :rst:`:hwftlbl:\`OTA\``

     - :hwftlbl:`4㎆`
       :hwftlbl:`OTA`

     - hardware feature label for a common purpose

   * - | :rst:`:hwftlbl-btn:\`RST\``
       | :rst:`:hwftlbl-btn:\`USR\``

     - :hwftlbl-btn:`RST`
       :hwftlbl-btn:`USR`

     - hardware feature label for a :u:`button and switch` purpose

   * - | :rst:`:hwftlbl-led:\`ERR\``
       | :rst:`:hwftlbl-led:\`USR\``

     - :hwftlbl-led:`ERR`
       :hwftlbl-led:`USR`

     - hardware feature label for a :u:`lamp and signal` purpose

   * - | :rst:`:hwftlbl-scr:\`OLED\``
       | :rst:`:hwftlbl-scr:\`HDMI\``

     - :hwftlbl-scr:`OLED`
       :hwftlbl-scr:`HDMI`

     - hardware feature label for a :u:`screen and display` purpose

   * - | :rst:`:hwftlbl-con:\`USB-C\``
       | :rst:`:hwftlbl-btn:\`10Base-T\``

     - :hwftlbl-con:`USB-C`
       :hwftlbl-con:`10Base-T`

     - hardware feature label for a :u:`connector` purpose

   * - | :rst:`:hwftlbl-sys:\`3.3V(PS)\``
       | :rst:`:hwftlbl-sys:\`3.3V(EN)\``

     - :hwftlbl-sys:`3.3V(PS)`
       :hwftlbl-sys:`3.3V(EN)`

     - hardware feature label for a :u:`system and control` purpose

   * - | :rst:`:hwftlbl-vdd:\`5V/300㎃\``
       | :rst:`:hwftlbl-vdd:\`3.3V/500㎃\``
       | :rst:`:hwftlbl-vdd:\`3.3V(OUT)\``

     - :hwftlbl-vdd:`5V/300㎃`

       :hwftlbl-vdd:`3.3V/500㎃`
       :hwftlbl-vdd:`3.3V(OUT)`

     - hardware feature label for a :u:`power and voltage distribution` purpose

   * - | :rst:`:hwftlbl-dbg:\`UF2\``
       | :rst:`:hwftlbl-dbg:\`SWD\``
       | :rst:`:hwftlbl-dbg:\`JTAG\``

     - :hwftlbl-dbg:`UF2`
       :hwftlbl-dbg:`SWD`
       :hwftlbl-dbg:`JTAG`

     - hardware feature label for a :u:`debug and development` purpose

   * - | :rst:`:hwftlbl-pio:\`20\``
       | :rst:`:hwftlbl-pwm:\`16\``
       | :rst:`:hwftlbl-pcm:\`1\``
       | :rst:`:hwftlbl-dac:\`2\``
       | :rst:`:hwftlbl-adc:\`4\``
       | :rst:`:hwftlbl-i2s:\`1\``
       | :rst:`:hwftlbl-i2c:\`1\``
       | :rst:`:hwftlbl-spi:\`2\``
       | :rst:`:hwftlbl-hsi:\`2\``
       | :rst:`:hwftlbl-can:\`2\``
       | :rst:`:hwftlbl-uart:\`2\``
       | :rst:`:hwftlbl-usart:\`2\``
       | :rst:`:hwftlbl-mmc:\`1\``
       | :rst:`:hwftlbl-sdc:\`1\``
       | :rst:`:hwftlbl-tfc:\`1\``
       | :rst:`:hwftlbl-csi:\`1\``
       | :rst:`:hwftlbl-dsi:\`1\``
       | :rst:`:hwftlbl-dpp:\`1\``
       | :rst:`:hwftlbl-tsi:\`1\``

     - :hwftlbl-pio:`20`
       :hwftlbl-pwm:`16`
       :hwftlbl-pcm:`1`

       :hwftlbl-dac:`2`
       :hwftlbl-adc:`4`

       :hwftlbl-i2s:`1`
       :hwftlbl-i2c:`1`
       :hwftlbl-spi:`2`
       :hwftlbl-hsi:`2`

       :hwftlbl-can:`2`
       :hwftlbl-uart:`2`
       :hwftlbl-usart:`2`

       :hwftlbl-mmc:`1`
       :hwftlbl-sdc:`1`
       :hwftlbl-tfc:`1`

       :hwftlbl-csi:`1`
       :hwftlbl-dsi:`1`
       :hwftlbl-dpp:`1`
       :hwftlbl-tsi:`1`

     - hardware feature label for a :u:`function and interface` purpose

       - Total number of PIO (Parallel In-/Output)
       - Total number of PWM (Pulse-Width Modulation)
       - Total number of PCM (Pulse-Code Modulation)
       - Total number of DAC (Digital-to-Analog Converter)
       - Total number of ADC (Analog-to-Digital Converter)
       - Total number of I2S (Inter-IC Sound)
       - Total number of I2C (Inter-Integrated Circuit)
       - Total number of SPI (Serial Peripheral Interface)
       - Total number of HSI (High-Speed Synchronous Serial Interface)
       - Total number of CAN (Controller Area Network)
       - Total number of UART (Universal Asynchronous Receiver-Transmitter)
       - Total number of USART (Universal Synchronous and Asynchronous Receiver-Transmitter)
       - Total number of MMC/SD/TF (Multi-Media-/Secure-Digital-Card or TransFlash)
       - Total number of CSI (Camera Sensor Interface, e.g. MIPI)
       - Total number of DSI (Display Serial Interface, e.g. MIPI)
       - Total number of DPP (Display Parallel Port, e.g. RGB444/HS/VS/CLK)
       - Total number of TS (Touch-Screen Interface)

   * - | :rst:`:rpi-pico-gnd:\`GND\``
       | :rst:`:rpi-pico-vdd:\`VSYS\``

     - :rpi-pico-gnd:`GND`

       :rpi-pico-vdd:`VSYS`

     - Raspberry Pi Pico :u:`signal line label` special purpose

       - Total number of GND (Ground potential)
       - Total number of VSYS (Voltage level of System)

   * - | :rst:`:rpi-pico-sys:\`RUN\``
       | :rst:`:rpi-pico-swd:\`SWCLK\``

     - :rpi-pico-sys:`RUN`

       :rpi-pico-swd:`SWCLK`

     - Raspberry Pi Pico :u:`signal line label` special purpose

       - Total number of RUN (Reset)
       - Total number of SWCLK (Serial Wire Clock)

   * - | :rst:`:rpi-pico-pio:\`GPIO28\``
       | :rst:`:rpi-pico-pwm:\`PWM12\``
       | :rst:`:rpi-pico-adc:\`ADC_CH2\``

     - :rpi-pico-pio:`GPIO28`

       :rpi-pico-pwm:`PWM12`

       :rpi-pico-adc:`ADC_CH2`

     - Raspberry Pi Pico :u:`signal line label` special purpose

       - Total number of GPIO28 (General Purpose I/O line ``28``)
       - Total number of PWM12 (PWM output line ``12``)
       - Total number of ADC_CH2 (ADC input channel ``2``)

   * - | :rst:`:rpi-pico-spi-dfl:\`SPI0_SCK\``
       | :rst:`:rpi-pico-spi:\`SPI1_CSN\``

     - :rpi-pico-spi-dfl:`SPI0_SCK`

       :rpi-pico-spi:`SPI1_CSN`

     - Raspberry Pi Pico :u:`signal line label` special purpose

       - Total number of SPI0_SCK (Serial Clock line on default SPI ``0``)
       - Total number of SPI1_CSN (Chip Select Negative line on SPI ``1``)

   * - | :rst:`:rpi-pico-i2c-dfl:\`I2C0_SDA\``
       | :rst:`:rpi-pico-i2c:\`I2C1_SCL\``

     - :rpi-pico-i2c-dfl:`I2C0_SDA`

       :rpi-pico-i2c:`I2C1_SCL`

     - Raspberry Pi Pico :u:`signal line label` special purpose

       - Total number of I2C0_SDA (Serial Data line on default I2C ``0``)
       - Total number of I2C1_SCL (Serial Clock line on I2C ``1``)

   * - | :rst:`:rpi-pico-uart-dfl:\`UART0_TX\``
       | :rst:`:rpi-pico-uart:\`UART1_RX\``

     - :rpi-pico-uart-dfl:`UART0_TX`

       :rpi-pico-uart:`UART1_RX`

     - Raspberry Pi Pico :u:`signal line label` special purpose

       - Total number of UART0_TX (Data Transmit line on default UART ``0``)
       - Total number of UART1_RX (Data Receive line on UART ``1``)

Special Replacements
====================

Special technical or domain specific UNICODE characters can be used by
replacements without having to know their exact numeric code when entering
text. For this purpose, the individually maintained list exists in the file
:bridle_file:`doc/bridle/unicode.txt`.

The following table shows just a few examples.

.. list-table::
   :header-rows: 1

   * - reStructuredText
     - rendered result
     - unicode
     - description

   * - :rst:`Lorem |nbsp| |nbsp| |nbsp| ipsum`
     - Lorem |nbsp| |nbsp| |nbsp| ipsum
     - U+000A0
     - nob-space / non-breaking space

   * - :rst:`|curs|`
     - |curs|
     - U+000A4
     - currency sign (the old German "pig")

   * - :rst:`|copy|`
     - |copy|
     - U+000A9
     - copyright sign

   * - :rst:`|regs|`
     - |regs|
     - U+000AE
     - registered sign

   * - :rst:`|!!| / |!?|`
     - |!!| / |!?|
     - U+0203C, U+02049
     - double exclamation  and exclamation questionmark

   * - :rst:`|?| / |!|`
     - |?| / |!|
     - U+02753, U+02757
     - red question and exclamation mark

   * - :rst:`|candle| |star| |open book|`
     - |candle| |star| |open book|
     - U+1F56F, U+02B50, U+1F4D6
     - Emojis: candle, star, open book

   * - :rst:`|secret| |free of charge| |open for business| |passing grade|`
     - |secret| |free of charge| |open for business| |passing grade|
     - U+03299, U+1F21A, U+1F23A, U+1F234
     - CJK signes: secret, free of charge, open for business, passing grade

   * - :rst:`|oneq|`
     - |oneq|
     - U+000BC
     - vulgar fraction one quarter

   * - :rst:`|oneq|`
     - |oneq|
     - U+000BC
     - vulgar fraction one quarter

   * - :rst:`|oneh|`
     - |oneh|
     - U+000BD
     - vulgar fraction one half

   * - :rst:`|threeq|`
     - |threeq|
     - U+000BE
     - vulgar fraction three quarters

   * - :rst:`|sup2| |sup3| |/| |sub3| |sub2|`
     - |sup2| |sup3| |/| |sub3| |sub2|
     - U+0338F
     - special fraction

   * - :rst:`X |sup7| |sup(| |sup8| |sup-| |sup9| |sup)|`
     - X |sup7| |sup(| |sup8| |sup-| |sup9| |sup)|
     - U+02070 |...| U+0207E
     - superscript formatter

   * - :rst:`X |sub7| |sub(| |sub8| |sub-| |sub9| |sub)|`
     - X |sub7| |sub(| |sub8| |sub-| |sub9| |sub)|
     - U+02080 |...| U+0208E
     - subscript formatter

   * - :rst:`N = J/m = |kg| |*| m |*| s |sup-| |sup2|`
     - N = J/m = |kg| |*| m |*| s |sup-| |sup2|
     - U+02044, U+0207B, U+000B2
     - Newton in Joule per meter and in SI units

   * - :rst:`8 |nm| = 8 |*| 10 |sup-| |sup3| |um|`
     - 8 |nm| = 8 |*| 10 |sup-| |sup3| |um|
     - U+0339A, U+0339B
     - nano, micro meter

   * - :rst:`|nm|/|um|/|mm|/|cm|/|dm|/|km|`
     - |nm|/|um|/|mm|/|cm|/|dm|/|km|
     - U+0339A |...| U+0339E
     - nano, micro, milli, centi, deci, kilo meter

   * - :rst:`|mm2|/|cm2|/|dm2|/|km2|`
     - |mm2|/|cm2|/|dm2|/|km2|
     - U+0339F |...| U+033A2
     - square milli, centi, deci, kilo meter squared

   * - :rst:`|mm3|/|cm3|/|dm3|/|km3|`
     - |mm3|/|cm3|/|dm3|/|km3|
     - U+033A3 |...| U+033A6
     - square milli, centi, deci, kilo meter cubed

   * - :rst:`|ul|/|ml|/|dl|`
     - |ul|/|ml|/|dl|
     - U+03395 |...| U+03397
     - micro, milli, deci litre

   * - :rst:`|ug|/|mg|/|kg|`
     - |ug|/|mg|/|kg|
     - U+0338D |...| U+0338F
     - micro, milli, kilo gramm

   * - :rst:`|ps|/|ns|/|us|/|ms|`
     - |ps|/|ns|/|us|/|ms|
     - U+033B0 |...| U+033B3
     - pico, nano, micro, milli, second

   * - :rst:`|Hz|/|kHz|/|MHz|/|GHz|/|THz|`
     - |Hz|/|kHz|/|MHz|/|GHz|/|THz|
     - U+03390 |...| U+03394
     - kilo, mega, giga, tera, hertz

   * - :rst:`|pA|/|nA|/|uA|/|mA|/A/|kA|`
     - |pA|/|nA|/|uA|/|mA|/A/|kA|
     - U+03380 |...| U+03384
     - pico, nano, micro, milli, kilo ampere

   * - :rst:`|pV|/|nV|/|uV|/|mV|/V/|kV|/|MV|`
     - |pV|/|nV|/|uV|/|mV|/V/|kV|/|MV|
     - U+033B4 |...| U+033B9
     - pico, nano, micro, milli, kilo, mega volt

   * - :rst:`|pW|/|nW|/|uW|/|mW|/W/|kW|/|MW|`
     - |pW|/|nW|/|uW|/|mW|/W/|kW|/|MW|
     - U+033BA |...| U+033BF
     - pico, nano, micro, milli, kilo, mega watt

   * - :rst:`|mO|/|O|/|kO|/|MO|`
     - |mO|/|O|/|kO|/|MO|
     - U+003A9, U+033C0, U+033C1
     - milli, kilo, mega ohm

   * - :rst:`|mO|/|O|/|kO|/|MO|`
     - |mO|/|O|/|kO|/|MO|
     - U+003A9, U+033C0, U+033C1
     - milli, kilo, mega ohm

   * - :rst:`|pF|/|nF|/|uF|`
     - |pF|/|nF|/|uF|
     - U+0338A, U+0338B, U+0338C
     - pico, nano, micro farad

   * - :rst:`|uH|/|mH|`
     - |uH|/|mH|
     - U+000B5, simulated
     - micro, milli henry

   * - :rst:`L = 500 |uH| = 0.5 |mH|`
     - L = 500 |uH| = 0.5 |mH|
     - U+000B5, simulated
     - micro, milli henry in equation

   * - :rst:`|Theta| = 20000 |x| 20 |uA| = 400 |mA|`
     - |Theta| = 20000 |x| 20 |uA| = 400 |mA|
     - U+00398, U+000D7, U+03382, U+03383
     - Greek capital letter theta symbol and micro / milli ampere

   * - :rst:`|theta| = 20 |°C| = 293.15 |K|`
     - |theta| = 20 |°C| = 293.15 |K|
     - U+003D1, U+02103, U+0212A
     - Greek theta symbol and degree Celsius and Kelvin sign

   * - :rst:`|kb|/|kB|/|MB|/|GB|`
     - |kb|/|kB|/|MB|/|GB|
     - U+03385, U+03386, U+03387
     - kilo bit / kilo, mega, giga byte

Doxygen style guide
*******************

This style guide covers guidelines for the doxygen-based API documentation.

General documentation guidelines
================================

#. Always use full sentences, except for descriptions for variables, structs,
   and enums, where sentence fragments with no verb are accepted, and always
   end everything with period.
#. Everything that is documented must belong to a group (see below).
#. Use capitalization sparingly. When in doubt, use lowercase.
#. Line breaks: In doxygen, break after 80 characters (following the dev
   guidelines). In RST, break after each sentence.
#. **@note** and **@warning** should only be used in the details section, and
   only when really needed for emphasis. Use notes for emphasis and warnings
   if things will really really go wrong if you ignore the warning.

File headers and groups
=======================

#. **@file** element is always required at the start of a file.
#. There is no need to use **@brief** for **@file**.
#. **@defgroup** or **@addgroup** usually follows **@file**.
   You can divide a file into several groups as well.
#. **@{** must open the group, **@}** must close it.
#. **@brief** must be added for every defgroup.
#. **@details** is optional to be used within the defgroup.

.. code-block:: c
   :caption: File header and group documentation example

   /** @file
    *  @defgroup nm_lab_pool Nemo LAB attribute pool API
    *  @{
    *  @brief Nemo LAB attribute pools.
    */

   #ifdef __cplusplus
   extern "C" {
   #endif

   #include <nemo/lab.h>
   #include <nemo/uuid.h>

   /** @brief Register a primary service descriptor.
    *
    *  @param _svc LAB service descriptor.
    *  @param _svc_uuid_init Service UUID.
    */
   #define NM_LAB_POOL_SVC_GET(_svc, _svc_uuid_init) \
   {                                                 \
     struct bt_uuid *_svc_uuid = _svc_uuid_init;     \
     nm_lab_pool_svc_get(_svc, _svc_uuid);           \
   }

   [...]
   /** @brief Return a PI descriptor to the pool.
    *
    *  @param attr Attribute describing the PI descriptor to be returned.
    */
   void nm_lab_pool_pi_put(struct nm_lab_attr const *attr);

   #if CONFIG_NM_LAB_POOL_STATS != 0
   /** @brief Print basic module statistics (containing pool size usage). */
   void nm_lab_pool_stats_print(void);
   #endif

   #ifdef __cplusplus
   }
   #endif

   /**
    * @}
    */

Functions
=========

#. Do not use **@fn**. Instead, document each function where it is defined.
#. **@brief** is mandatory.

   * Start the brief with the "do sth" form.

  .. code-block:: none
     :caption: Brief documentation examples

     /** @brief Request a read operation to be executed from Secure Firmware.

     /** @brief Send Boot Keyboard Input Report.

#. **@details** is optional. It can be introduced either by using
   **@details** or by leaving a blank line after **@brief**.
#. **@param** should be used for every parameter.

   * Always add parameter description. Use a sentence fragment (no verb) with
     period at the end.
   * Make sure the parameter documentation within the function is consistently
     using the parameter type: ``[in]``, ``[out]``, or ``[in,out]``.

  .. code-block:: none
     :caption: Parameter documentation example

     * @param[out] destination Pointer to destination array where the
     *                         content is to be copied.
     * @param[in]  addr        Address to be copied from.
     * @param[in]  len         Number of bytes to copy.

#. If you include more than one **@sa** ("see also", optional), add
   them this way.

   .. code-block:: none
      :caption: See also reference example

      * @sa first_function
      * @sa second_function

#. **@return** should be used to describe a generic return value without
   a specific value (for example, "@return The length of ...",
   "@return The handle"). There is usually only one return value.

   .. code-block:: none
      :caption: Return documentation example

      * @return  Initializer that sets up the pipe, length, and byte array for
      *          content of the TX data.

#. **@retval** should be used for specific return values (for example,
   "@retval true", "@retval CONN_ERROR"). Describe the condition for each of
   the return values (for example, "If the function completes successfully",
   "If the connection cannot be established").

   .. code-block:: none
      :caption: Retval documentation example

      * @retval 0 If the operation was successful.
      *           Otherwise, a (negative) error code is returned.
      * @retval (-ENOTSUP) Special error code used when the UUID
      *           of the service does not match the expected UUID.

#. Do not use **@returns**. Use **@return** instead.

.. code-block:: c
   :caption: Complete function documentation example

   /** @brief Request a random number from the Secure Firmware.
    *
    *  This function provides a True Random Number from the on-board random
    *  number generator.
    *
    *  @note Currently, the RNG hardware is run each time this function is
    *        called. This consumes significant time and power.
    *
    *  @param[out] output  The random number. Must be at least @p len long.
    *  @param[in]  len     The length of the output array. Currently, @p len
    *                      must be 144.
    *  @param[out] olen    The length of the random number provided.
    *
    *  @retval 0        If the operation was successful.
    *  @retval -EINVAL  If @p len is invalid. Currently, @p len must be 144.
    */
   int nm_request_random_number(u8_t *output, size_t len, size_t *olen);

Enums
=====

The documentation block should precede the documented element. This is in
accordance with the `Zephyr coding style`_.

.. code-block:: c
   :caption: Enum documentation example

   /** Nemo LAB service events. */
   enum nm_lab_svc_evt {

     /** Boot mode entered. */
     NM_LAB_SVC_EVT_BOOT_MODE_ENTERED,

     /** Report mode entered. */
     NM_LAB_SVC_EVT_REPORT_MODE_ENTERED,
   };

Structs
=======

The documentation block should precede the documented element. This is in
accordance with the `Zephyr coding style`_. Make sure to add ``:members:``
when you include the API documentation in RST; otherwise, the member
documentation will not show up.

.. code-block:: c
   :caption: Struct documentation example

   /** @brief Event header structure.
    *
    *  @warning When event structure is defined event header must be placed
    *           as the first field.
    */
   struct event_header {

     /** Linked list node used to chain events. */
     sys_dlist_t node;

     /** Pointer to the event type object. */
     const struct event_type *type_id;
   };


.. note::

   Always add a name for the struct. Avoid using unnamed structs
   due to `Sphinx parser issue`_.

References
==========

To link to functions, enums, or structs from within doxygen itself, use the
``@ref`` keyword.

.. code-block:: c
   :caption: Reference documentation example

   /** @brief Event header structure.
    *  Use this structure with the function @ref function_name and
    *  this structure is related to another structure, @ref structure_name.
    */

.. note::

   Linking to functions does not currently work due to `Breathe issue #438`_.

Typedefs
========

The documentation block should precede the documented element. This is in
accordance with the `Zephyr coding style`_.

.. code-block:: c
   :caption: Typedef documentation example

   /** @brief Download client asynchronous event handler.
    *
    *  Through this callback, the application receives events, such as
    *  download of a fragment, download completion, or errors.
    *
    *  If the callback returns a non-zero value, the download stops.
    *  To resume the download, use @ref download_client_start().
    *
    *  @param[in] event  The event.
    *
    *  @retval 0 The download continues.
    *  @retval non-zero The download stops.
    */
   typedef int (*download_client_callback_t)
               (const struct download_client_evt *event);
