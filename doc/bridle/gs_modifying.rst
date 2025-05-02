.. _gs_modifying:

Modifying a sample application
##############################

.. contents::
   :local:
   :depth: 2

After programming and testing a sample application, you probably want to make
some modifications to the application, for example, add your own files with
additional functionality, change compilation options, or update the default
configuration.

Adding files and changing compiler settings
*******************************************

All files that your application uses must be specified in the
:file:`CMakeLists.txt` file. By default, most samples include only the main
application file :file:`src/main.c`. This means that you must add all other
files that you are using.

You can also configure compiler options, application defines, or include
directories, or set :ref:`build types <gs_modifying_build_types>` in
:file:`CMakeLists.txt`.

To update the :file:`CMakeLists.txt` file, either edit it directly or
use ... t.b.d. (TBD) IDE.

Editing CMakeLists.txt directly
===============================

Add all files that your application uses to the ``target_sources`` function in
:file:`CMakeLists.txt`. To include several files, it can be useful to specify
them with a wildcard. For example, to include all :file:`.c` files from the
:file:`src` folder, add the following lines to your :file:`CMakeLists.txt`::

   FILE(GLOB app_sources src/*.c)
   target_sources(app PRIVATE ${app_sources})

Instead of specifying each file (explicitly or with a wildcard), you can
include all files from a folder by adding that folder as include folder::

   target_include_directories(app PRIVATE src)

See the `CMake documentation`_ and :external+zephyr:ref:`cmake-details`
in the Zephyr documentation for more information about how to edit
:file:`CMakeLists.txt`.

Maintaining CMakeLists.txt in ... t.b.d. (TBD) IDE
==================================================

t.b.d.

.. _configure_application:

Configuring your application
****************************

If your application uses a provided library or targets a specific board, you
might want to change the default configuration of the library or board. There
are different ways of doing this, but not all will store your configuration
permanently.

The default configuration for a library is specified in its :file:`Kconfig`
file. Similarly, the default configuration for a board is specified in its
:file:`*_defconfig` file (and its :file:`Kconfig.defconfig` file, see
:external+zephyr:ref:`default_board_configuration` in the Zephyr documentation
for more information). The configuration for your application, which might
override some default options of the libraries or the board, is specified
in a :file:`prj.conf` file in the application directory.

For detailed information about configuration options, see
:external+zephyr:ref:`application-kconfig` in the Zephyr documentation.

Changing the configuration permanently
======================================

To configure your application and maintain the configuration when you clean
the build directory, add your changes to the :file:`prj.conf` file in your
application directory. In this file, you can specify different values for
configuration options that are defined by a library or board, and you can
add configuration options that are specific to your application.

See :external+zephyr:ref:`setting_configuration_values` in the Zephyr
documentation for information on how to edit the :file:`prj.conf` file.

.. note::

   It is possible to change the default configuration for a library by
   changing the :file:`Kconfig` file of the library. However, best practice is
   to override the configuration in the application configuration file
   :file:`prj.conf`.

Changing the configuration temporarily
======================================

When building your application, the different :file:`Kconfig` and
:file:`*_defconfig` files and the :file:`prj.conf` file are merged together.
The combined configuration is saved in a :file:`zephyr/.config` file in your
build directory. This means that this file is available when building the
application, but it is deleted when you clean the build directory.

To quickly test different configuration options, or to build your application
in different variants, you can update the :file:`.config` file in the build
directory. While it is possible to edit the :file:`.config` file directly,
you should use a tool like menuconfig or guiconfig to update it. These tools
present all available options and allow you to select the ones that you need.

See :external+zephyr:ref:`menuconfig` in the Zephyr documentation for
instructions on how to run menuconfig or guiconfig.

To locate a specific configuration option, use the filter (:guilabel:`Jump to`
in menuconfig and guiconfig). The documentation for each
:ref:`configuration option <kconfig:configuration_options>` also lists the menu
path where the option can be found.

.. important:: All changes to the :file:`.config` file are lost when you clean
   your build directory. You can save it to another location, but you must then
   manually copy it back to your build directory.

.. _cmake_options:

Providing CMake options
***********************

You can provide additional options for building your application to the CMake
process, which can be useful, for example, to switch between different build
scenarios. These options are specified when CMake is run, thus not during the
actual build, but when configuring the build.

If you work on the command line, pass the additional options to the
``west build`` command. The options must be added after a ``--`` at
the end of the command. See :external+zephyr:ref:`west-building-cmake-args`
for more information.

.. _gs_modifying_build_types:

Configuring build types
***********************

Build types enable you to use different sets of configuration options for each
board. You can create several build type :file:`.conf` files per board and
select one of them when building the application. This means that you do not
have to use one :file:`prj.conf` file for your project and modify it each time
to fit your needs.

.. note::

   Creating build types and selecting them is optional.

.. _gs_modifying_build_types_creating:

Creating build type files
=========================

To create custom build type files for your application instead of using a single
:file:`prj.conf` file, complete the following steps:

#. During :external+zephyr:ref:`application development <application>`, follow
   the procedure for creating the application until after the step where
   you create the :file:`CMakeLists.txt` file.
#. In the :file:`CMakeLists.txt` file, define the file name pattern for
   configuration files. For example::

      set(CONF_FILE "app_${CMAKE_BUILD_TYPE}.conf")

   In this define, ``CMAKE_BUILD_TYPE`` will be used for selecting the
   build type.
#. Optionally, include an if statement that checks for the presence of the
   selected build type configuration files.
   .. For an example, see :file:`applications/bridle_desktop/CMakeLists.txt`.
#. Continue the application creation procedure by setting the Kconfig
   configuration options.
#. Save the :file:`.conf` file in the application directory with a name
   that matches the file name pattern defined in CMakeLists. For example,
   :file:`app_ZRelease.conf`. In this file name, ``ZRelease`` is the build
   type name.

You can now select build types from command line.

Selecting a build type from command line
========================================

To select the build type when building the application from command line,
specify the build type by adding the following parameter to the
``west build`` command:

.. parsed-literal::
   :class: highlight

   -- -DCMAKE_BUILD_TYPE=\ *selected_build_type*\

For example, you can replace the *selected_build_type* variable to build the
``ZRelease`` firmware for PCA20041 by running the following command in the
project directory:

.. parsed-literal::
   :class: highlight

   west build -b bridle_board -d build_board -- -DCMAKE_BUILD_TYPE=ZRelease

The ``build_board`` parameter specifies the output directory for the build files.
