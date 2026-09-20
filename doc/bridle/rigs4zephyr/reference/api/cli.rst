Front door
============

The command line, the run's sequence, and the exit code. This is the only
stage that decides *what happens next* rather than computing a value:
everything below it is called from :py:func:`rigc.cli._expand` in order,
and every rejection funnels back through one place.

``rigc.cli``
--------------

.. automodule:: rigc.cli

``rigc.__main__``
-------------------

.. automodule:: rigc.__main__

``rigc.promote``
------------------

.. automodule:: rigc.promote

``rigc.deps``
---------------

.. automodule:: rigc.deps

``rigc.unimplemented``
------------------------

.. automodule:: rigc.unimplemented
