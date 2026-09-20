The expander's architecture
==============================

:doc:`/reference/api/index` says *what* each stage of the :term:`expander`
does and lets each module's own docstring say *how*. This page is the
missing third layer: *why* the pipeline is cut into five stages at those
particular boundaries, and why a handful of disciplines — diagnostics as
values, an emitter that cannot fail, deterministic output — show up in
every one of them rather than being a rule for one module alone.

Two things can be wrong with a rig, and the pipeline is cut along that line
------------------------------------------------------------------------------

A rig can be wrong in two unrelated ways. Its *files* can be wrong: a
reference to an instance that was never declared, an axis value nobody
defined, a shield name that does not exist in the library. Or the
*hardware* it describes can be wrong: two devices fixed at the same I²C
address, a chip-select pool with more claimants than positions, a module
that needs a bus the socket it is plugged into never exposes. Neither
category of mistake can be caught by the same kind of check, and neither
needs to see the other's evidence: a dangling reference is a fact about
text, and a mating impossibility is a fact about copper. The
:doc:`/reference/api/loader` and :doc:`/reference/api/analyzer` stages
exist because rejecting a rig on paper and rejecting it on physical
grounds are different jobs — one reads YAML and a shield library, the
other reads solved addresses, positions, and nets — and giving them one
name would hide which of the two the eventual diagnostic is about.

Between them sits the :doc:`/reference/api/board` stage, split off for a
reason that has nothing to do with that files-versus-hardware line: it is
the only stage that needs a build recipe. Reading a rig's own files is
just parsing YAML; reading what a board actually offers means running the
C preprocessor over a real devicetree and building an ``edtlib.EDT``
from it, which needs include directories and bindings resolved the way a
real Zephyr build resolves them. That is a different kind of IO from
everything around it, so it gets its own stage rather than being folded
into the loader (which never needs a board to assemble a topology) or the
analyzer (which never touches a filesystem at all — it only ever sees the
``Board`` value the board reader already built).

The :doc:`/reference/api/cli` stage is the odd one out on purpose: it is
the only place in the pipeline that decides *what happens next* rather
than computing a value. Every other stage is a function from inputs to
``(result, diagnostics)``; the CLI is the one place that calls them in
order, desugars a promoted shield into the rig files the rest of the
pipeline reads, and turns a diagnostics list into an exit code. Keeping
that sequencing in one place — rather than letting, say, the loader decide
whether to go on to the board reader — is what lets every other stage stay
a pure value function with no opinion about the run as a whole.

:doc:`/reference/api/model` is not a sixth stage; it is the vocabulary the
other five share. Every stage reads and returns the same handful of
dataclasses — ``Rig``, ``Board``, the analyzer's ``Solved`` — instead of
inventing its own shape for "a rig" or "a board" and translating at every
boundary. The nearest thing already in a Zephyr tree is ``edtlib.EDT``:
an EDT is the semantic model of one
devicetree, built once and read by everything downstream of it; the rig
model plays the same role one level up, standing for the assembly a board
and its plugged-in modules make together.

Why diagnostics are values
-----------------------------

Nothing in the expander threads a mutable "report problems here" object
through a call chain, and no pass raises to signal an ordinary finding.
A function that finds something wrong about the rig returns a
``Diagnostic`` — or a list of them — alongside its actual result;
composition all the way up to the CLI is just list concatenation. This
buys three things a mutable accumulator or a control-flow exception would
not.

First, every pass is unit-testable on its own: call it with a rig and a
board, and its diagnostics are sitting right there in the return value,
with nothing to mock. Second, it makes the failure mode where a real
finding silently disappears structurally hard to reach. A rig that fails
to *parse* at all still has to raise (there is no partial value to return
alongside), but even that path — ``LoadError`` — carries every diagnostic
gathered before the raise, so the exception message is never the only
finding an author sees. A pass whose socket never resolved does not
abort the run either; it is simply absent from the resolution the later
passes consult, and every one of those passes already treats
absence as "skip this one," so one bad slot cannot swallow the rest of
the rig's diagnostics.

Third, and most concretely: because diagnostics are ordinary data, one
function renders all of them into text, and that one function's output is
a frozen, testable contract — the exact stderr bytes a rig produces on
rejection are part of the expander's golden-test corpus, the same way its
accepted artifacts are. A change that reorders findings or reformats an
anchor path is a test failure, not a matter of taste, because authors and
CI scripts alike read that text.

Why the emitter cannot fail
-------------------------------

By the time the :doc:`/reference/api/emitter` stage runs, every decision
about whether the rig is physically buildable has already been made — by
the analyzer, against the board the CLI resolved earlier. The analyzer's
output, ``Solved``, is a frozen value precisely so that guarantee holds:
nothing downstream of it can quietly patch in one more allocation or
retract one more socket resolution after the fact. Freezing it also fixes
who owns what — a pass rebinding a field that a different pass already
produced is the failure mode this design set out to make impossible, and
a frozen dataclass turns an accidental rebind into a ``TypeError`` instead
of a silent divergence between what the analyzer decided and what the
emitter renders.

Given that contract, the emitter has no error class of its own to define.
It reads ``Solved`` plus the rig and the connector types, and renders —
never allocates, never validates, never rejects. That is also why its
output does not depend on the order instances were authored in: every
renderer sorts by a stable key (instance name, device label, bus path)
rather than walking a dict in insertion order, so two rigs that plug the
same modules into the same sockets in a different order in the YAML
produce byte-identical artifacts. Determinism here is not a nice-to-have
bolted on afterward; it falls directly out of "the emitter only renders
what the analyzer already decided," because a decision has no notion of
which line of the rig file mentioned it first.

Output determinism as the project's specification
------------------------------------------------------

That same discipline — sort by a stable key, never rely on authoring or
dict-insertion order — runs through every stage, not just the emitter.
It is what makes the corpus of golden tests meaningful as a specification
rather than merely a regression net: because every artifact and every
diagnostic the pipeline produces is a pure function of the rig's and
board's *content*, not of how either was typed, a byte-for-byte comparison
against a recorded overlay, config sheet, or stderr transcript is asking
the right question. If two runs over equivalent input ever produced
different bytes, no fixed golden could describe the tool's behavior at
all — so the goldens being byte-frozen and the pipeline being
deterministic are the same property, looked at from two ends. Changing a
diagnostic's wording, an artifact's key order, or an allocator's tie-break
rule is consequently always a deliberate, visible act: the golden moves
in the same change that explains why.

One model, one seam per rule
--------------------------------

A handful of small accessor modules exist for a reason that is easy to
mistake for over-engineering until the alternative is spelled out: the
socket-resolution accessors inside the :doc:`/reference/api/analyzer`
stage and the bus-kind matcher shared by the loader, the board reader and
the analyzer each give one rule — "which socket does this reference
resolve to," "does this bus name mean spi" — exactly one implementation
that every caller shares. Without that seam, each of the loader, the board
reader and the analyzer would grow its own copy of the same lookup, and
the three copies would drift the moment one of them needed to handle a
case (a role-suffixed bus name, a carrier's nested slot) the others had
not seen yet. A seam is not an abstraction for its own sake here; it is
the place a physical rule about the hardware lives exactly once, so that
fixing it once actually fixes it everywhere it applies.

The rig model plays the equivalent role for *data* rather than for a
single rule: it is what lets the loader, the board reader, the analyzer
and the emitter agree on what a socket, an instance, or a wire *is*
without any of them reaching into another stage's internals. A stage that
needs a fact about a rig asks the model for it; it never re-derives that
fact from the raw YAML or the raw devicetree a different stage already
turned into a model value.
