.. _doc_build:

Building |BRIDLE| documentation
###############################

.. contents::
   :local:
   :depth: 2

The |BRIDLE| documentation is written using the reStructuredText markup language
(.rst file extension) with Sphinx extensions and processed using Sphinx. API
documentation is included from Doxygen comments.

See :ref:`zephyr:documentation-overview` in the Zephyr :ref:`zephyr:zephyr_doc`
developer guide for information about reStructuredText.

Before you start
****************

Before you can build the documentation, install |BRIDLE| as described in
:ref:`gs_installing`. Make sure that you have installed the required
:ref:`Python dependencies <additional_deps>`. See
:ref:`zephyr:documentation-processors` in the Zephyr :ref:`zephyr:zephyr_doc`
developer guide for information about installing the required tools to build
the documentation and their supported versions.

The following tool versions have been tested to work:

* Doxygen |doxygen_min_ver|
* MscGen |mscgen_min_ver|
* Python dependencies as listed in :ref:`python_req_documentation`

Complete the following steps to install the required tools:

1. If you have not done so already, install the |BRIDLE| as described in
   :ref:`gs_installing`.
#. Install or update all required :ref:`Python dependencies <additional_deps>`.
#. Install `Doxygen`_.
#. Install `mscgen`_ and make sure that the :file:`mscgen` executable is in your
   :file:`PATH`.

.. note::

   On Windows, the Sphinx executable ``sphinx-build.exe`` is placed in the
   ``Scripts`` folder of your Python installation path. Dependending on how
   you have installed Python, you may need to add this folder to your ``PATH``
   environment variable. Follow the instructions in `Windows Python Path`_
   to add those if needed.

.. _Windows Python Path:
   https://docs.python.org/3/using/windows.html#finding-the-python-executable

.. _documentation_sets:

Documentation structure
***********************

All documentation build files are located in the :file:`workspace/bridle/doc`
folder. The :file:`bridle` subfolder in that directory contains all .rst source
files that are not directly related to a sample application or a library.
Documentation for samples and libraries are provided in a :file:`README.rst` or
:file:`*.rst` file in the same directory as the code.

Building the documentation output requires building the output for all
documentation sets. Following are the available documentation sets:

:bridle: |BRIDLE|
:zephyr: Zephyr RTOS
:kconfig: All available Kconfig References in the Zephyr RTOS and |BRIDLE|
:devicetree: All available DTS Bindings in the Zephyr RTOS and |BRIDLE|

Since there are links from the |BRIDLE| documentation set into other
documentation sets, the other documentation sets built in a predefined order.

Building documentation output
*****************************

There are two different methods available, a quick way via :command:`west` and
a way with direct calls to the necessary configuration and build tools.

:use west:

   .. code-block:: console

      west build --cmake-only -b none -d build/bridle-doc bridle/doc
      west build -t build-all -b none -d build/bridle-doc

:direct calls:

   Complete the following steps to build the documentation output:

   #. Load the environment setting for Zephyr builds.

      * On Windows:

        .. code-block:: console

           zephyr\zephyr-env.cmd

      * On Linux or macOS:

        .. code-block:: console

           source zephyr/zephyr-env.sh

   #. Generate the Ninja build files and build the complete |BRIDLE| (3rd)
      documentation:

      .. zephyr-app-commands::
         :app: bridle/doc
         :build-dir: bridle-doc
         :goals: build-all
         :host-os: unix
         :tool: cmake
         :generator: ninja
         :compact:

This command will build all documentation sets and can take up to 20 minutes.

Alternatively, if you want to build each documentation set separately,
complete the following steps. Generate the Ninja build files and build
the Kconfig Reference and Devicetree Bindings (1st), Zephyr (2nd), and
|BRIDLE| (3rd) documentation:

:use west:

   .. code-block:: console

      # Use west to configure a Ninja-based buildsystem with cmake:
      west build --cmake-only -b none -d build/bridle-doc bridle/doc

      # Now run west on the generated build system:
      west build -t kconfig -b none -d build/bridle-doc
      west build -t devicetree -b none -d build/bridle-doc
      west build -t zephyr -b none -d build/bridle-doc
      west build -t bridle -b none -d build/bridle-doc

:direct calls:

   .. zephyr-app-commands::
      :app: bridle/doc
      :build-dir: bridle-doc
      :goals: kconfig devicetree zephyr bridle
      :host-os: unix
      :tool: cmake
      :generator: ninja

   It is important to keep the order of build targets!

The documentation output is written to :file:`build/bridle-doc/html`.
Double-click the :file:`index.html` file to display the documentation
in your browser or type in:

.. code-block:: console

   firefox build/bridle-doc/html/index.html &

.. tip::

   If you modify or add RST files, you only need to rerun the steps that
   build the respective documentation: 2nd target in step 3 if you modified
   the Zephyr documentation, 3rd target in step 3 if you modified |BRIDLE|
   documentation.

   If you open up a new command prompt, you must repeat step 2
   or complete step 3.

Serve documentation locally
***************************

Allow running from localhost; local build can be served with Python
HTTP server module:

.. code-block:: console

   python -m http.server -b localhost -d build/bridle-doc/html 4711 &

Now you can browse locally with:

.. code-block:: console

   firefox http://localhost:4711/index.html &

.. _caching_and_cleaning:

Caching and cleaning
********************

To speed up the documentation build, Sphinx processes only those files that
have been changed since the last build. In addition, RST files are copied
to a different location during the build process. This mechanism can cause
outdated or deleted files to be used in the build, or the navigation to not
be updated as expected.

If you experience any such problems, clean the build folders before you run
the documentation build. Note that this will cause the documentation to be
built from scratch, which takes a considerable time.

To clean the build folders for the Kconfig Reference:

:use west:

   .. code-block:: console

      west build -t kconfig-clean -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc kconfig-clean

To clean the build folders for the Devicetree Bindings:

:use west:

   .. code-block:: console

      west build -t devicetree-clean -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc devicetree-clean

To clean the build folders for the Zephyr RTOS documentation:

:use west:

   .. code-block:: console

      west build -t zephyr-clean -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc zephyr-clean

To clean the build folders for |BRIDLE| documentation:

:use west:

   .. code-block:: console

      west build -t bridle-clean -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc bridle-clean

To clean all the documentation sets build files:

:use west:

   .. code-block:: console

      west build -t clean -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc clean

If you want to build the documentation from scratch just delete the contents
of the build folder and run :command:`cmake` and then :command:`ninja` again:

:direct calls:

   .. code-block:: console

      rm -rf build/bridle-doc

Different versions
******************

Documentation sets for different versions of the |BRIDLE| are defined in the
:file:`doc/versions.json` file. This file is used to display the version
drop-down in the top-left corner of the documentation.

The version drop-down is displayed only if the documentation files are
organized in the required folder structure and the documentation is hosted
on a web server. To test the version drop-down locally, complete the
following steps:

1. In the documentation build folder (for example, :file:`build/bridle-doc`),
   rename the :file:`html` folder to :file:`latest`.
#. Open a command window in the documentation build folder and enter the
   following command to start a Python web server:

   .. code-block:: console

      python -m http.server

   Alternative set the documentation build folder as document root:

   .. code-block:: console

      python -m http.server -d build/bridle-doc

#. Access http://localhost:8000/latest/index.html with your browser to see
   the documentation.

To add other versions of the documentation to your local documentation output,
build the versions from a tagged release and rename the :file:`html` folder to
the respective version (for example, |release_number_tt|).

Dealing with warnings
*********************

When building the documentation, all warnings are regarded as errors, so they
will make the documentation build fail.

However, there are some known issues with Sphinx and Breathe that generate
Sphinx warnings even though the input is valid C code. To deal with such
unavoidable warnings, Zephyr provides the Sphinx extension
:file:`zephyr.warnings_filter` that filters out warnings based on a set of
regular expressions. You can find the extension together with usage details
at :file:`workspace/zephyr/doc/_extensions/zephyr/warnings_filter.py`.

The configuration file that defines the expected warnings for the |BRIDLE|
documentation set is located at :file:`workspace/doc/bridle/known-warnings.txt`.
It contains regular expressions to filter out warnings related to duplicate
C declarations. These warnings are caused by different objects (for example,
a struct and a function or nested elements) sharing the same name.
