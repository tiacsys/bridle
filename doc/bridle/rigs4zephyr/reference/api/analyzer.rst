Analyzer
==========

Rig model plus board in, solved rig out — or a diagnostic naming the pin.
Everything this stage rejects is something the *hardware* gets wrong: a
plug that does not mate, a position that is not routed, two devices at one
address, no chip-select left to allocate.

Each pass is a value function returning its own piece plus its
diagnostics; ``rigc.analyzer.analyze`` is the one composer that runs them
in order.

``rigc.analyzer``
-------------------

.. automodule:: rigc.analyzer

``rigc.analyzer.sockets``
---------------------------

.. automodule:: rigc.analyzer.sockets

``rigc.analyzer.socketmap``
-----------------------------

.. automodule:: rigc.analyzer.socketmap

``rigc.analyzer.gpio``
------------------------

.. automodule:: rigc.analyzer.gpio

``rigc.analyzer.addresses``
-----------------------------

.. automodule:: rigc.analyzer.addresses

``rigc.analyzer.cs``
----------------------

.. automodule:: rigc.analyzer.cs

``rigc.analyzer.wires``
-------------------------

.. automodule:: rigc.analyzer.wires

``rigc.analyzer.ordering``
----------------------------

.. automodule:: rigc.analyzer.ordering

``rigc.analyzer.labels``
--------------------------

.. automodule:: rigc.analyzer.labels
