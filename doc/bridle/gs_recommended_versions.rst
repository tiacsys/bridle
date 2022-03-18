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
         * - |cmake|_
           - |cmake_min_ver|
           - |cmake_recommended_ver_win10|
         * - |dtc_win10|_
           - |dtc_min_ver|
           - |dtc_recommended_ver_win10|
         * - |openocd|_
           - |openocd_min_ver|
           - |openocd_recommended_ver_win10|
         * - |git|_
           -
           - |git_recommended_ver_win10|
         * - |gperf|_
           - |gperf_min_ver|
           - |gperf_recommended_ver_win10|
         * - |ninja|_
           - |ninja_min_ver|
           - |ninja_recommended_ver_win10|
         * - |python|_
           - |python_min_ver|
           - |python_recommended_ver_win10|
         * - |west|_
           - |west_min_ver|
           - |west_recommended_ver_win10|
         * - |zephyrsdk|_
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_win10|
         * - |gnuarmemb|_
           - |gnuarmemb_min_ver|
           -
         * - |doxygen|_
           - |doxygen_min_ver|
           -
         * - |graphviz|_
           - |graphviz_min_ver|
           -
         * - |mscgen|_
           - |mscgen_min_ver|
           -

   .. group-tab:: Linux

      .. list-table::
         :header-rows: 1

         * - Tool
           - Minimum version
           - Tested version
         * - |ccache|_
           -
           - |ccache_recommended_ver_linux|
         * - |cmake|_
           - |cmake_min_ver|
           - |cmake_recommended_ver_linux|
         * - |dfu_util|_
           -
           - |dfu_util_recommended_ver_linux|
         * - |dtc_linux|_
           - |dtc_min_ver|
           - |dtc_recommended_ver_linux|
         * - |openocd|_
           - |openocd_min_ver|
           - |openocd_recommended_ver_linux|
         * - |git|_
           -
           - |git_recommended_ver_linux|
         * - |gperf|_
           - |gperf_min_ver|
           - |gperf_recommended_ver_linux|
         * - |ninja|_
           - |ninja_min_ver|
           - |ninja_recommended_ver_linux|
         * - |python|_
           - |python_min_ver|
           - |python_recommended_ver_linux|
         * - |west|_
           - |west_min_ver|
           - |west_recommended_ver_linux|
         * - |zephyrsdk|_
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_linux|
         * - |gnuarmemb|_
           - |gnuarmemb_min_ver|
           -
         * - |doxygen|_
           - |doxygen_min_ver|
           - |doxygen_recommended_ver_linux|
         * - |graphviz|_
           - |graphviz_min_ver|
           - |graphviz_recommended_ver_linux|
         * - |mscgen|_
           - |mscgen_min_ver|
           - |mscgen_recommended_ver_linux|

   .. group-tab:: macOS

      .. list-table::
         :header-rows: 1

         * - Tool
           - Minimum version
           - Tested version
         * - |cmake|_
           - |cmake_min_ver|
           - |cmake_recommended_ver_macos|
         * - |dtc_macos|_
           - |dtc_min_ver|
           - |dtc_recommended_ver_macos|
         * - |openocd|_
           - |openocd_min_ver|
           - |openocd_recommended_ver_macos|
         * - |git|_
           -
           - |git_recommended_ver_macos|
         * - |gperf|_
           - |gperf_min_ver|
           - |gperf_recommended_ver_macos|
         * - |ninja|_
           - |ninja_min_ver|
           - |ninja_recommended_ver_macos|
         * - |python|_
           - |python_min_ver|
           - |python_recommended_ver_macos|
         * - |west|_
           - |west_min_ver|
           - |west_recommended_ver_macos|
         * - |zephyrsdk|_
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_macos|
         * - |gnuarmemb|_
           - |gnuarmemb_min_ver|
           -
         * - |doxygen|_
           - |doxygen_min_ver|
           -
         * - |graphviz|_
           - |graphviz_min_ver|
           -
         * - |mscgen|_
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
   * - |ecdsa|_
     - |ecdsa_ver|
   * - |imagesize|_
     - |imagesize_ver|
   * - |intelhex|_
     - |intelhex_ver|
   * - |pyelftools|_
     - |pyelftools_ver|
   * - |pylint|_
     - |pylint_ver|
   * - |PyYAML|_
     - |PyYAML_ver|
   * - |west|_
     - |west_ver|
   * - |windows-curses|_ (only Windows)
     - |windows-curses_ver|

.. _python_req_documentation:

Building documentation
======================

.. list-table::
   :header-rows: 1

   * - Package
     - Version
   * - |docutils|_
     - |docutils_ver|
   * - |breathe|_
     - |breathe_ver|
   * - |Pygments|_
     - |Pygments_ver|
   * - |CommonMark|_
     - |CommonMark_ver|
   * - |recommonmark|_
     - |recommonmark_ver|
   * - |Sphinx|_
     - |Sphinx_ver|
   * - |sphinx_tsn_theme|_
     - |sphinx_tsn_theme_ver|
   * - |sphinxcontrib-svg2pdfconverter|_
     - |sphinxcontrib-svg2pdfconverter_ver|
   * - |sphinxcontrib-mscgen|_
     - |sphinxcontrib-mscgen_ver|
   * - |sphinx-tabs|_
     - |sphinx-tabs_ver|
   * - |sphinx-csv-filter|_
     - |sphinx-csv-filter_ver|
