.. _rigs4zephyr_explanation_why-rigs:

Why rigs
==========

Zephyr already has a way to describe an add-on module: a shield, which is
a devicetree overlay applied on top of a board. This page explains why
that is not enough once a module has to appear twice, on one of several
connectors, or on more than one host board, and why the answer takes the
shape it does: a :term:`rig` file that names module instances, a
:term:`shield template` written in connector positions, and
:term:`rigc`, a tree transform whose output is an ordinary
overlay.

:ref:`rigs4zephyr_explanation_architecture` explains how ``rigc`` itself is
cut into stages. This page is about the problem those stages solve.

.. contents::
   :local:
   :depth: 1


A shield is a patch, not a type
-----------------------------------

Devicetree separates type from instance for *devices*. A binding is the
type, a node is the instance, and a driver instantiates itself once per
``okay`` node. For an *assembly* of nodes, a module with a button, an LED
and a sensor on it, there is no equivalent type. A shield overlay is a
reusable description written directly into instance space: it uses
concrete node paths, globally unique labels and concrete connector labels.
Overlays merge by path, so applying the same overlay a second time merges
into the same nodes instead of creating a second copy. That is why a
shield can only ever be placed once.

Shield authors work around this by namespacing by hand. Upstream Zephyr's
``adafruit_data_logger`` overlay suffixes every label with the shield's
name (``rtc0_adafruit_data_logger``, ``sdhc0_adafruit_data_logger``,
``green_led_adafruit_data_logger``), and it still supports only one copy.

Bridle's own Grove modules show what this costs once a module can sit on
any of several connectors. ``boards/shields/grove_btn_legacy`` carries 64
overlays for one Grove button: ``grove_btn_d0`` to ``grove_btn_d31``, each
in a normal and an ``_inv`` flavour. ``grove_led_legacy`` carries another
64 for the LED. Each overlay differs from its neighbours in one number and
one suffix:

.. code-block:: devicetree

   grove_btn_d2: grove-btn-d2 {
           label = "Grove Button D2";
           zephyr,code = <INPUT_KEY_2>;
           gpios = <&grove_gpios 2 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>;
   };

The "which pin" axis and the "inverted or not" axis are both encoded in
the file name, and a build can still select only one button of each
flavour.

A :term:`shield template` is the missing type. ``grove_btn.shield``
describes the button once, against a :term:`plug` and a :term:`position`
(``GROVE_SIG0``) rather than a pin. Each :term:`instance` in a rig gives
it a name, and ``rigc`` derives every label from that name. The
``lotus_buttons`` rig places two buttons and an LED. The overlay ``rigc``
emits for it on the Seeeduino Lotus holds two copies of the same template
side by side:

.. code-block:: devicetree

   btn_start_gb_key: btn_start_gb_key {
           zephyr,code = <INPUT_KEY_0>;
           gpios = <&grove_d2 0 0x20>;     /* SIG0 */
   };
   btn_stop_gb_key: btn_stop_gb_key {
           zephyr,code = <INPUT_KEY_1>;
           gpios = <&grove_d6 0 0x21>;     /* SIG0 inverted */
   };

The pin is chosen by the socket each instance is placed on, and
inversion is the ``invert:`` field of that instance. Nobody writes either
into a file name.


Connectors exist only by convention
---------------------------------------

Part of the connector story already works in upstream devicetree. A GPIO
nexus node (``gpio-map``) lets a shield write
``&arduino_header ARDUINO_HEADER_R3_D10`` and lets the board decide which
SoC pin that is. Nexus maps compose, and they are checked by machine.

Everything beyond GPIO is left to naming conventions. ``arduino_i2c``,
``arduino_spi`` and ``mikrobus_i2c`` are ordinary labels that point at SoC
bus nodes. Nothing declares which buses a connector carries. Nothing
checks that a module's needs match the connector it is plugged into, and
nothing records that a board has *four* connectors of one kind. Boards
with several connectors of the same kind invent numbered label families,
and every shield has to agree with every board on those names.

Bridle's Grove support is a large example of this. The board directories
hold 80 ``*grove*connector*.dtsi`` files spread across 13 directories,
which between them define 37 distinct ``grove_<n>_header`` labels. Board
files alias one label onto another (``grove_d2_header: &grove_d3_header``)
wherever the silkscreen and the wiring disagree. The ``grove`` base shield
alone ships 98 overlays, most of them per-board adaptations under
``boards/shields/grove/boards/``. The legacy button reaches its pin
through yet another label, ``grove_gpios``. Some boards define it
themselves; on others it exists only once one of the ``grove`` base
shields has been applied.

A rig turns the convention into data. A :term:`connector type`
(``dts/bindings/connectors/grove.yaml`` and its header of position
indices) states once what a Grove socket offers. A board declares each of
its connectors as a real :term:`socket` node with a ``socket,grove``
compatible; the Seeeduino Lotus declares nine in
``boards/seeed/seeeduino_lotus/grove_sockets.dtsi``, next to its existing
nexus nodes, which it leaves in place. Each socket keeps the standard
``gpio-map`` mechanism, and adds ``pwm-map`` and ``io-channel-map`` on the
pins that can do PWM or ADC. Once connectors are nodes with a type,
``rigc`` can check a placement against them. A module plugged into a
socket that cannot carry what it needs is rejected at configure time,
with the socket named, rather than failing later with a missing label.
:ref:`rigs4zephyr_reference_board-socket` lists what a socket can declare.


Composition is allocation, not concatenation
------------------------------------------------

When two overlays set the same property, the later value replaces the
earlier one. Devicetree has ``/delete-property/`` and ``/delete-node/``
but no append operator. Child nodes compose (two I²C devices at different
``reg`` addresses merge cleanly), but arrays owned by a parent and indexed
by its children do not.

``cs-gpios`` is the standard case. Upstream Zephyr's
``adafruit_data_logger``, ``adafruit_winc1500`` and ``link_board_eth``
shields each write the whole ``cs-gpios`` array of ``&arduino_spi``, and
each claims D10. Combine two of them and the last array wins without any
warning, while both SPI children still claim ``reg = <0>``. The problem is
tracked upstream as `zephyr#52948
<https://github.com/zephyrproject-rtos/zephyr/issues/52948>`_.

A missing ``+=`` is not the real difficulty. A SPI child's ``reg`` has to
equal its index in the parent's ``cs-gpios`` array. Putting two modules on
one bus therefore means assigning chip-select indices across the whole
bus and then rewriting each child's ``reg`` to match. That is resource
allocation, and no textual mechanism can do it, whether it is the C
preprocessor or an append operator. It needs a pass that sees the whole
assembly.

This is the strongest reason ``rigc`` is a program rather than a set of
preprocessor tricks. A socket offers a chip-select pool
(``socket,cs-pool``). A module either fixes its chip-select in copper
(``shield,cs-position``) or leaves it to the pool. ``rigc`` assigns the
positions, writes each ``cs-gpios`` array together with its children's
``reg`` values, and rejects an assembly whose pool runs out (``phys-cs``).
I²C addresses work the same way: ``rigc`` writes every ``reg`` and unit
address itself and rejects two devices fixed at one address in one bus
scope. :ref:`rigs4zephyr_reference_shield-template` and
:ref:`rigs4zephyr_reference_diagnostics` cover the details.


A tree transform with an ordinary overlay as its output
-----------------------------------------------------------

Instance namespacing, routing references through a socket, and allocation
are all computations over a whole tree. None of them needs new syntax. So
``rigc`` does not define a devicetree dialect with its own parser. It
reads ordinary inputs and writes one ordinary file, ``rig-gen.overlay``,
which the build places on ``EXTRA_DTC_OVERLAY_FILE``. From then on the
unchanged Zephyr devicetree pipeline takes over: the same ``dtc``, the same
``edtlib``, the same generated ``DT_*`` macros, the same drivers. Nothing
downstream can tell that an overlay was computed rather than written.

Three things follow from this choice:

- **The result can be inspected.** ``build/rig/rig-gen.overlay`` is plain
  devicetree that a person can read, diff and review, and the
  :term:`config sheet` beside it covers what the MCU cannot see: which
  module goes in which socket, and which jumper to set. See
  :ref:`rigs4zephyr_reference_commands` for everything a run writes.
- **Plain builds are untouched.** Bridle steps into the ``boards``,
  ``shields`` and ``dts`` build modules only when ``-DRIG`` is given.
  Without it, every build, ``--shield`` builds included, runs the upstream
  modules unchanged.
- **Hand-written devicetree still has a place.** A rig folder may carry
  its own ``<rig>.overlay`` for things a template cannot express yet.
  ``lotus_pwm_led.overlay`` supplies the SoC pinmux that the Lotus board
  leaves empty and that ``rigc`` deliberately does not write.


Why the topology is YAML and the modules stay devicetree
------------------------------------------------------------

A rig is made of three kinds of file, and they are written in two
languages on purpose.

Shield templates and board sockets are devicetree. What they describe
ends up in the devicetree, so they use its syntax, its preprocessor, its
bindings and stock ``dtlib`` to parse them. A shield template reads like
the overlay it replaces, with plug positions where the pins used to be.

The rig itself, :term:`rig metadata file` plus :term:`rig content file`,
is YAML. The main reason is what an author sees when they get something
wrong. A rig is mostly references: an instance to a shield, an instance to
a socket, a parameter to a device inside an instance. Stock ``dtlib``
resolves a ``&label`` inside a property value only after parsing has
finished. Its error then carries the node path alone, with no file or
line and no list of names that would have been valid, and it stops at the
first one. A rig topology written in devicetree would fare worse still,
because per-instance nodes do not exist until ``rigc`` has expanded the
rig, so "instance 2's button" could not even be a real ``&label``. A
dedicated loader can report precisely what went wrong and where:

.. code-block:: text

   error[lang-instance-shield]: instance 'b1': unknown shield 'grove_bnt'
       known shields: grove_btn, grove_led, grove_pwm_led
       at .../bad.yml:3 (instances[0].shield)

YAML also puts ``rig.yml`` next to the ``board.yml`` and ``shield.yml``
files a Zephyr developer already knows. Because only the topology file
changes language, the change stays small: shield payloads and board
fragments are still devicetree.
:ref:`rigs4zephyr_reference_rig-file` lists what each rig file may
declare.


The build coordinate is board × rig
---------------------------------------

A rig names shield instances and says where they are plugged. It does not
name a board. The board comes from the invocation, exactly as it does for
any Zephyr build:

.. code-block:: console

   $ west build -b seeeduino_lotus <app> -- -DRIG=lotus_buttons

What to build is therefore a pair, the :term:`invocation coordinate`, and
its two halves vary independently. The same rig can be built against any
board whose sockets satisfy it, and a rig build with no board given is a
configure error rather than a fallback. ``west rigs --boards-for`` asks
the same question the other way round: which boards could host this
target (:ref:`rigs4zephyr_reference_commands` explains what it can and
cannot conclude).

Two identity cases pin down where rigs meet plain Zephyr:

- **The empty rig is the plain board.** A rig with ``instances: []``
  produces an overlay that holds no nodes at all, so the devicetree built
  is the board's own.
- **A single shield is a rig of one instance.** Naming a template shield
  where a rig is expected, for example
  ``-DRIG='grove_led:socket=grove_a0'``, desugars to a rig with one
  instance of that shield. ``west rigs --explain`` prints the two files it
  stands for, and a checked-in rig with that content builds the same
  thing. This is the rig counterpart of ``--shield``. The ``socket=`` is
  needed here because the Lotus has nine Grove sockets; ``rigc`` infers a
  socket only when exactly one on the board fits. See
  :term:`promoted shield` and :ref:`rigs4zephyr_reference_promotion`.

A rig build takes its shields from the rig and nowhere else, so
``--shield`` together with ``-DRIG`` is a fatal configure error, not a
second source of modules.

Because a shield name can stand where a rig name does, the two share one
namespace. A name that is only a rig resolves as that rig. A name that is
only a promotable shield resolves as a promotion. A name that matches both
is refused with both paths named. It is never resolved by precedence,
because the author meant one of them and ``rigc`` cannot know which.


How this relates to upstream Zephyr efforts
-----------------------------------------------

Upstream Zephyr's closest proposal is `RFC #82889
<https://github.com/zephyrproject-rtos/zephyr/issues/82889>`_, "Introduce
option parameter for shields". It extends ``--shield`` to the form
``<shield_name>[@<index>][:<option>{=<value>}...]``. Overlays are
parameterized through preprocessor macros, and the build generates a
"derived overlay" for each instance given on the command line. Grove is
its motivating example: moving a module to another connector, and using
the same shield more than once. The RFC is open. Its implementation, `PR
#82825 <https://github.com/zephyrproject-rtos/zephyr/pull/82825>`_, was
closed without being merged in February 2026.

The two approaches start from the same problem and differ in where the
topology lives and what does the work:

- In the RFC, the topology lives on the ``west build`` command line and
  the reuse unit is still an overlay, substituted per instance. In a rig,
  the topology is a checked-in file, and the reuse unit is a template
  written in connector positions.
- Per-instance text substitution can rename labels and change values. It
  cannot allocate chip-selects across instances or reject two modules at
  one address, because each derived overlay is produced without seeing
  the others. ``rigc`` analyzes the whole assembly before it emits
  anything.
- The shapes of the command-line grammars are close.
  :ref:`rigs4zephyr_reference_promotion` also uses
  ``name[@...][:key=value...]``. In ``rigc``, though, ``@`` selects a
  shield's revision, following hwmv2, and an instance's identity is a name
  in the rig rather than an index.

On the board side, rig sockets reuse the nexus mechanism upstream Zephyr
already has. A socket is a ``gpio-map`` nexus node, with the standard
``pwm-map`` and ``io-channel-map`` added where they apply, and ``rigc``
reads those maps through ``edtlib`` in the usual way. What a socket adds
is a type and an identity: a compatible that names its connector type,
and a node that ``rigc`` can check a module against.


.. seealso::

   :ref:`rigs4zephyr_explanation_architecture`
      How ``rigc`` itself is structured, and why.

   :ref:`rigs4zephyr_tutorials_build-a-rig-that-exists`
      ``lotus_buttons`` and ``lotus_pwm_led``, built end to end.

   :ref:`rigs4zephyr_reference_glossary`
      Every term used on this page.
