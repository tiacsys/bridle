Glossary
=========

.. glossary::
   :sorted:

   rig
      The set of modules plugged into a board's sockets, described as
      data. A rig is two files in ``boards/rigs/<name>/``: the
      :term:`rig metadata file` and the :term:`rig content file` (see
      :doc:`rig-file` for what each one declares). Neither names a board
      — a rig is a topology, and the board is the other half of the
      :term:`invocation coordinate`. It is built with
      ``west build -b <board> <app> -- -DRIG=<name>``. A single shield,
      or a small list of them, can also become a rig with neither file
      ever written — see :doc:`promotion`.

   connector type
      The contract a family of sockets shares — which :term:`position`\ s
      exist, which buses may cross the connector, whether two modules may
      stack on one socket. Authored once as a devicetree binding under
      ``dts/bindings/connectors/<type>.yaml`` plus a header of position
      indices, and named by the ``socket,<type>`` compatible. ``grove``,
      ``arduino-r3``, ``mikrobus`` and ``i2c-port`` exist today.

   socket
      A physical connector on a board, declared as a real devicetree node
      with a ``socket,<type>`` compatible. Declaring one is how a board
      opts in to rigs: a board with no socket node is not rig-enabled.
      A socket maps each :term:`position` of its :term:`connector type` to
      an actual SoC pin, and declares which buses it exposes.

   plug
      The module side of a connector, declared inside a
      :term:`shield template` as a nexus node. A module's devices
      reference the plug and a :term:`position` — never a board pin — which
      is what makes the same template usable on any matching socket.

   position
      A numbered signal on a :term:`connector type`, named by a ``#define``
      in that type's header (``GROVE_SIG0``, ``ARDUINO_HEADER_R3_D7``,
      ``MIKROBUS_AN``). The single source of truth shared by socket
      ``gpio-map``\ s and shield references alike: the board says which pin
      a position reaches, the module says which position it uses, and
      neither has to know the other.

   shield template
      A module described once, in positions rather than pins:
      ``boards/shields/<name>/<name>.shield``. Unlike a Zephyr shield
      overlay, a template is not applied directly — it is *instantiated*,
      so the same module can appear several times in one rig, on different
      sockets, with different per-instance settings. A shield whose own
      ``shield.yml`` declares ``template: true`` can also be built
      directly as a rig of one instance, with no rig files of its own —
      see :doc:`promotion`.

   instance
      One placement of a :term:`shield template` in a rig: a name, the
      shield it instantiates, and where it is plugged. Instances are what
      a :term:`rig content file` lists.

   promoted shield
      A single :term:`shield template` (or a small ``;``-separated list
      of them) built directly as a rig of one instance per shield, with
      neither a :term:`rig metadata file` nor a :term:`rig content file`
      ever written to disk — the natural mapping "one shield is a rig of
      one instance", desugared on the fly wherever a rig target is
      accepted. Only a shield whose own ``shield.yml`` declares
      ``template: true`` qualifies. Full grammar and refusals:
      :doc:`promotion`.

   rig metadata file
      ``boards/rigs/<name>/rig.yml`` — the rig's identity and its axes
      (name, optional variants and revisions). Carries no hardware
      description at all, and no board. Full grammar: :doc:`rig-file`.

   rig content file
      ``boards/rigs/<name>/<name>.yml`` — the assembly itself:
      :term:`instance`\ s, wires, and any headers the rig's parameters need.
      Named after the rig, and required. Full grammar: :doc:`rig-file`.

   board extension
      A directory under ``boards/extend/`` that adds a ``rig`` variant to an
      existing upstream board — its ``board.yml`` names the base board with
      ``extend:``, and its devicetree pulls the base board in and layers
      typed :term:`socket` nodes on top. The base board is never modified.

   expander
      ``rigc``, the tool that reads a rig, checks that the assembly is
      physically possible, and emits the devicetree overlay and the build
      glue. It runs during ``cmake`` configure, before devicetree is
      processed, so a rejected rig fails the configure rather than the
      build.

   invocation coordinate
      The pair naming what to build: a board and a rig, given
      independently (``-b``/``--board`` and ``-DRIG=``). The invocation is
      the *only* source of the board — no rig file declares one — so the
      same rig can be built against any board whose sockets satisfy it,
      and a rig build with no board given is a configure error.

   carrier
      A :term:`shield template` that itself provides :term:`socket`\ s, so
      other modules can plug into it — an I²C multiplexer, or a
      click-adapter shield. Instances plugged into a carrier name their
      socket as ``<carrier instance>.<socket>``.

   config sheet
      ``config-sheet.md``, one of the files the :term:`expander` emits: the
      human-facing wiring instructions for the rig — which module goes in
      which socket, which jumper to set, which chip-select each device
      ended up on.

   routing jumper
      A solder jumper or strap on a :term:`shield template` that selects
      which :term:`position` a signal reaches the :term:`plug` on — a
      config element carrying a ``shield,position-domain``. The choice is
      the rig's to make, so a device referencing one supplies flags only
      and leaves the position to the jumper, which is why a jumper node
      declares ``#gpio-cells = <1>`` where a plug declares no cell counts
      at all. Only meaningful on a shield with exactly one plug: the
      position domain has no plug axis.
