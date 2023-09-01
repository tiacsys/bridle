.. _west-bridle-ext-cmds:

Additional Bridle extension commands
####################################

This page documents miscellaneous Bridle extensions for West.

.. _west-bridle-export:

Installing CMake packages: ``west bridle-export``
*************************************************

This command registers the current Bridle installation as a CMake config
package in the CMake user package registry.

In Windows, the CMake user package registry is found in
``HKEY_CURRENT_USER\Software\Kitware\CMake\Packages``.

In Linux and MacOS, the CMake user package registry is found in
:file:`~/.cmake/packages`.

You may run this command when setting up a Bridle workspace. If you do,
application CMakeLists.txt files that are outside of your workspace will
be able to find the Bridle repository with the following:

.. error:: TEMP-OFF for PDF with "rinoh"

.. TEMP-OFF for PDF with "rinoh"
.. .. code-block:: cmake
   :caption: Find the Bridle repository

   find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})

See :bridle_file:`share/bridle-package/cmake` for details.
