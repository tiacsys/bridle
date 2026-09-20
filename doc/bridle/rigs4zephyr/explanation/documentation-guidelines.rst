Documentation guidelines
==========================

The rules this documentation set follows, stated as norms — a checklist
for anyone (human or AI) writing or reviewing a page here.

Format
--------

- **reStructuredText only** — no MyST, no Markdown, anywhere under
  ``doc/``.
- **Sphinx** with **sphinx-rtd-theme**; docs live in ``doc/`` (singular),
  not ``docs/``.
- Builds must pass ``sphinx-build -W`` with **zero warnings** — a broken
  cross-reference or an unresolved ``:term:`` fails the build, not just a
  review comment. See :doc:`../howto/build-the-docs`.
- **Every page is reachable from a toctree.** No orphan pages, no dangling
  references.

Structure
-----------

Every page lives in one of the four `Diátaxis <https://diataxis.fr/>`_
quadrants, decided *before* writing, not after:

- **Tutorial** — learning by doing: a guided path to a working result.
- **How-to guide** — a task recipe for someone who already knows their way
  around.
- **Reference** — facts to look up: precise, complete, no narrative.
- **Explanation** — understanding: the reasoning behind how or why
  something is built the way it is.

The design record — briefs, rulings, design log — is **not** documentation
and does not live here. It stays under ``claude/``. A page in ``doc/``
states what the tool does today; it never narrates how the team arrived at
it, who decided what, or which alternative was rejected.

Tutorials
-----------

- **One new concept per tutorial**, named in a bold sentence near the top.
  A page that teaches two things is two pages.
- **Tutorials are ordered and cumulative.** Each states its prerequisites
  in an ``.. admonition:: Prerequisites`` and links the previous page;
  each ends with a ``Next`` section linking the following one. The series
  moves from the familiar (build something that exists) toward the
  powerful (carriers, parameters, one rig on many boards).
- **A running narrative cast**, consistent across the series, so the
  hardware story accumulates instead of resetting each page.
- **Every command and every output block is real.** Run it, paste it, trim
  it for width — never invent plausible-looking output. Output that cannot
  be produced yet belongs in a tutorial marked as a design target, and
  nowhere else.
- Explain *between* the commands, not after them. A tutorial that is a
  list of commands with a paragraph at the end has taught nothing.

Honesty about maturity
------------------------

- Anything not yet implemented is explicitly hedged as a **design
  target** — say so on the page; do not let present-tense prose imply
  otherwise.
- A tutorial for functionality that has not shipped opens with a bold
  ``.. warning::`` reading **"This tutorial does not work yet."** as the
  very first content on the page, and points at the working alternative if
  there is one.
- When such functionality ships, the warning is deleted in the **same
  change** that ships it, and the tutorial's commands and outputs are
  re-captured from a real run.
- Never promise a page or a feature that does not exist yet — link only to
  what is actually written.

Vocabulary
------------

- The glossary owns nuanced terminology. Define a term once, in
  :doc:`../reference/glossary`, and use ``:term:`` at its first occurrence
  on every other page.
- Write for Zephyr developers: the reader knows devicetree, ``west`` and
  shields, and does not know anything about rigs. Reach for the shield
  they already understand as the point of comparison.
- Prefer the reader's word over the implementation's. The tool calls the
  expander ``rigc``; a tutorial says "the expander" and lets the glossary
  carry the name.

Diagrams
----------

Diagrams use ``.. graphviz::`` and render to SVG. A diagram earns its place
by showing a relationship prose cannot — a socket/plug/position triangle, a
carrier chain — never as decoration for something a sentence already said.
