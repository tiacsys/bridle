.. _doc_build:

Building the |LPNB| documentation
#################################

The |LPNB| documentation is written using the reStructuredText markup language
(.rst file extension) with Sphinx extensions and processed using Sphinx. API
documentation is included from Doxygen comments.

See the *Documentation overview* section in the :ref:`zephyr:zephyr_doc`
developer guide for information about reStructuredText.

Before you start
****************

Before you can build the documentation, install the |LPNB| as described in
... t.b.d.

Before you can build the documentation, install the |LPNB| as described in
:ref:`gs_installing`. Make sure that you have installed the required
:ref:`Python dependencies <additional_deps>`.

See the *Installing the documentation processors* section in the
:ref:`zephyr:zephyr_doc` developer guide for information about installing the
required tools to build the documentation and their supported versions.

.. note::
   On Windows, the Sphinx executable ``sphinx-build.exe`` is placed in
   the ``Scripts`` folder of your Python installation path.
   Dependending on how you have installed Python, you may need to
   add this folder to your ``PATH`` environment variable. Follow
   the instructions in `Windows Python Path`_ to add those if needed.

Documentation structure
***********************

All documentation build files are located in the ``doc/lpnb`` folder. The
``lpnb`` subfolder in that directory contains all .rst source files that are
not directly related to a sample application or a library. Documentation for
samples and libraries are provided in a ``README.rst`` or ``*.rst`` file in
the same directory as the code.

Building the documentation output requires building output for all
documentation sets. Currently, there are two sets: lpnb, and zephyr. Since
there are links from the lpnb documentation set into other documentation
sets, the other documentation sets must be built first.

Building documentation output
*****************************

Complete the following steps to build the documentation output:

#. Load the environment setting for Zephyr builds.

   * On Windows:

        .. code-block:: console

           zephyr\zephyr-env.cmd

   * On Linux or macOS:

        .. code-block:: console

           source zephyr/zephyr-env.sh

#. Generate the Ninja build files and build the complete |LPNB| (3rd)
   documentation:

   .. zephyr-app-commands::
      :app: bridle/doc
      :build-dir: lpn-bridle-doc
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
   |LPNB| (3rd) documentation:

   .. zephyr-app-commands::
      :app: bridle/doc
      :build-dir: lpn-bridle-doc
      :goals: kconfig-html devicetree-html zephyr lpnb
      :host-os: unix
      :tool: cmake
      :generator: ninja

   It is important to keep the order of build targets!

The documentation output is written to ``build/lpn-bridle-doc/html``.
Double-click the ``index.html`` file to display the documentation in your
browser or type in:

.. code-block:: console

   firefox build/lpn-bridle-doc/html/index.html &

.. tip::
   If you modify or add RST files, you only need to rerun the steps that
   build the respective documentation: 2nd target in step 3 if you modified
   the Zephyr documentation, 3rd target in step 3 if you modified the |LPNB|
   documentation.

   If you open up a new command prompt, you must repeat step 2
   or complete step 3.

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

.. code-block:: console

   ninja -C build/lpn-bridle-doc clean-kconfig

To clean the build folders for the Devicetree bindings:

.. code-block:: console

   ninja -C build/lpn-bridle-doc clean-devicetree

To clean the build folders for the Zephyr documentation:

.. code-block:: console

   ninja -C build/lpn-bridle-doc clean-zephyr

To clean the build folders for the |LPNB| documentation:

.. code-block:: console

   ninja -C build/lpn-bridle-doc clean-lpnb

If you want to build the documentation from scratch just delete the contents
of the build folder and run ``cmake`` and then ``ninja`` again:

.. code-block:: console

   rm -rf build/lpn-bridle-doc

.. _Windows Python Path: https://docs.python.org/3/using/windows.html#finding-the-python-executable
