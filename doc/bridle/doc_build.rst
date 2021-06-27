.. _doc_build:

Building |BRIDLE| documentation
###############################

The |BRIDLE| documentation is written using the reStructuredText markup language
(.rst file extension) with Sphinx extensions and processed using Sphinx. API
documentation is included from Doxygen comments.

See the *Documentation overview* section in the :ref:`zephyr:zephyr_doc`
developer guide for information about reStructuredText.

Before you start
****************

Before you can build the documentation, install |BRIDLE| as described in
:ref:`gs_installing`. Make sure that you have installed the required
:ref:`Python dependencies <additional_deps>`.

See the *Installing the documentation processors* section in the
:ref:`zephyr:zephyr_doc` developer guide for information about installing the
required tools to build the documentation and their supported versions.

.. note::

   On Windows, the Sphinx executable ``sphinx-build.exe`` is placed in the
   ``Scripts`` folder of your Python installation path. Dependending on how
   you have installed Python, you may need to add this folder to your ``PATH``
   environment variable. Follow the instructions in `Windows Python Path`_
   to add those if needed.

Documentation structure
***********************

All documentation build files are located in the ``doc/bridle`` folder. The
``bridle`` subfolder in that directory contains all .rst source files that are
not directly related to a sample application or a library. Documentation for
samples and libraries are provided in a ``README.rst`` or ``*.rst`` file in
the same directory as the code.

Building the documentation output requires building output for all
documentation sets. Currently, there are two sets: bridle, and zephyr. Since
there are links from the bridle documentation set into other documentation
sets, the other documentation sets must be built first.

Building documentation output
*****************************

There are two different methods available, a quick way via ``west`` and
a way with direct calls to the necessary configuration and build tools.

.. rubric:: use ``west``

.. code-block:: console

   west build --cmake-only -b none -d build/bridle-doc bridle/doc
   west build -t build-all -b none -d build/bridle-doc

.. rubric:: direct calls

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

   This command will build all documentation sets and can take
   up to 20 minutes.

Alternatively, if you want to build each documentation set separately,
complete the following steps. Generate the Ninja build files and build
the Kconfig Reference and Devicetree Bindings (1st), Zephyr (2nd), and
|BRIDLE| (3rd) documentation:

:use ``west``:

   .. code-block:: console

      # Use west to configure a Ninja-based buildsystem with cmake:
      west build --cmake-only -b none -d build/bridle-doc bridle/doc

      # Now run west on the generated build system:
      west build -t kconfig-html -b none -d build/bridle-doc
      west build -t devicetree-html -b none -d build/bridle-doc
      west build -t zephyr -b none -d build/bridle-doc
      west build -t bridle -b none -d build/bridle-doc

:direct calls:

   .. zephyr-app-commands::
      :app: bridle/doc
      :build-dir: bridle-doc
      :goals: kconfig-html devicetree-html zephyr bridle
      :host-os: unix
      :tool: cmake
      :generator: ninja

   It is important to keep the order of build targets!

The documentation output is written to ``build/bridle-doc/html``.
Double-click the ``index.html`` file to display the documentation in your
browser or type in:

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

To clean the build folders for the Kconfig references:

:use ``west``:

   .. code-block:: console

      west build -t clean-kconfig -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc clean-kconfig

To clean the build folders for the Devicetree bindings:

:use ``west``:

   .. code-block:: console

      west build -t clean-devicetree -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc clean-devicetree

To clean the build folders for the Zephyr documentation:

:use ``west``:

   .. code-block:: console

      west build -t clean-zephyr -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc clean-zephyr

To clean the build folders for |BRIDLE| documentation:

:use ``west``:

   .. code-block:: console

      west build -t clean-bridle -b none -d build/bridle-doc

:direct calls:

   .. code-block:: console

      ninja -C build/bridle-doc clean-bridle

If you want to build the documentation from scratch just delete the contents
of the build folder and run ``cmake`` and then ``ninja`` again:

:direct calls:

   .. code-block:: console

      rm -rf build/bridle-doc

.. _Windows Python Path: https://docs.python.org/3/using/windows.html#finding-the-python-executable
