.. _rigs4zephyr_reference_api_junit_html:

Test-report rendering
========================

Not a pipeline stage: ``scripts/rigc/check.sh`` calls this module after
every pytest invocation to render a browsable HTML report from the
``--junitxml`` file, including on a failed run. In btr-shields, the repo
this documentation set was ported from, this module lives at
``scripts/junit_html.py`` — a sibling of ``rigc/``, not a member of the
package. In bridle it landed inside ``scripts/rigc/`` itself, so it is a
real ``rigc`` submodule here and is documented for that reason, not
because it belongs to :ref:`the expander pipeline <rigs4zephyr_reference_api_index>`.

``rigc.junit_html``
----------------------

.. automodule:: rigc.junit_html
