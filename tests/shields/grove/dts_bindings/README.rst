Grove Interconnect Shields DTS Binding
######################################

This integration test verifies the DTS binding of the :ref:`grove_base_shield`
against all possible :term:`boards <board>` and shields that are supported by
:ref:`Zephyr <zephyr:boards>` and :ref:`Bridle <boards>`.

Depending on the number of compatible boards, this test suite will take several
minutes to complete::

    west twister \
         --jobs 4 \
         --verbose \
         --inline-logs \
         --testsuite-root bridle/tests/shields/grove/dts_bindings

With the option ``--cmake-only`` the test time can be reduced significantly,
but then the runtime filter will not act as expected and the filtering rules
become ineffective::

    west twister \
         --jobs 4 \
         --verbose \
         --cmake-only \
         --inline-logs \
         --testsuite-root bridle/tests/shields/grove/dts_bindings

Even more time can be saved by limiting the test runs to the boards currently
supported by this shield and that will be used for maintenance::

    west twister \
         --jobs 4 \
         --verbose \
         --inline-logs \
         --platform rpi_pico \
         --platform nucleo_f303re \
         --platform nucleo_f401re \
         --platform nucleo_f413zh \
         --platform nucleo_f767zi \
         --platform mimxrt1010_evk \
         --platform mimxrt1060_evk \
         --platform mimxrt1060_evkb \
         --board-root bridle/boards \
         --platform seeeduino_lotus \
         --testsuite-root bridle/tests/shields/grove/dts_bindings
