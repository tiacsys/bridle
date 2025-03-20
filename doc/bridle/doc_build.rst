.. _doc_build:

Building |BRIDLE| documentation
###############################

.. contents::
   :local:
   :depth: 2

The |BRIDLE| documentation is written using the reStructuredText markup language
(.rst file extension) with Sphinx extensions and processed using Sphinx. API
documentation is included from Doxygen comments.

See :zephyr:ref:`documentation-overview` in the Zephyr :zephyr:ref:`zephyr_doc`
developer guide for information about reStructuredText.

Before you start
****************

Before you can build the documentation, install |BRIDLE| as described in
:ref:`gs_installing`. Make sure that you have installed the required
:ref:`Python dependencies <additional_deps>`. See
:zephyr:ref:`documentation-processors` in the Zephyr :zephyr:ref:`zephyr_doc`
developer guide for information about installing the required tools to build
the documentation and their supported versions.

The following tool versions have been tested to work:

.. list-table::
   :header-rows: 1

   * - Tool
     - Min. Version
   * - |Sphinx|_
     - |Sphinx_ver|
       (see :ref:`Python dependencies <python_req_documentation>`)
   * - |doxygen|_
     - |doxygen_min_ver|
   * - |graphviz|_
     - |graphviz_min_ver|
   * - |mscgen|_
     - |mscgen_min_ver|

Complete the following steps to install the required tools:

1. If you have not done so already, install |BRIDLE| as described in
   :ref:`gs_installing`.
#. Install or update all required :ref:`Python dependencies <additional_deps>`.
#. The installation process of all other tools is different depending on your
   operating system.

   .. tabs::

      .. group-tab:: Linux

         .. _install_dependencies_linux:

         To install the required tools on Linux, complete the following steps:

         .. tsn-include:: contribute/documentation/generation.rst
            :docset: zephyr
            :dedent: 6
            :start-after: .. group-tab:: Linux
            :end-before: .. group-tab:: macOS

         To upgrade and install additional required tools on Ubuntu, complete
         the following steps:

         #. If using an Ubuntu version older than 24.04, it is necessary to
            add extra repositories to meet the minimum required versions for
            the main dependencies listed above. In that case inspect, evaluate
            and then apply the `TiaC Systems Doxygen PPA`_ from Canonical
            Launchpad:

            .. code-block:: bash

               sudo add-apt-repository ppa:tiac-systems/doxygen
               sudo apt update

         #. Use ``apt`` to install additional required dependencies:

            .. code-block:: bash

               sudo apt install --no-install-recommends doxygen graphviz mscgen

         #. Verify the versions of the main dependencies installed on your
            system by entering:

            .. code-block:: bash

               sphinx-build --version
               doxygen --version
               dot -V
               mscgen -V

            Check those against the versions in the table in the beginning
            of this section.

      .. group-tab:: macOS

         .. _install_dependencies_macos:

         To install the required tools on macOS, complete the following steps:

         .. tsn-include:: contribute/documentation/generation.rst
            :docset: zephyr
            :dedent: 6
            :start-after: .. group-tab:: macOS
            :end-before: .. group-tab:: Windows

         Use ``brew`` to install the additional tool ``mscgen``:

         .. code-block:: console

            brew install mscgen

      .. group-tab:: Windows

         .. _install_dependencies_windows:

         To install the required tools on Windows, complete the following steps:

         .. tsn-include:: contribute/documentation/generation.rst
            :docset: zephyr
            :dedent: 6
            :start-after: .. group-tab:: Windows
            :end-before: .. doc_processors_installation_end

         Download, inspect (MD5: a04b258bb459f894ed8ec2c7896fa346) and execute
         Michael McTernan's Windows installer for ``mscgen`` from:
         https://www.mcternan.me.uk/mscgen/software/mscgen_0.20.exe

.. _doc_build_steps:

Building documentation output
*****************************

There are two different methods available, a quick way via :command:`west` and
a way with direct calls to the necessary configuration and build tools.

:use west:

   .. zephyr-app-commands::
      :app: bridle/doc
      :build-dir: bridle-doc
      :goals: zephyr-doxygen bridle-doxygen build-all
      :west-args: --cmake-only
      :generator: ninja
      :tool: west
      :host-os: all
      :compact:

:direct calls:

   Complete the following steps to build the documentation output:

   #. Load the environment setting for Zephyr builds.

      * On Linux or macOS:

        .. code-block:: console

           source zephyr/zephyr-env.sh

      * On Windows:

        .. code-block:: console

           zephyr\zephyr-env.cmd

   #. Generate the Ninja build files and build the complete |BRIDLE| (3rd)
      documentation:

      .. zephyr-app-commands::
         :app: bridle/doc
         :build-dir: bridle-doc
         :goals: zephyr-doxygen bridle-doxygen build-all
         :generator: ninja
         :tool: cmake
         :host-os: all
         :compact:

This command will build all documentation sets and can take up to 20 minutes.

Alternatively, if you want to build each documentation set separately,
complete the following steps. Generate the Ninja build files and build
the Kconfig Reference and Devicetree Bindings (1st), Zephyr (2nd), and
|BRIDLE| (3rd) documentation:

:use west:

   .. zephyr-app-commands::
      :app: bridle/doc
      :build-dir: bridle-doc
      :goals: kconfig devicetree zephyr-doxygen zephyr bridle-doxygen bridle
      :west-args: --cmake-only
      :generator: ninja
      :tool: west
      :host-os: all

:direct calls:

   .. zephyr-app-commands::
      :app: bridle/doc
      :build-dir: bridle-doc
      :goals: kconfig devicetree zephyr-doxygen zephyr bridle-doxygen bridle
      :generator: ninja
      :tool: cmake
      :host-os: all

   It is important to keep the order of build targets!

The documentation output is written to :file:`build/bridle-doc/html` or
:file:`build/bridle-doc/doxygen/*/html` in case of the standalone API
documentation of Zephyr and Bride.

.. tabs::

   .. group-tab:: Linux

      Double-click the :file:`index.html` file to display the documentation
      in your default browser or type in:

         .. code-block:: console

            xdg-open build/bridle-doc/html/index.html
            xdg-open build/bridle-doc/doxygen/zephyr/html/index.html
            xdg-open build/bridle-doc/doxygen/bridle/html/index.html

   .. group-tab:: macOS

      Double-click the :file:`index.html` file to display the documentation
      in your default browser or type in:

         .. code-block:: console

            open build/bridle-doc/html/index.html
            open build/bridle-doc/doxygen/zephyr/html/index.html
            open build/bridle-doc/doxygen/bridle/html/index.html

   .. group-tab:: Windows

      Double-click the :file:`index.html` file to display the documentation
      in your default browser or type in:

         .. code-block:: console

            start build\bridle-doc\html\index.html
            start build\bridle-doc\doxygen\zephyr\html\index.html
            start build\bridle-doc\doxygen\bridle\html\index.html

.. tip::

   If you modify or add RST files, you only need to rerun the steps that
   build the respective documentation: 2nd target in step 3 if you modified
   the Zephyr documentation, 3rd target in step 3 if you modified |BRIDLE|
   documentation.

   If you open up a new command prompt, you must repeat step 2
   or complete step 3.

Serve documentation locally
***************************

Allow running from :bbl:`localhost` at port :bgn:`4711`; local build can be
served with `Python HTTP server`_ module:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      |python_bin| -m http.server -b :bbl:`localhost` -d build/bridle-doc/html :bgn:`4711` &

.. tabs::

   .. group-tab:: Linux

      Now you can browse locally with:

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               xdg-open http\:\/\/:bbl:`localhost`::bgn:`4711`/index.html &

   .. group-tab:: macOS

      Now you can browse locally with:

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               open http\:\/\/:bbl:`localhost`::bgn:`4711`/index.html &

   .. group-tab:: Windows

      Now you can browse locally with:

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               start http\:\/\/:bbl:`localhost`::bgn:`4711`/index.html &

Developer-mode Document Building
********************************

When making and testing major changes to the documentation, we provide an option
to temporarily stub-out the auto-generated Devicetree bindings documentation so
the doc build process runs faster.

To enable this mode, set the following option when invoking :command:`cmake`:

   .. code-block:: console

      -DDT_TURBO_MODE=1

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

      west build -t kconfig-clean -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -Cbuild/bridle-doc kconfig-clean

To clean the build folders for the Devicetree Bindings:

:use west:

   .. code-block:: console

      west build -t devicetree-clean -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -Cbuild/bridle-doc devicetree-clean

To clean the build folders for the Zephyr RTOS documentation:

:use west:

   .. code-block:: console

      west build -t zephyr-clean -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -Cbuild/bridle-doc zephyr-clean

To clean the build folders for |BRIDLE| documentation:

:use west:

   .. code-block:: console

      west build -t bridle-clean -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -Cbuild/bridle-doc bridle-clean

To clean all the documentation sets build files:

:use west:

   .. code-block:: console

      west build -t clean -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -Cbuild/bridle-doc clean

If you want to build the documentation from scratch just delete the contents
of the build folder and run :command:`cmake` and then :command:`ninja` again:

:direct calls:

   .. code-block:: console

      rm -rf build/bridle-doc

.. _testing_versions:

Testing different versions locally
**********************************

Documentation sets for different versions of the |BRIDLE| are defined in the
:file:`doc/versions.json` file. This file is used to display the version
drop-down in the top-left corner of the documentation.

The version drop-down is displayed only if the documentation files are
organized in the required folder structure and the documentation is hosted
on a web server. To test the version drop-down locally, complete the
following steps:

1. In the documentation build folder (for example, :file:`build/bridle-doc`),
   :ubl:`rename` the :file:`html` folder to :file:`latest`.
#. Open a command window :ubl:`inside the documentation build folder` and
   enter the following command to start a `Python HTTP server`_:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         |python_bin| -m http.server &

   Alternative set the documentation build folder as document root:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         |python_bin| -m http.server -d build/bridle-doc &

#. Access http://localhost:8000/latest/index.html with your browser to see
   the documentation.

To add other versions of the documentation to your local documentation output,
build the versions from a tagged release and rename the :file:`html` folder to
the respective version (for example, |release_number_tt|).

Dealing with warnings
*********************

When building the documentation, all warnings are regarded as errors, so they
will make the documentation build fail.

However, there are some expected warnings when creating the Sphinx inventory
file for each documentation set and also known issues with Sphinx and Breathe
that generate Sphinx warnings even though the input is valid C code. To deal
with such unavoidable warnings, Bridle provides the Sphinx extension
:file:`bridle.warnings_filter` that filters out warnings based on a set of
regular expressions. You can find the extension together with usage details
at :file:`workspace/bridle/doc/_extensions/bridle/warnings_filter.py`.

The configuration file that defines the expected warnings for the |BRIDLE|
documentation set is located at :file:`workspace/doc/bridle/known-warnings.txt`
and  :file:`workspace/doc/bridle/known-warnings-inventory.txt`. It contains
regular expressions to filter out warnings related to duplicate C declarations
or missing (unknown) links to other Sphinx documentation sets (from other
Sphinx inventories).
