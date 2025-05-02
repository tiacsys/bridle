.. _snippet-del-default-aliases:

Delete Default Devicetree Aliases Snippet (del-default-aliases)
###############################################################

.. code-block:: console

   west build -S del-default-aliases [...]

Overview
********

This snippet deletes common default alias properties from the
:external+zephyr:ref:`devicetree`, e.g. such as :dts:`sw0 = &gpio_key_node;`,
or :dts:`led0 = &gpio_led_node;`, or :dts:`pwm-led0 = &pwm_led_node;`.
In general, these are only expected from simple examples or test cases but
can potentially cause ugly side effects if, for example, both an application
and a Zephyr subsystem simultaneously initialize interrupt callbacks on the
underlying hardware.

In such a constellation, for example in the case of
:external+zephyr:zephyr:code-sample:`lvgl` together with the
:dtcompatible:`zephyr,input-longpress` function in the input system on exactly
the same GPIO pin, every second event would not be handled there for by the
input system but at the application level and would therefore be lost for the
input system. The end user is free to use this snippet in such cases or to use
another adequate solution.

Current Deletions
*****************

.. literalinclude:: del-default-aliases.overlay
   :caption: del-default-aliases.overlay
   :language: DTS
   :encoding: ISO-8859-1
   :linenos:
   :prepend: / {
   :start-at: aliases {
   :end-at: };
   :append: };
