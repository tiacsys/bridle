.. _rigs4zephyr_explanation_build-integration:

How a rig build hooks into Zephyr
====================================

:ref:`rigs4zephyr_reference_commands` covers *what* a rig build accepts and
writes: ``-DRIG=<target>``, the files under ``build/rig/``, and the
:term:`rigc` command line. This page covers *why* the hook has the
shape it has. That means where ``rigc`` runs inside Zephyr's CMake module
chain, what it hands on to the rest of the build, which inputs it takes
over and which stay with the user, and what it needs from the Zephyr tree
underneath it.

.. contents::
   :local:
   :depth: 1

A rig build is an ordinary build with three modules shadowed
----------------------------------------------------------------

A Zephyr configure is a fixed chain of CMake modules that
``zephyr_default.cmake`` includes one after another: ``boards``,
``shields``, ``snippets``, ``hwm_v2``, ``configuration_files``, ``dts``,
``kconfig`` and the rest. Each one runs as a plain ``include(<name>)``, so
whatever file named ``<name>.cmake`` comes first on ``CMAKE_MODULE_PATH``
is the one that runs. Bridle's ``ZephyrBuildConfiguration`` package, which
Zephyr loads from the west manifest repository before that chain starts,
puts
``bridle/cmake/modules`` in front of Zephyr's own directory. That makes
``boards.cmake``, ``shields.cmake`` and ``dts.cmake`` there *forks*: they
shadow the upstream modules of the same name.

Shadowing is the only extension point the chain offers at the place a rig
has to act. A rig has to become a devicetree overlay and a shield list
after the board is known and before devicetree and Kconfig are assembled.
Zephyr has no hook between those two points. The overlay variables are
already final by the time ``dts`` runs, since ``configuration_files``
finalizes them, and the shield list is produced by a module that runs
before the board's hardware model is even loaded. A fork of the module
that owns each decision can act at exactly the right moment, with exactly
that module's variables in scope.

Each fork starts by dispatching. Without ``-DRIG``, it includes the real
upstream module by absolute path and does nothing else. (It uses the
absolute path because ``include(dts)`` would find the fork itself again.)
A plain build or a ``--shield`` build therefore runs Zephyr's own code,
unchanged. The one exception is a small include-path fix in the boards
fork that every build gets. A :term:`board extension`'s ``.dts`` lives in a
different directory from the base board it ``#include``\ s, and
``pre_dt.cmake`` never puts board directories on the preprocessor's search
path. So the fork adds the other board directories through the documented
``DTS_EXTRA_CPPFLAGS`` extension point. It only does this when the
resolved ``.dts`` really sits outside the base board's own directory.

The boards fork also does the rig's first piece of work. It asks
``list_rigs.py`` to resolve the full ``-DRIG`` target, and it refuses a
build that gives no board. A rig names a topology, not a board (see
:term:`invocation coordinate`), so the invocation is the only place a board
can come from.

The shields phase is empty, and ``-DSHIELD`` is refused
---------------------------------------------------------

In a rig build, which shields take part depends on the rig's expansion.
Nobody chooses them up front. Zephyr's ``shields`` module runs right after
``boards``, before ``hwm_v2`` and before the overlay variables are final,
so at that point in the chain nothing can know what a rig instantiates.
Nothing needs to know it yet either: the ``shields`` module's outputs
(``SHIELD_DIRS``, ``SHIELD_AS_LIST``, ``shield_conf_files``) are first read
by ``dts``. So in a rig build the shields fork has no work to do. It only
guards.

The guard refuses ``-DSHIELD`` next to ``-DRIG`` with a fatal error; the
flag is never silently ignored. A stock shield's overlay makes physical
claims of its own: pins, bus children, addresses, chip-selects. None of
that goes through ``rigc``'s analysis, so a shield that rides alongside a
rig could quietly collide with an instance that ``rigc`` has just allocated
to the same pins. That is the class of mistake rigs exist to catch.
Ignoring the flag would be worse still, because the user's request would
disappear without a trace. The guard reads ``SHIELD`` through
``zephyr_get``, so it also catches a value cached from an earlier
``--shield`` configure of the same build directory, and a ``SHIELD`` set in
the environment.

The rig takes over the *physical* inputs only: the board comes from the
invocation, and the shields come from the rig. Everything that is
*configuration* stays with the user: ``SNIPPET``, ``EXTRA_CONF_FILE``,
``EXTRA_DTC_OVERLAY_FILE``, and the application's own ``prj.conf`` and
overlays. A rig owns what is plugged in where, not how the firmware is
configured.

Everything happens inside the dts fork
----------------------------------------

The rig block lives in the ``dts`` fork because ``dts`` is the first slot
in the chain where everything it needs exists and where everything it
produces is still in time. ``hwm_v2`` has already run, so ``pre_dt.cmake``
can compute the architecture include directories. ``configuration_files``
has already finalized ``EXTRA_DTC_OVERLAY_FILE``, so there is a list to
prepend to. And ``kconfig``, which reads ``shield_conf_files`` and
``SHIELD_AS_LIST``, has not run yet. The block runs at file scope and is
never wrapped in a function, because those are exactly the variables it
must leave behind for the real ``dts.cmake`` and ``kconfig.cmake`` to read.
Its last line includes the real ``dts.cmake``. From that point on, the
build is Zephyr's.

The block processes the devicetree in two passes, with a clean boundary
between them.

**Pass 1** is ``rigc`` itself. It reads the board's real devicetree through
``edtlib``, together with the shield templates, and decides the whole
assembly. It sees the board as the board defines it: the board's ``.dts``
plus the include and bindings directories, and nothing from the
application. No app overlay, no ``EXTRA_DTC_OVERLAY_FILE`` and no snippet
reaches ``rigc``. So whether a rig fits a board is a property of the board
and the modules, and it does not change from one application to the next.
The flip side: an application overlay that reconfigures a socket's bus is
invisible to that analysis.

**Pass 2** is Zephyr's own devicetree processing of the board plus every
overlay, the generated one included, exactly as in any other build.

Pass 1 needs the same preprocessor and bindings recipe that pass 2 uses,
but pass 2 has not happened yet. In a fresh build directory there is no
``build_info.yml`` with a devicetree section to read the recipe from.
``rigc``'s ``--build-info`` option exists for standalone and test runs that
start from an earlier plain build. So the fork builds the recipe itself.
It includes the real ``pre_dt.cmake`` once, before ``rigc`` runs, and turns
the resulting ``DTS_ROOT_SYSTEM_INCLUDE_DIRS`` into ``--include-dir``
arguments. It derives ``--bindings-dir`` and ``--connector-dir`` with the
same ``<dts_root>/dts/bindings`` rule that upstream's
``dts_configuration_files()`` uses; that function only runs inside the real
``dts.cmake``. At this point ``SHIELD_DIRS`` is still empty. That does not
matter for pass 1, because ``rigc`` finds its templates through
``--shield-dir``. After ``rigc`` has named the shields, the fork calls
``pre_dt_module_run()`` a second time, so pass 2 gets shield bindings
folded into ``DTS_ROOT`` just as a ``--shield`` build would. It calls the
function rather than including the file again because ``pre_dt.cmake`` has
a global include guard, and a second ``include`` would silently do nothing.

What the rig adds, and why the user still wins
-------------------------------------------------

Devicetree files apply in list order, and a later file overrides an
earlier one. The fork *prepends* the rig's overlays to
``EXTRA_DTC_OVERLAY_FILE`` rather than appending or overwriting them.
Anything the user passed, and anything a snippet added, stays at the end
of the list and wins. Here is the real order for
``-b seeeduino_lotus samples/helloshell -- -DRIG=lotus_pwm_led
-DEXTRA_DTC_OVERLAY_FILE=u.overlay``:

.. code-block:: text

   -- Found BOARD.dts: .../boards/seeed/seeeduino_lotus/seeeduino_lotus.dts
   -- Found devicetree overlay: .../samples/helloshell/boards/seeeduino_lotus.overlay
   -- Found devicetree overlay: .../build/rig/rig-gen.overlay
   -- Found devicetree overlay: .../boards/rigs/lotus_pwm_led/lotus_pwm_led.overlay
   -- Found devicetree overlay: .../u.overlay

So the order is: board, then the application's own overlay, then the
generated ``rig-gen.overlay``, then the rig's hand-authored
``<rig>.overlay`` (then the variant overlay and the combined
variant-and-revision overlay, when selected), and last the user's extras.
The application overlay (``DTC_OVERLAY_FILE``) is a slot that comes before
every ``EXTRA_`` file, so the rig's devicetree overrides the application's.

Kconfig follows the same pattern through a different slot. Zephyr merges
the board defconfig, ``CONF_FILE`` (``prj.conf`` and its board-specific
``.conf``), then ``shield_conf_files``, then ``EXTRA_CONF_FILE``. The rig's
``<rig>_defconfig`` and its variant and revision fragments are *appended*
to ``shield_conf_files``, after each shield's own ``.conf``. Two
properties follow from upstream's merge order alone, with no reordering by
the fork: the rig overrides ``prj.conf``, and a user's ``EXTRA_CONF_FILE``
overrides the rig. The two use different slots for a reason. Kconfig
already has a slot that every rig build fills (the shield confs). The
devicetree has none, because the rig build never collects a shield's own
``.overlay``: ``rigc`` writes the whole devicetree contribution itself.

The hand-authored overlay is an escape hatch
----------------------------------------------

``<rig>.overlay`` is part of the output. ``rigc`` never parses it, never
models it and never checks it. It is applied after ``rig-gen.overlay``, so
it can reference the node labels that ``rigc`` generated, and ``dtc``
resolves them like any other labels. It exists for devicetree that the rig
model does not express. ``lotus_pwm_led`` shows the typical case:
``rig-gen.overlay`` enables ``&tcc0`` and routes each LED to its socket,
but SoC pinmux is board knowledge, and the Lotus's ``tcc0_pwm_default``
pinctrl state ships empty. So the rig's own overlay supplies the two
``pinmux`` groups.

Because nothing checks it, the escape hatch is also a way around every
guarantee a rig makes. ``rigc`` is the only author of bus children,
``reg`` addresses and ``cs-gpios``. If you write any of them from
``<rig>.overlay``, ``rigc``'s allocation is bypassed: the collision analysis
never sees them, and the :term:`config sheet` describes an assembly that is
no longer the one being built. A typo in a label there also only shows up
later, as a ``dtc`` error during the build.

Kconfig follows the devicetree
--------------------------------

Kconfig symbols are global, so there is no such thing as per-instance
Kconfig. Two buttons on two sockets are one ``INPUT_GPIO_KEYS``. Anything
that differs per device lives in the devicetree, and driver enablement
follows from it. The fork sets ``SHIELD_AS_LIST`` from the rig's shields,
so each shield's ``Kconfig.shield`` and ``Kconfig.defconfig`` fire exactly
as they do in a ``--shield`` build. Leaf drivers then default to on through
``DT_HAS_<compat>_ENABLED``, since the generated overlay creates their
nodes. What is left for the rig is umbrella subsystems. For example,
``lotus_buttons_defconfig`` turns on ``CONFIG_INPUT`` and ``CONFIG_LED``,
the bare menus that the ``gpio-keys`` and ``gpio-leds`` drivers live under.

``rigc`` itself writes no Kconfig. The fork has a slot for a generated
``build/rig/rig-gen.conf``: it would be merged ahead of ``<rig>_defconfig``
and recorded in ``build_info.yml``. But no ``rigc`` run produces that file
today. So every rig build prints ``Rig: no Kconfig fragment produced``. On a
healthy build that line is expected and does not mean anything went wrong.

Rebuilds track exactly what the run read
------------------------------------------

A rig build has to reconfigure when any file its expansion depends on
changes. Globbing for those files would guess. ``rigc`` knows, so it
reports them. ``context.cmake`` carries ``RIG_DEPENDS``: every source-tree
file that the run opened, sorted and absolute. The fork appends that list
to ``CMAKE_CONFIGURE_DEPENDS``. For ``lotus_pwm_led``, the list holds the
rig's two files, the board ``.dts``, ``grove_pwm_led.shield`` and its
``shield.yml``, and the ``grove`` connector binding and header.

The list is exactly what was read, no more and no less. If it left out a
file that was read, editing that file would leave a stale overlay. If it
included files that were never read, every edit anywhere in the shield
library would trigger a reconfigure. Shield templates are parsed only when
a rig references them, so a template the rig never names stays off the
list. The list is also a *history of resolution*, not a summary of the end
result. When a variant or revision delta swaps a shield out, the shield
that the base stage resolved stays in ``RIG_DEPENDS``. It was read, and a
change to it can still change the outcome, for example by making the base
stage reject.

``context.cmake`` only exists after a successful run, so a rig that fails to
expand would never report anything. That is why the fork also registers a
fixed set of files itself. The set contains ``rig.yml``, the content file
(registered even when it is missing, so creating it triggers a
reconfigure), ``<rig>_defconfig``, ``<rig>.overlay``, ``rigc``'s own
sources and ``list_rigs.py``.

The work directory is kept
----------------------------

``build/rig/rigc-generated/`` holds what the run actually fed its parsers:
each shield's devicetree fragment and its preprocessed form, the
preprocessed board devicetree, and the synthesized rig files for a
:term:`promoted shield`. It is kept on every exit, whether the run was
accepted or rejected. A diagnostic that points into a preprocessed file
needs that file in order to be read. And an accepted run is exactly the
one whose overlay somebody later questions.

Keeping it costs almost nothing. The name is fixed and the directory is
wiped when the next run starts, so a build directory holds exactly one of
them. It can never mix one run's intermediates with another run's
``rig-gen.overlay``, and ``west build -p`` reclaims it along with the rest
of the build.

A rig under twister is one ``extra_args`` line
------------------------------------------------

Twister always supplies the board: it is the platform it builds for. A rig
build takes its board from the invocation, so a rig fits into twister with
no changes to twister at all:

.. code-block:: yaml

   tests:
     rigs.lotus_buttons:
       platform_allow: seeeduino_lotus
       extra_args: RIG=lotus_buttons

Twister turns each ``extra_args`` entry into a ``-D`` argument, so the
entry reads ``RIG=``, just as ``SHIELD=`` does for a shield.

To fill ``platform_allow``, you need to know which boards can host a given
rig, and ``west rigs --boards-for`` answers that. The reverse question,
which rigs fit a given board, has no command: no build or test flow asks
it, and answering it would mean loading every rig in every board root.

The Zephyr tree must carry four patches
-----------------------------------------

The rig machinery relies on four changes to the Zephyr tree that a stock
upstream Zephyr does not have. Bridle's Zephyr branch carries them.

``edtlib`` accepts vendor-namespaced top-level binding keys
   A :term:`connector type`'s binding holds the plug side of the contract
   in the same file as the socket side, as comma-namespaced top-level keys
   (``plug,bus-proxies``, ``plug,positions`` in ``grove.yaml``). With the
   patch, keys that contain a comma are allowed and preserved in
   ``Binding.raw``; a ``-cells`` suffix keeps its usual meaning. Stock
   ``edtlib`` rejects any unknown top-level key as soon as it loads the
   binding, which it does whenever a ``socket,<type>`` node is in the
   devicetree. That includes ``rigc``'s pass 1, Zephyr's own pass 2, and
   even a plain build of a board such as ``seeeduino_lotus``, whose
   sockets are part of its base devicetree.

``edtlib`` checks only ``*-cells`` keys as cells lists
   Stock ``edtlib`` applies the shape check for ``*-cells`` lists to
   *every* top-level value, because of an operator-precedence error. As a
   result, a value that cannot be iterated crashes with a raw
   ``TypeError``, and a list of mappings is rejected as a malformed cells
   list. Once the patch above lets extension keys through, their values
   have to get past this check too.

``shield.yml`` accepts a ``template`` boolean
   ``template: true`` marks a :term:`shield template`, a shield that
   ``rigc`` unfolds instead of one that is applied as an overlay (see
   :ref:`rigs4zephyr_reference_promotion`). ``list_shields.py`` validates
   every ``shield.yml`` against Zephyr's shield schema, and that schema
   refuses unknown keys. On a stock tree it exits with ``Malformed shield
   YAML file`` on ``grove_btn`` or ``grove_led``. That breaks the rig
   build's shield resolution, and also every ``--shield`` build and every
   ``west shields`` run that scans bridle's board root.

``shield.yml`` accepts a ``revisions:`` block
   This declares the revisions a shield offers, so that one can be selected
   by name rather than by copying a whole shield folder for each hardware
   revision. It is refused by the same schema check, and it is needed by any
   shield template that declares a revision axis.

``build_info.yml`` records lists as joined strings
----------------------------------------------------

The fork writes what the rig build looked at into ``build_info.yml`` under
``cmake.vendor-specific.rig``, using Zephyr's own ``build_info()``. For
``vendor-specific`` entries, that function records every value as a
scalar. If you give it a multi-element CMake list, it keeps the first
element and drops the rest without any warning. So the fork joins each
list (shields, shield directories, applied fragments, shield revisions)
into one ``", "``-separated string before recording it:

.. code-block:: yaml

   vendor-specific:
     rig:
       board: 'seeeduino_lotus/samd21g18a'
       name: 'lotus_pwm_led'
       overlay: '.../boards/rigs/lotus_pwm_led/lotus_pwm_led.overlay'
       overlay-gen: '.../build/rig/rig-gen.overlay'
       shield-dirs: '.../boards/shields/grove_led'
       shields: 'grove_pwm_led'

A promoted target can itself contain ``;``. The fork escapes it five levels
deep so that it survives the macro chain inside ``build_info()``. That
depth is something measured against the current CMake modules, not a
promise anyone makes, so a Zephyr update that changes either macro can
break it.

.. seealso::

   :ref:`rigs4zephyr_reference_commands`
      The ``-DRIG`` rules, ``rigc expand``'s options, and every file a run
      writes.

   :ref:`rigs4zephyr_reference_rig-file`
      The fragment naming scheme that the fork collects from a rig folder.

   :ref:`rigs4zephyr_explanation_architecture`
      Why ``rigc``'s own pipeline is cut the way it is.
