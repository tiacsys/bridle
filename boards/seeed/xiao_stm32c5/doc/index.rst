.. _xiao_stm32c5_board-extensions:

XIAO STM32C5 (BBE)
##################

Overview
********

This is a set of Bridle's board extensions (BBE) to the original Zephyr
upstream board |zephyr:board:xiao_stm32c5| with some adaptions and
improvement on Twister, Kconfig and Devicetree level.

:|okay|:

   .. admonition:: CONSTRAINTS
      :class: hint dropdown

      :USB CDC-ACM console:

         The Bridle Board Extension eliminates the restriction of having to
         use only the USB CDC-ACM console. This allows users to also use the
         UART available on the XIAO connector as a console (e.g., with a debug
         and probe adapter). To restore the USB CDC-ACM console, you can use
         Bridle's :ref:`snippet-usb-console`.

         .. rubric:: Zephyr USB CDC-ACM UART (by :code:`usb-console`)

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |xiao_stm32c5_VID|, idProduct=\ |xiao_stm32c5_PID_CON|, bcdDevice=\ |xiao_stm32c5_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |xiao_stm32c5_PStr_CON|
               Manufacturer: |xiao_stm32c5_VStr|
               SerialNumber: 482910563728491057392814

         |nbsp|

      :USB URB data as shipped:

         .. rubric:: MicroPython

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |xiao_stm32c5_VID_MP4|, idProduct=\ |xiao_stm32c5_PID_MP4|, bcdDevice=\ |xiao_stm32c5_BCD_MP4|
               USB device strings: Mfr=1, Product=2, SerialNumber=0
               Product: |xiao_stm32c5_PStr_MP4|
               Manufacturer: |xiao_stm32c5_VStr_MP4|

         .. rubric:: TinyUF2 Bootloader

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |xiao_stm32c5_VID_UF2|, idProduct=\ |xiao_stm32c5_PID_UF2|, bcdDevice=\ |xiao_stm32c5_BCD_UF2|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |xiao_stm32c5_PStr_UF2|
               Manufacturer: |xiao_stm32c5_VStr_UF2|
               SerialNumber: 482910563728491057392814

:|warn|:

   .. admonition:: EXPERIMENTAL SUPPORT
      :class: warning dropdown toggle-shown

      The `XIAO STM32C5 <XIAO STM32C5 wiki_>`_ is a brand-new development board
      in the `Seeed Studio XIAO`_ family. So far, the only support available is
      manufacturer-specific support provided by `MicroPython for Seeed board`_,
      which is based on Zephyr v4.4.0. Official support will not be available
      until release of Zephyr v4.5. Thus, some shortcomings currently exist
      when working with it:

      :Wrong user button polarity:

         The polarity of the user button is incorrectly (inverted) specified in
         the board Devicetree. A corresponding pull request is already open.

         See: https://github.com/zephyrproject-rtos/zephyr/pull/123468

         |nbsp|

      :Missing USB pinctrl and clock setup:

         The board Devicetree has no valid setup for pinctrl and clock setup
         for the USB device node. A corresponding pull request is already open.

         See: https://github.com/zephyrproject-rtos/zephyr/pull/123503

         |nbsp|

      :Missing UF2 support:

         The Kconfig symbol |CONFIG_BUILD_OUTPUT_UF2| can not yet be used
         because Zephyr's own UF2 conversion script |scripts/build/uf2conv.py|_
         does not yet support the required new UF2 family. The UF2 family ID
         newly introduced by Seeed Studio is :code:`0x00C5C5C5`, and the UF2
         volume label is :code:`XIAOC5BOOT` (see `XIAO STM32C5 MicroPython`_
         and `XIAO STM32C5 MicroPython Release Notes`_). The missing data
         still needs to be added to Zephyr's own UF2 database in
         |scripts/build/uf2families.json|_.

         As long this has not been done, the UF2 conversion can only be
         performed manually using:

         .. parsed-literal::
            :class: highlight-console notranslate

               ./zephyr/scripts/build/uf2conv.py -b :bbl:`0x08008000` -f :brd:`0x00C5C5C5` \\
                                                 -i :emphasis:`<build_folder>`\ /zephyr/zephyr\ :strong:`bin` \\
                                                 -o :emphasis:`<build_folder>`\ /zephyr/zephyr\ :strong:`uf2`

         … and then copy this UF2 file to the :strong:`XIAOC5BOOT` volume of
         the active `UF2 bootloader`_. If in doubt or if other errors occur, you
         can also try out the Seeed-specific UF2 conversion script from their
         MicroPython, |Seeed-Studio/micropython-seeed-boards/tools/uf2conv.py|_.

         |nbsp|

      :Flash over SWD required:

         Since the :program:`'west build …'` command does not include the UF2
         image conversion step at the end, only programming via the SWD
         interface over a suitable debug and probe adapter is supported. The
         current integration for Zephyr requires the use of the
         |zephyr:flash_debug:host-tools:runner:stm32cubeprogrammer|
         for this purpose. Bridle developers recommend the following hardware
         setup for working with the `XIAO STM32C5 <XIAO STM32C5 wiki_>`_,
         consisting of an additional `Expansion Base for XIAO`_ and one of the
         myriad affordable ST-LINK adapters (e.g., the
         |WeActStudio MiniDebugger/STLink|, as shown).

         .. figure:: img/xiao_stm32_stlink.webp
            :align: center
            :alt: XIAO STM32C5 on Expansion Base for XIAO with WeActStudio MiniDebugger

            XIAO STM32C5 on Expansion Base for XIAO with WeActStudio MiniDebugger

         |nbsp|

         Through the :emphasis:`Expansion Base for XIAO`, the :code:`3V3` power
         supply and :code:`GND`, as well as the SWD signals :code:`SWDIO` and
         :code:`SWCLK` and the UART signals :code:`TxD` and :code:`RxD`
         (cross-connected), are appropriately connected to and from the
         :emphasis:`XIAO STM32C5` to the :emphasis:`ST-LINK`. These
         :emphasis:`ST-LINK` variants should work:

         - `ST-LINK/V2`_
         - `ST-LINK-V3MINIE`_
         - `ST-LINK-V3MODS`_
         - `ST-LINK-V3SET`_
         - `ST-LINK-V3PWR`_
         - |WeActStudio MiniDebugger/STLink|_

List of extensions
******************

.. rubric:: Board YAML

- add the missing features that this board supports and
  that Twister tests might depends on:

  - :code:`flash`
  - :code:`hwinfo`
  - :code:`pwm`
  - :code:`usbd`
  - :code:`xiao_adc`
  - :code:`xiao_can`
  - :code:`xiao_gpio`
  - :code:`xiao_i2c`
  - :code:`xiao_serial`
  - :code:`xiao_spi`

.. rubric:: Kconfig

- :brd:`deactivate` self powered USB explicitly and set the maximum of
  electrical current consumption to :brd:`500㎃`:

  - |CONFIG_CDC_ACM_SERIAL_SELF_POWERED|
  - |CONFIG_CDC_ACM_SERIAL_MAX_POWER|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: XIAO STM32C5

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 1-2,5-6
            :start-at: config CDC_ACM_SERIAL_SELF_POWERED
            :end-before: Logger cannot use itself to log

- :brd:`change` log level only in case of use the native USB device port
  :dtcompatible:`st,stm32-usb` with CDC-ACM UART
  :dtcompatible:`zephyr,cdc-acm-uart` as Zephyr console:

  - |CONFIG_USBD_CDC_ACM_LOG_LEVEL_CHOICE| :=
    |CONFIG_USBD_CDC_ACM_LOG_LEVEL_OFF|
  - |CONFIG_USBD_LOG_LEVEL_CHOICE| :=
    |CONFIG_USBD_LOG_LEVEL_OFF|
  - |CONFIG_UDC_DRIVER_LOG_LEVEL_CHOICE| :=
    |CONFIG_UDC_DRIVER_LOG_LEVEL_ERR|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: XIAO STM32C5

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :lines: -14,23-
            :emphasize-lines: 3-4,16-17,22-23,28-29
            :start-at: Workaround for not being able to have commas in macro arguments
            :end-at: endif # zephyr,cdc-acm-uart

- :brd:`revert` and :brd:`deactivate` CDC-ACM UART console requirements
  via common fragment in upstream board:

  - |CONFIG_BOARD_REQUIRES_SERIAL_BACKEND_CDC_ACM|
  - |CONFIG_BOARD_SERIAL_BACKEND_CDC_ACM|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: XIAO STM32C5

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 2-3,6-7
            :start-after: Revert USB CDC-ACM console via common fragment in upstream board.
            :end-before: END of Revert USB CDC-ACM console (do not remove or change this line)

.. rubric:: Devicetree

- :brd:`revert` and :brd:`deactivate` CDC-ACM UART console setup
  via common fragment in upstream board:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: XIAO STM32C5

     * - .. literalinclude:: ../xiao_stm32c5_stm32c5a3xx_bbe.dts
            :caption: xiao_stm32c5_stm32c5a3xx_bbe.dts
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 2-3
            :start-after: Revert USB CDC-ACM console via common fragment in upstream board.
            :end-before: Fix missing pinctrl and clock setup for USB device (PR #123503).

- :brd:`change` and :brd:`fix` missing pinctrl and clock setup for USB device:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: XIAO STM32C5

     * - .. literalinclude:: ../xiao_stm32c5_stm32c5a3xx_bbe.dts
            :caption: xiao_stm32c5_stm32c5a3xx_bbe.dts
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 2-3,7-8
            :start-after: Fix missing pinctrl and clock setup for USB device (PR #123503).
            :end-before: Fix user button polarity on the BOOT0 pad (PR #123468).

     * - The Devicetree node for the USB device requires the correct mapping
         of the dedicated USB pins on the STM32C5. These are :code:`DM` on
         :code:`PA11` and :code:`DP` on :code:`PA12`. In order for the on-chip
         USB functional unit to work at all, a highly stable 48 MHz clock must
         also be enabled. Direct access via the HSE from an external 48 MHz
         crystal is the recommended method for this.

- :brd:`change` and :brd:`fix` user button polarity on the BOOT0 pad:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: XIAO STM32C5

     * - .. literalinclude:: ../xiao_stm32c5_stm32c5a3xx_bbe.dts
            :caption: xiao_stm32c5_stm32c5a3xx_bbe.dts
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 2
            :start-after: Fix user button polarity on the BOOT0 pad (PR #123468).
            :end-at: };

     * - The user button connected to the :code:`PH2/BOOT0` pin has an
         additional external connection to the test pad on the bottom of the PCB
         and sets :code:`PH2/BOOT0` to :code:`3V3`. This makes the user button
         :strong:`active-high`. The external :strong:`pull-down` resistor
         ensures the inactive state when the user button is not pressed.

         :code:`BOOT0` is still sampled by the MCU during a reset; :strong:`do
         not hold down the button` when powering on or resetting the board to
         :strong:`prevent the DFU ROM bootloader in the SoC from starting`.

- set default entries for ``model`` and ``compatible`` of the boards:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: XIAO STM32C5

     * - .. literalinclude:: ../xiao_stm32c5_stm32c5a3xx_bbe.dts
            :caption: xiao_stm32c5_stm32c5a3xx_bbe.dts
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-before: chosen {
            :append: };

References
**********

.. target-notes::

.. |scripts/build/uf2conv.py| replace:: :code:`scripts/build/uf2conv.py`
.. _`scripts/build/uf2conv.py`:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/build/uf2conv.py

.. |scripts/build/uf2families.json| replace:: :code:`scripts/build/uf2families.json`
.. _`scripts/build/uf2families.json`:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/build/uf2families.json

.. |Seeed-Studio/micropython-seeed-boards/tools/uf2conv.py| replace::
   :code:`Seeed-Studio/micropython-seeed-boards/tools/uf2conv.py`
.. _`Seeed-Studio/micropython-seeed-boards/tools/uf2conv.py`:
   https://github.com/Seeed-Studio/micropython-seeed-boards/blob/master/tools/uf2conv.py
