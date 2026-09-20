Writing a shield template
===========================

.. admonition:: Prerequisites

   - :doc:`give-a-board-a-socket` — this tutorial plugs into the socket
     that one declared.

Rae has a Grove LED module: a single LED on the connector's first signal
pin. In Zephyr today that is an overlay naming a board pin, and a second
copy on a second connector needs a second overlay. Bridle ships sixty-four
of them for one Grove button.

**One new concept: a shield template describes a module in positions, not
pins** — so one file covers every socket the module could ever be plugged
into.

Write it
----------

Shields live in ``boards/shields/<name>/``, the same layout Zephyr already
uses. The one substitution is the file extension: where a Zephyr shield has
``<name>.overlay``, a template has ``<name>.shield``.

.. code-block:: console

   $ mkdir -p acme-rigs/boards/shields/acme_grove_led

.. code-block:: devicetree

   /* acme-rigs/boards/shields/acme_grove_led/acme_grove_led.shield */
   #include <dt-bindings/connector/grove.h>
   #include <zephyr/dt-bindings/gpio/gpio.h>

   / {
           shield-templates {
                   acme_grove_led: acme_grove_led {
                           agl_plug: plug {
                                   compatible = "shield,plug";
                                   shield,plugs = "grove";
                           };

                           gpio {
                                   agl_led: led {
                                           shield,collect = "gpio-leds";
                                           gpios = <&agl_plug GROVE_SIG0 GPIO_ACTIVE_HIGH>;
                                   };
                           };
                   };
           };
   };

.. code-block:: yaml

   # acme-rigs/boards/shields/acme_grove_led/shield.yml
   shield:
     name: acme_grove_led
     full_name: ACME Grove LED
     vendor: acme
     template: true

Three things in that ``.shield`` file carry the whole idea:

``agl_plug: plug`` with ``compatible = "shield,plug"``
   The :term:`plug` — the module's own side of the connector, as a nexus
   node. It stands in for "whatever socket I end up in". A shield declares
   one node like this per plug it has; the node's name (``plug`` here) is
   just what this shield calls that slot, and a module with two connectors
   declares two such nodes with two names. Nothing about having one is a
   special case.

``shield,plugs = "grove"``
   What this plug mates with, declared *on the plug*. It is the same
   :term:`connector type` name the board's socket used, and it is the
   entire compatibility check: a Grove module goes in a Grove socket, and
   an attempt to put it anywhere else is rejected before the build starts.

``gpios = <&agl_plug GROVE_SIG0 GPIO_ACTIVE_HIGH>``
   The LED is wired to the connector's first signal. Not to ``gpioa 10``,
   not to ``D2`` — to ``GROVE_SIG0``, the same ``#define`` the board's
   ``gpio-map`` used on the other side.

That last line is why one file replaces sixty-four. The template never
names a pin, so it never has to be copied to reach a different one. When
the rig says which socket, the :term:`expander` resolves the position
through that socket's ``gpio-map`` and writes the real ``&gpioa 10`` into
the generated overlay. Same module, any socket, one file.

``shield,collect = "gpio-leds"`` says this device is an entry in the
board's shared ``gpio-leds`` collection rather than a node of its own, so
several instances merge into one ``gpio-keys``-style parent instead of
fighting over it.

Note also what is *not* in the file: no ``status = "okay"`` on a bus, no
``&i2c1``, no board reference of any kind. A template is
pre-instantiation text. It becomes a devicetree node only once something
places it.

Why ``template: true``
------------------------

``shield.yml`` is ordinary Zephyr shield metadata with one addition. The
flag marks this folder as a rig template — a shield whose ``.overlay`` has
been replaced by a ``.shield``. It is what lets a rig-aware tool tell your
module apart from a classic Zephyr shield sitting in the same directory
tree, and it is what makes the next tutorial's shortcut legal.

What you cannot do yet
------------------------

You have a socket and you have a module that mates with it. What you do
*not* have is anything that says one is plugged into the other — and
without that there is nothing to build. A template on its own is inert.

That missing sentence is a :term:`rig`, and the next two tutorials are two
ways of writing it: the fastest possible way, and the durable way.

Next
------

:doc:`build-a-rig-on-the-fly` builds this module on that socket without
writing a rig at all.
