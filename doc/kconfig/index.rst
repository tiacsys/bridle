.. _index:
.. _kconfig-search:
.. _configuration_options:

Kconfig Search
##############

This is a searchable reference documentation for all
:external+zephyr:ref:`Kconfig <kconfig>` options as it is used for Zephyr and
Bridle development. For a high-level guide, see :external+zephyr:ref:`kconfig`.
For a platform-independent specification, see the official
`Kconfig language documentation`_.

.. _Kconfig language documentation:
   https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html

:file:`Kconfig` files describe build-time configuration options (called
symbols in Kconfig-speak), how they are grouped into menus and sub-menus,
and dependencies between them that determine what configurations are valid.
:file:`Kconfig` files appear throughout the directory tree. For example,
:file:`subsys/shell/modules/Kconfig` defines Bridle related shell options.

All :file:`Kconfig` options can be searched using the search functionality.
The search functionality supports searching using regular expressions. See
:ref:`kconfig-regex` for more information. All the :file:`Kconfig` options
that match a particular regular expression is displayed along with the
information on the matched :file:`Kconfig` options. The search results
can be navigated page by page if the number of matches exceeds a page.

.. kconfig:search::

.. toctree::
   :maxdepth: 1
   :hidden:

   regex
