.. _gs_recommended_versions:

Requirements
############

.. contents::
   :local:
   :depth: 2

|BRIDLE| supports Linux for development and in theory macOS and Windows, but
these have not been tested yet.

.. _gs_supported_OS:

Supported operating systems
***************************

The following table shows the operating system versions that support
the |BRIDLE| development environment:

.. _req_os_table:

.. tabs::

   .. group-tab:: Linux

      .. list-table::
         :header-rows: 1

         * - Operating System
           - x86
           - x64
           - ARM
           - ARM64
           - PPC64LE
           - RISV64
           - S390X
         * - `Ubuntu 24.04 LTS`_
           - :rd:`Not applicable`
           - :bgn:`Tier 1`
           - Not supported
           - :byl:`Tier 3`
           - Not supported
           - Not supported
           - Not supported
         * - `Ubuntu 22.04 LTS`_
           - :rd:`Not applicable`
           - :bbl:`Tier 2`
           - Not supported
           - :byl:`Tier 3`
           - Not supported
           - Not supported
           - Not supported
         * - `Ubuntu 20.04 LTS`_
           - :rd:`Not applicable`
           - :bbl:`Tier 2`
           - Not supported
           - :bbl:`Tier 2`
           - Not supported
           - Not supported
           - Not supported

   .. group-tab:: macOS

      .. list-table::
         :header-rows: 1

         * - Operating System
           - x86
           - x64
           - ARM64
         * - `macOS 12`_
           - :rd:`Not applicable`
           - :byl:`Tier 3`
           - :byl:`Tier 3`
         * - `macOS 11`_
           - :rd:`Not applicable`
           - :byl:`Tier 3`
           - Not supported
         * - `macOS 10.15`_
           - :rd:`Not applicable`
           - :byl:`Tier 3`
           - Not supported

   .. group-tab:: Windows

      .. list-table::
         :header-rows: 1

         * - Operating System
           - x86
           - x64
           - ARM64
         * - `Windows 11`_
           - :byl:`Tier 3`
           - :byl:`Tier 3`
           - Not supported
         * - `Windows 10`_
           - :byl:`Tier 3`
           - :byl:`Tier 3`
           - Not supported

The table uses the following :bbk:`Tier #` definitions to categorize the level
of operating system support:

:bgn:`Tier 1`
   The |BRIDLE| development environment will always work. The automated build
   and automated testing ensure that the |BRIDLE| development environment build
   and successfully complete tests after each change.

:bbl:`Tier 2`
   The |BRIDLE| development environment will always build. The automated build
   ensures that the |BRIDLE| development environment build successfully after
   each change. There is no guarantee that a build will work because the
   automation tests do not always run.

:byl:`Tier 3`
   The |BRIDLE| development environment are supported by design but not built
   or tested after each change. Therefore, the application may or may not work.

Not supported
   The |BRIDLE| development environment do not work, but it may be supported
   in the future.

:rd:`Not applicable`
   The specified architecture is not supported for the respective operating
   system.

.. note::

   The |BRIDLE| development environment are not supported by the older
   versions of the operating system.

.. _gs_required_tools:

Required tools
**************

The following table shows the tools that are required for working with |BRIDLE|
|version|. It lists the minimum version that is required and the version that is
installed when using the :ref:`gs_app_sim` as described in :ref:`gs_assistant`.

.. _req_tools_table:

.. tabs::

   .. group-tab:: Linux

      .. list-table::
         :header-rows: 1

         * - Tool / Suggestion
           - Minimum version
           - Tested version
         * - | |Git|_
             | |git_linux|_
           - |
             |
           - |
             | |git_recommended_ver_linux|
         * - | |Python 3|_
             | |python_linux|_
           - | |python_min_ver|
             |
           - |
             | |python_recommended_ver_linux|
         * - |west_pypa|_
           - |west_min_ver|
           - |west_recommended_ver_linux|
         * - | |CMake|_
             | |cmake_linux|_
           - | |cmake_min_ver|
             |
           - |
             | |cmake_recommended_ver_linux|
         * - | |Ninja|_
             | |ninja_linux|_
           - | |ninja_min_ver|
             |
           - |
             | |ninja_recommended_ver_linux|
         * - | |Device tree compiler|_
             | |dtc_linux|_
           - | |dtc_min_ver|
             |
           - |
             | |dtc_recommended_ver_linux|
         * - | |OpenOCD|_
             | |openocd_linux|_
           - | |openocd_min_ver|
             |
           - |
             | |openocd_recommended_ver_linux|
         * - | |DFU Utilities|_
             | |dfu_linux|_
           - |
             |
           - |
             | |dfu_util_recommended_ver_linux|
         * - | |GNU gperf|_
             | |gperf_linux|_
           - | |gperf_min_ver|
             |
           - |
             | |gperf_recommended_ver_linux|
         * - **Tools for documentation**
           -
           -
         * - | |Doxygen|_
             | |doxygen_linux|_
           - | |doxygen_min_ver|
             |
           - |
             | |doxygen_recommended_ver_linux|
         * - | |Graphviz|_
             | |graphviz_linux|_
           - | |graphviz_min_ver|
             |
           - |
             | |graphviz_recommended_ver_linux|
         * - | |MscGen|_
             | |mscgen_linux|_
           - | |mscgen_min_ver|
             |
           - |
             | |mscgen_recommended_ver_linux|
         * - | |ccache|_
             | |ccache_linux|_
           - |
             |
           - |
             | |ccache_recommended_ver_linux|
         * - **SDK suites for development**
           -
           -
         * - |zephyrsdk|_
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_linux|
         * - |armgnutc|_
           - |armgnutc_min_ver|
           - |armgnutc_recommended_ver_linux|
         * - |gnuarmemb|_
           - |gnuarmemb_min_ver|
           - |gnuarmemb_recommended_ver_linux|
         * - |stm32cubeclt|_
           - |stm32cubeclt_min_ver|
           - |stm32cubeclt_recommended_ver_linux|
         * - |mcuxpressoide|_
           - |mcuxpressoide_min_ver|
           - |mcuxpressoide_recommended_ver_linux|

   .. group-tab:: macOS

      .. list-table::
         :header-rows: 1

         * - Tool / Suggestion
           - Minimum version
           - Tested version
         * - | |Git|_
             | |git_macos|_
           - |
             |
           - |
             | |git_recommended_ver_macos|
         * - | |Python 3|_
             | |python_macos|_
           - | |python_min_ver|
             |
           - |
             | |python_recommended_ver_macos|
         * - |west_pypa|_
           - |west_min_ver|
           - |west_recommended_ver_macos|
         * - | |CMake|_
             | |cmake_macos|_
           - | |cmake_min_ver|
             |
           - |
             | |cmake_recommended_ver_macos|
         * - | |Ninja|_
             | |ninja_macos|_
           - | |ninja_min_ver|
             |
           - |
             | |ninja_recommended_ver_macos|
         * - | |Device tree compiler|_
             | |dtc_macos|_
           - | |dtc_min_ver|
             |
           - |
             | |dtc_recommended_ver_macos|
         * - | |OpenOCD|_
             | |openocd_macos|_
           - | |openocd_min_ver|
             |
           - |
             | |openocd_recommended_ver_macos|
         * - | |DFU Utilities|_
             | |dfu_macos|_
           - |
             |
           - |
             | |dfu_util_recommended_ver_macos|
         * - | |GNU gperf|_
             | |gperf_macos|_
           - | |gperf_min_ver|
             |
           - |
             | |gperf_recommended_ver_macos|
         * - **Tools for documentation**
           -
           -
         * - | |Doxygen|_
             | |doxygen_macos|_
           - | |doxygen_min_ver|
             |
           - |
             | |doxygen_recommended_ver_macos|
         * - | |Graphviz|_
             | |graphviz_macos|_
           - | |graphviz_min_ver|
             |
           - |
             | |graphviz_recommended_ver_macos|
         * - | |MscGen|_
             | |mscgen_macos|_
           - | |mscgen_min_ver|
             |
           - |
             | |mscgen_recommended_ver_macos|
         * - **SDK suites for development**
           -
           -
         * - |zephyrsdk|_
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_macos|
         * - |armgnutc|_
           - |armgnutc_min_ver|
           - |armgnutc_recommended_ver_macos|
         * - |gnuarmemb|_
           - |gnuarmemb_min_ver|
           - |gnuarmemb_recommended_ver_macos|
         * - |stm32cubeclt|_
           - |stm32cubeclt_min_ver|
           - |stm32cubeclt_recommended_ver_macos|
         * - |mcuxpressoide|_
           - |mcuxpressoide_min_ver|
           - |mcuxpressoide_recommended_ver_macos|

   .. group-tab:: Windows

      .. list-table::
         :header-rows: 1

         * - Tool / Suggestion
           - Minimum version
           - Tested version
         * - | |Git|_
             | |git_win1x_winget|_
             | |git_win1x_choco|_
           - |
             |
             |
           - |
             | |git_recommended_ver_win1x|
             | |git_recommended_ver_win1x|
         * - | |Python 3|_
             | |python_win1x_winget|_
             | |python_win1x_choco|_
           - | |python_min_ver|
             |
             |
           - |
             | |python_recommended_ver_win1x|
             | |python_recommended_ver_win1x|
         * - |west_pypa|_
           - |west_min_ver|
           - |west_recommended_ver_win1x|
         * - | |CMake|_
             | |cmake_win1x_winget|_
             | |cmake_win1x_choco|_
           - | |cmake_min_ver|
             |
             |
           - |
             | |cmake_recommended_ver_win1x|
             | |cmake_recommended_ver_win1x|
         * - | |Ninja|_
             | |ninja_win1x_winget|_
             | |ninja_win1x_choco|_
           - | |ninja_min_ver|
             |
             |
           - |
             | |ninja_recommended_ver_win1x|
             | |ninja_recommended_ver_win1x|
         * - | |Device tree compiler|_
             | |dtc_win1x_winget|_
             | |dtc_win1x_choco|_
           - | |dtc_min_ver|
             |
             |
           - |
             | |dtc_winget_recommended_ver_win1x|
             | |dtc_choco_recommended_ver_win1x|
         * - | |OpenOCD|_
             | |openocd_win1x_xpack|_
             | |openocd_win1x_choco|_
           - | |openocd_min_ver|
             |
             |
           - |
             | |openocd_xpack_recommended_ver_win1x|
             | |openocd_choco_recommended_ver_win1x|
         * - | |DFU Utilities|_
             | |dfu_win1x_bintarxz|_
           - |
             |
           - |
             | |dfu_util_recommended_ver_win1x|
         * - | |GNU gperf|_
             | |gperf_win1x_winget|_
             | |gperf_win1x_choco|_
           - | |gperf_min_ver|
             |
             |
           - |
             | |gperf_recommended_ver_win1x|
             | |gperf_recommended_ver_win1x|
         * - **Tools for documentation**
           -
           -
         * - | |Doxygen|_
             | |doxygen_win1x_winget|_
             | |doxygen_win1x_choco|_
           - | |doxygen_min_ver|
             |
             |
           - |
             | |doxygen_recommended_ver_win1x|
             | |doxygen_recommended_ver_win1x|
         * - | |Graphviz|_
             | |graphviz_win1x_winget|_
             | |graphviz_win1x_choco|_
           - | |graphviz_min_ver|
             |
             |
           - |
             | |graphviz_recommended_ver_win1x|
             | |graphviz_recommended_ver_win1x|
         * - | |MscGen|_
             | |mscgen_win1x|_
           - | |mscgen_min_ver|
             |
           - |
             | |mscgen_recommended_ver_win1x|
         * - **SDK suites for development**
           -
           -
         * - |zephyrsdk|_
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_win1x|
         * - |armgnutc|_
           - |armgnutc_min_ver|
           - |armgnutc_recommended_ver_win1x|
         * - |gnuarmemb|_
           - |gnuarmemb_min_ver|
           - |gnuarmemb_recommended_ver_win1x|
         * - |stm32cubeclt|_
           - |stm32cubeclt_min_ver|
           - |stm32cubeclt_recommended_ver_win1x|
         * - |mcuxpressoide|_
           - |mcuxpressoide_min_ver|
           - |mcuxpressoide_recommended_ver_win1x|

.. _gs_required_python_packages:

Required Python dependencies
****************************

The following table shows the Python packages that are required for working
with |BRIDLE| |version|. If no version is specified, the default version
provided with :command:`pip` is recommended. If a version is specified, it
is important that the installed version matches the required version. See
:ref:`additional_deps` for instructions on how to install the Python
dependencies.

.. _python_req_development:

Building and running applications, samples, and tests
=====================================================

.. _req_devpkgs_table:

.. zephyr-keep-sorted-start re(^\s+\* - \|\w)

.. list-table::
   :header-rows: 1

   * - Package
     - Version
   * - |PyYAML|_
     - |PyYAML_ver|
   * - |ecdsa|_
     - |ecdsa_ver|
   * - |intelhex|_
     - |intelhex_ver|
   * - |pyelftools|_
     - |pyelftools_ver|
   * - |pykitinfo|_
     - |pykitinfo_ver|
   * - |pylint|_
     - |pylint_ver|
   * - |pymcuprog|_
     - |pymcuprog_ver|
   * - |pyocd|_
     - |pyocd_ver|
   * - |pyserial|_
     - |pyserial_ver|
   * - |pytest|_
     - |pytest_ver|
   * - |regex|_
     - |regex_ver|
   * - |west|_
     - |west_ver|
   * - |windows-curses|_ (only Windows)
     - |windows-curses_ver|

.. zephyr-keep-sorted-stop

.. _python_req_documentation:

Building documentation
======================

.. _req_docpkgs_table:

.. zephyr-keep-sorted-start re(^\s+\* - \|\w)

.. list-table::
   :header-rows: 1

   * - Package
     - Version
   * - |Pillow|_
     - |Pillow_ver|
   * - |Pygments|_
     - |Pygments_ver|
   * - |Sphinx|_
     - |Sphinx_ver|
   * - |docutils|_
     - |docutils_ver|
   * - |doxmlparser|_
     - |doxmlparser_ver|
   * - |imagesize|_
     - |imagesize_ver|
   * - |sphinx-autobuild|_
     - |sphinx-autobuild_ver|
   * - |sphinx-copybutton|_
     - |sphinx-copybutton_ver|
   * - |sphinx-csv-filter|_
     - |sphinx-csv-filter_ver|
   * - |sphinx-notfound-page|_
     - |sphinx-notfound-page_ver|
   * - |sphinx-sitemap|_
     - |sphinx-sitemap_ver|
   * - |sphinx-tabs|_
     - |sphinx-tabs_ver|
   * - |sphinx-togglebutton|_
     - |sphinx-togglebutton_ver|
   * - |sphinx_tsn_theme|_
     - |sphinx_tsn_theme_ver|
   * - |sphinxcontrib-mscgen|_
     - |sphinxcontrib-mscgen_ver|
   * - |sphinxcontrib-programoutput|_
     - |sphinxcontrib-programoutput_ver|
   * - |sphinxcontrib-svg2pdfconverter|_
     - |sphinxcontrib-svg2pdfconverter_ver|

.. zephyr-keep-sorted-stop
