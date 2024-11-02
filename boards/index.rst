.. _boards:

Supported Boards
################

The |BRIDLE| project developers are continually adding board-specific support as
documented below. If you are looking to add |BRIDLE| support for a new board,
please start with the upstream Zephyr :zephyr:ref:`board_porting_guide`. To add
support documentation for a new board, please use the template available under
:zephyr_file:`doc/templates/board.tmpl`

.. toctree::
   :maxdepth: 2
   :glob:

   */index

.. _boards-extensions:

Supported Extensions
####################

Boards already supported by Zephyr or other Zephyr modules can be extended
by downstream users. In some situations, certain hardware description or
:zephyr:ref:`choices <devicetree-chosen-nodes>` can not be added in the
upstream Zephyr repository, but they can be in a downstream project, where
custom bindings or driver classes can also be created. For more details about
board extensions read the upstream Zephyr :zephyr:ref:`board_porting_guide`,
section about **Board extensions**.

.. toctree::
   :maxdepth: 1
   :glob:

   extensions/**/index

.. _boards-shields:

Supported Shields
#################

.. toctree::
   :maxdepth: 1
   :glob:

   shields/**/index
