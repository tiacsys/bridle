.. _gs_recommended_versions:

Required tools
##############

.. contents::
   :local:
   :depth: 2

The following table shows the tools that are required for working with |BRIDLE|
v\ |version|. It lists the minimum version that is required and the version
that is installed when using the :ref:`gs_app_sim` as described in
:ref:`gs_assistant`.

.. tabs::

   .. group-tab:: Windows

      .. list-table::
         :header-rows: 1

         * - Tool
           - Minimum version
           - Tested version
         * - CMake
           - |cmake_min_ver|
           - |cmake_recommended_ver_win10|
         * - device-tree-compiler
           - |dtc_min_ver|
           - |dtc_recommended_ver_win10|
         * - openocd
           - |openocd_min_ver|
           - |openocd_recommended_ver_win10|
         * - git
           -
           - |git_recommended_ver_win10|
         * - gperf
           - |gperf_min_ver|
           - |gperf_recommended_ver_win10|
         * - ninja
           - |ninja_min_ver|
           - |ninja_recommended_ver_win10|
         * - Python
           - |python_min_ver|
           - |python_recommended_ver_win10|
         * - west
           - |west_min_ver|
           - |west_recommended_ver_win10|
         * - Zephyr SDK
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_win10|
         * - Doxygen
           - |doxygen_min_ver|
           -
         * - MscGen
           - |mscgen_min_ver|
           -

   .. group-tab:: Linux

      .. list-table::
         :header-rows: 1

         * - Tool
           - Minimum version
           - Tested version
         * - ccache
           -
           - |ccache_recommended_ver_linux|
         * - CMake
           - |cmake_min_ver|
           - |cmake_recommended_ver_linux|
         * - dfu-util
           -
           - |dfu_util_recommended_ver_linux|
         * - device-tree-compiler
           - |dtc_min_ver|
           - |dtc_recommended_ver_linux|
         * - openocd
           - |openocd_min_ver|
           - |openocd_recommended_ver_linux|
         * - git
           -
           - |git_recommended_ver_linux|
         * - gperf
           - |gperf_min_ver|
           - |gperf_recommended_ver_linux|
         * - ninja
           - |ninja_min_ver|
           - |ninja_recommended_ver_linux|
         * - Python
           - |python_min_ver|
           - |python_recommended_ver_linux|
         * - west
           - |west_min_ver|
           - |west_recommended_ver_linux|
         * - Zephyr SDK
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_linux|
         * - Doxygen
           - |doxygen_min_ver|
           -
         * - MscGen
           - |mscgen_min_ver|
           -

   .. group-tab:: macOS

      .. list-table::
         :header-rows: 1

         * - Tool
           - Minimum version
           - Tested version
         * - CMake
           - |cmake_min_ver|
           - |cmake_recommended_ver_darwin|
         * - device-tree-compiler
           - |dtc_min_ver|
           - |dtc_recommended_ver_darwin|
         * - openocd
           - |openocd_min_ver|
           - |openocd_recommended_ver_darwin|
         * - git
           -
           - |git_recommended_ver_darwin|
         * - gperf
           - |gperf_min_ver|
           - |gperf_recommended_ver_darwin|
         * - ninja
           - |ninja_min_ver|
           - |ninja_recommended_ver_darwin|
         * - Python
           - |python_min_ver|
           - |python_recommended_ver_darwin|
         * - west
           - |west_min_ver|
           - |west_recommended_ver_darwin|
         * - Zephyr SDK
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_darwin|
         * - Doxygen
           - |doxygen_min_ver|
           -
         * - MscGen
           - |mscgen_min_ver|
           -

Required Python dependencies
****************************

The following table shows the Python packages that are required for working with
|BRIDLE| v\ |version|. If no version is specified, the default version provided
with pip is recommended. If a version is specified, it is important that the
installed version matches the required version. See :ref:`additional_deps` for
instructions on how to install the Python dependencies.

Building and running applications, samples, and tests
=====================================================

.. list-table::
   :header-rows: 1

   * - Package
     - Version
   * - ecdsa
     - |ecdsa_ver|
   * - imagesize
     - |imagesize_ver|
   * - intelhex
     - |intelhex_ver|
   * - pyelftools
     - |pyelftools_ver|
   * - pylint
     - |pylint_ver|
   * - PyYAML
     - |PyYAML_ver|
   * - west
     - |west_ver|
   * - windows-curses (only Windows)
     - |windows-curses_ver|

.. _python_req_documentation:

Building documentation
======================

.. list-table::
   :header-rows: 1

   * - Package
     - Version
   * - docutils
     - |docutils_ver|
   * - breathe
     - |breathe_ver|
   * - Pygments
     - |Pygments_ver|
   * - CommonMark
     - |CommonMark_ver|
   * - recommonmark
     - |recommonmark_ver|
   * - sphinx
     - |sphinx_ver|
   * - sphinx_rtd_theme
     - |sphinx_rtd_theme_ver|
   * - sphinxcontrib-svg2pdfconverter
     - |sphinxcontrib-svg2pdfconverter_ver|
   * - sphinxcontrib-mscgen
     - |sphinxcontrib-mscgen_ver|
   * - sphinx-tabs
     - |sphinx-tabs_ver|
   * - sphinx-csv-filter
     - |sphinx-csv-filter_ver|
