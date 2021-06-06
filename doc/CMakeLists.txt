# Copyright (c) 2019-2021 Li-Pro.Net
# Copyright (c) 2019-2020 Nordic Semiconductor ASA
# SPDX-License-Identifier: LicenseRef-Nordic-5-Clause

# Builds combined documentation for all documentation sets: Li-Pro.Net bridle
# to embedded environment (LPNB), Zephyr, etc.
#
# We use our own Sphinx configuration files when building the documentation set
# for each repository, instead of reusing configuration files. See e.g.
# doc/lpnb/conf.py and doc/zephyr/conf.py.
#
# Intersphinx (http://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html)
# is used to link documentation sets together. It is configured in the Sphinx
# configuration files.
#
# The *-content targets copy/create .rst files that later get built by Sphinx.

cmake_minimum_required(VERSION 3.13.1)
project(lpn-bridle-doc LANGUAGES)

set(NO_BOILERPLATE TRUE)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE} ..)

#
# Set various *_BASE variables pointing to the lpnb/, zephyr/, etc.,
# directories. Derive them automatically if they're not set in the environment,
# by assuming that e.g. lpnbxlib can be found at ../../lpnbxlib/. Also add them
# to the environment if they're not there.
#

get_filename_component(BRIDLE_BASE ${CMAKE_CURRENT_LIST_DIR}../ DIRECTORY)
set(ENV{BRIDLE_BASE} ${BRIDLE_BASE})

message(STATUS "BRIDLE_BASE: $ENV{BRIDLE_BASE}")
message(STATUS "ZEPHYR_BASE: ${ZEPHYR_BASE}")

# Output directory for the shared Devicetree bindings and
# DTS root folders that have to parse (YAML to RTS).
set(DTS_BINDINGS_BINARY_DIR ${CMAKE_BINARY_DIR}/devicetree)
set(DTS_BINDINGS_RST_OUT ${DTS_BINDINGS_BINARY_DIR})
set(DTS_ROOTS ${ZEPHYR_BASE} ${BRIDLE_BASE})

message(STATUS "DTS_ROOTS: ${DTS_ROOTS}")

#
# Find programs we need (Python, Sphinx, and Doxygen)
#

find_package(PythonInterp 3.6)
set(DOXYGEN_SKIP_DOT True) # Skip the otional Dot component
find_package(Doxygen REQUIRED)

find_program(SPHINXBUILD sphinx-build)
if(${SPHINXBUILD} STREQUAL SPHINXBUILD-NOTFOUND)
  message(FATAL_ERROR "The 'sphinx-build' command was not found. Make sure you have Sphinx installed.")
endif()

#
# CMake build directories (build/zephyr, build/lpnb, etc.) and the shared
# HTML output directory.
#

set(ZEPHYR_BINARY_DIR ${CMAKE_BINARY_DIR}/zephyr)
set(BRIDLE_BINARY_DIR ${CMAKE_BINARY_DIR}/lpnb)

# Output directory for the shared Kconfig reference
set(KCONFIG_BINARY_DIR ${CMAKE_BINARY_DIR}/Kconfig)

# HTML output directory
set(HTML_DIR ${CMAKE_BINARY_DIR}/html)
file(MAKE_DIRECTORY ${HTML_DIR})

# Known issues script
set(KI_SCRIPT ${ZEPHYR_BASE}/scripts/filter-known-issues.py)

#
# Add the 'zephyr' target for building the Zephyr documentation. We reuse
# doc/CMakeLists.txt from the Zephyr repository, but use our own Sphinx
# configuration from doc/zephyr/conf.py. The generated HTML is placed in
# the common Sphinx HTML output folder.
#

# Parameters to doc/CMakeLists.txt in Zephyr
set(SPHINXOPTS -c ${BRIDLE_BASE}/doc/zephyr)
set(SPHINX_OUTPUT_DIR ${HTML_DIR}/zephyr)
set(KCONFIG_OUTPUT ${HTML_DIR}/kconfig)
set(DTS_BINDINGS_OUTPUT ${HTML_DIR}/devicetree)
set(GEN_DEVICETREE_REST_ZEPHYR_DOCSET " ")

# Get access to the 'html' target from doc/CMakeLists.txt in Zephyr
set(MODULES_EXT_ROOT ${BRIDLE_BASE})
add_subdirectory(${ZEPHYR_BASE}/doc ${ZEPHYR_BINARY_DIR})

# LPNB-specific parameters to pass these through to doc/zephyr/conf.py (the
# Sphinx configuration file). We use it for HTML Templates and Intersphinx.
set(zephyr_sphinx_environment
  ZEPHYR_BASE=${ZEPHYR_BASE}
  ZEPHYR_BUILD=${ZEPHYR_BINARY_DIR}
  ZEPHYR_OUTPUT=${SPHINX_OUTPUT_DIR}
  ZEPHYR_RST_SRC=${ZEPHYR_BINARY_DIR}/rst/doc
  KCONFIG_OUTPUT=${KCONFIG_OUTPUT}
  DTS_BINDINGS_OUTPUT=${DTS_BINDINGS_OUTPUT}
  BRIDLE_BASE=${BRIDLE_BASE}
)

# The 'html' target is from Zephyr
set(ZEPHYR_SPHINX_BUILD_HTML_COMMAND
  ${CMAKE_COMMAND} -E env
    ${zephyr_sphinx_environment}
      ${CMAKE_MAKE_PROGRAM} html
)

add_custom_target(
  zephyr-html
  COMMAND ${ZEPHYR_SPHINX_BUILD_HTML_COMMAND}
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
  COMMENT "Generating Zephyr HTML documentation with ${SPHINXBUILD} ${SPHINXOPTS}"
  USES_TERMINAL
)
add_dependencies(zephyr-html kconfig-html devicetree-html)

add_custom_target(zephyr)
add_dependencies(zephyr zephyr-html)

#
# Add 'clean-zephyr', 'clean-lpnb', etc., targets
#

foreach(target kconfig devicetree zephyr lpnb)
  set(TARGET_BINARY_DIR ${CMAKE_BINARY_DIR}/${target})
  # Cleanup build output
  add_custom_target(
    clean-${target}
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${TARGET_BINARY_DIR}/doctrees
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${TARGET_BINARY_DIR}/doxygen
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${TARGET_BINARY_DIR}/rst
    COMMAND ${CMAKE_COMMAND} -E remove ${TARGET_BINARY_DIR}/*.log
    COMMAND ${CMAKE_COMMAND} -E remove ${TARGET_BINARY_DIR}/*.warnings
    COMMAND ${CMAKE_COMMAND} -E remove ${TARGET_BINARY_DIR}/last_doxy_run_tstamp
    # Remove generated HTML as well
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${HTML_DIR}/${target}
  )
endforeach()

#
# Add lpnb-related targets
#

set(BRIDLE_SPHINXOPTS -d ${BRIDLE_BINARY_DIR}/doctrees ${BRIDLE_SPHINXOPTS})

set(BRIDLE_DOC_DIR ${BRIDLE_BASE}/doc/lpnb)

set(BRIDLE_DOXYFILE_IN ${BRIDLE_DOC_DIR}/lpnb.doxyfile.in)
set(BRIDLE_DOXYFILE_OUT ${BRIDLE_BINARY_DIR}/lpnb.doxyfile)
set(BRIDLE_RST_OUT ${BRIDLE_BINARY_DIR}/rst)
set(BRIDLE_DOC_LOG ${BRIDLE_BINARY_DIR}/doc.log)
set(BRIDLE_DOXY_LOG ${BRIDLE_BINARY_DIR}/doxy.log)
set(BRIDLE_SPHINX_LOG ${BRIDLE_BINARY_DIR}/sphinx.log)
set(BRIDLE_CONTENT_OUTPUTS ${BRIDLE_BINARY_DIR}/extracted-content.txt)
set(BRIDLE_DOC_WARN ${BRIDLE_BINARY_DIR}/doc.warnings)
set(BRIDLE_KI_DIR ${BRIDLE_BASE}/.known-issues/doc)

configure_file(${BRIDLE_DOXYFILE_IN} ${BRIDLE_DOXYFILE_OUT} @ONLY)

set(tools_version_files
    ${BRIDLE_BASE}/scripts/tools-versions-minimum.txt
    ${BRIDLE_BASE}/scripts/tools-versions-darwin.txt
    ${BRIDLE_BASE}/scripts/tools-versions-win10.txt
    ${BRIDLE_BASE}/scripts/tools-versions-linux.txt
)

set(pip_requirements_files
    ${ZEPHYR_BASE}/scripts/requirements-base.txt
    ${ZEPHYR_BASE}/scripts/requirements-doc.txt
    ${BRIDLE_BASE}/scripts/requirements-base.txt
    ${BRIDLE_BASE}/scripts/requirements-doc.txt
    ${BRIDLE_BASE}/scripts/requirements-build.txt
)

string(REPLACE ";" "\\;" tools_files_escaped "${tools_version_files}")
string(REPLACE ";" "\\;" pip_files_escaped "${pip_requirements_files}")

add_custom_command(
  OUTPUT ${BRIDLE_RST_OUT}/doc/lpnb/versions.txt
  COMMAND ${CMAKE_COMMAND}
    -DTOOLS_VERSION_FILES="${tools_files_escaped}"
    -DPIP_REQUIREMENTS_FILES="${pip_files_escaped}"
    -DVERSION_IN=${BRIDLE_DOC_DIR}/versions.txt.in
    -DVERSION_OUT=${BRIDLE_RST_OUT}/doc/lpnb/versions.txt
    -P ${BRIDLE_BASE}/doc/update_versions.cmake
  DEPENDS
    ${BRIDLE_DOC_DIR}/versions.txt.in
    ${tools_version_files}
    ${pip_requirements_files}
)

add_custom_target(
  lpnb-doxy
  COMMAND ${CMAKE_COMMAND}
    -DCOMMAND=${DOXYGEN_EXECUTABLE}
    -DARGS="${BRIDLE_DOXYFILE_OUT}"
    -DOUTPUT_FILE=${BRIDLE_DOXY_LOG}
    -DERROR_FILE=${BRIDLE_DOXY_LOG}
    -DWORKING_DIRECTORY=${CMAKE_CURRENT_LIST_DIR}
    -P ${ZEPHYR_BASE}/cmake/util/execute_process.cmake
)

set(BRIDLE_EXTRACT_CONTENT_COMMAND
  ${CMAKE_COMMAND} -E env
  ZEPHYR_BASE=${BRIDLE_BASE}
  ${PYTHON_EXECUTABLE} ${ZEPHYR_BASE}/doc/scripts/extract_content.py
  --outputs ${BRIDLE_CONTENT_OUTPUTS}
  --ignore ${CMAKE_CURRENT_BINARY_DIR}
  --sphinx-src-root ${BRIDLE_DOC_DIR}
  "*:doc:${BRIDLE_RST_OUT}"
  # We want to copy the .rst files in samples/ and boards/ to the rst
  # folder, and also the doc folder inside rst.
  #
  # Some files refer to items in samples/ and boards/ relative to
  # their actual position in the Zephyr tree. For example, in
  # subsystems/sensor.rst:
  #
  # .. literalinclude:: ../../samples/sensor/my4711/src/main.c
  #
  # The additional copy is a hackaround so these references work.
  "*.rst:boards:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.csv:boards:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.ioc:boards:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.pdf:boards:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.rst:samples:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.rst:applications:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.rst:include:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.rst:lib:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.rst:drivers:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.rst:scripts:${BRIDLE_RST_OUT}/doc/lpnb"
  "*.rst:tests:${BRIDLE_RST_OUT}/doc/lpnb"
  "release-notes*.rst:doc:${BRIDLE_RST_OUT}/doc/lpnb"
  "changelog.rst:doc:${BRIDLE_RST_OUT}/doc/lpnb"
)


add_custom_target(
  lpnb-content
  # Copy all files in doc/ to the rst folder
  COMMAND ${BRIDLE_EXTRACT_CONTENT_COMMAND}
  WORKING_DIRECTORY ${BRIDLE_DOC_DIR}
  DEPENDS ${BRIDLE_RST_OUT}/doc/lpnb/versions.txt
  COMMENT "Copying files to ${BRIDLE_RST_OUT}"
  USES_TERMINAL
)

if(WIN32)
  set(SEP $<SEMICOLON>)
else()
  set(SEP :)
endif()

set(lpnb_sphinx_environment
  ZEPHYR_BASE=${ZEPHYR_BASE}
  ZEPHYR_BUILD=${ZEPHYR_BINARY_DIR}
  ZEPHYR_OUTPUT=${SPHINX_OUTPUT_DIR}
  ZEPHYR_RST_SRC=${ZEPHYR_BINARY_DIR}/rst/doc
  KCONFIG_OUTPUT=${KCONFIG_OUTPUT}
  DTS_BINDINGS_OUTPUT=${DTS_BINDINGS_OUTPUT}
  BRIDLE_BASE=${BRIDLE_BASE}
  BRIDLE_BUILD=${BRIDLE_BINARY_DIR}
  BRIDLE_OUTPUT=${HTML_DIR}/lpnb
  BRIDLE_RST_SRC=${BRIDLE_RST_OUT}/doc/lpnb
)

set(LPNB_SPHINX_BUILD_HTML_COMMAND
  ${CMAKE_COMMAND} -E env
    ${lpnb_sphinx_environment}
      ${SPHINXBUILD}
        -w ${BRIDLE_SPHINX_LOG}
	-N
	-b html
	${BRIDLE_SPHINXOPTS}
	${BRIDLE_RST_OUT}/doc/lpnb
	${HTML_DIR}/lpnb
)

add_custom_target(
  lpnb-html
  COMMAND ${LPNB_SPHINX_BUILD_HTML_COMMAND}
  # Merge the Doxygen and Sphinx logs into a single file
  COMMAND ${CMAKE_COMMAND}
    -P ${ZEPHYR_BASE}/cmake/util/fmerge.cmake
    ${BRIDLE_DOC_LOG}
    ${BRIDLE_DOXY_LOG}
    ${BRIDLE_SPHINX_LOG}
  COMMAND ${PYTHON_EXECUTABLE} ${KI_SCRIPT}
    --config-dir ${BRIDLE_KI_DIR}
    --errors ${BRIDLE_DOC_WARN}
    --warnings ${BRIDLE_DOC_WARN}
    ${BRIDLE_DOC_LOG}
  # Copy root index file
  COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_LIST_DIR}/static/html/index.html
    ${HTML_DIR}
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Generating Li-Pro.Net bridle HTML documentation with ${SPHINXBUILD} to ${HTML_DIR}/lpnb"
  USES_TERMINAL
)
add_dependencies(lpnb-html lpnb-doxy lpnb-content kconfig-html devicetree-html zephyr)

add_custom_target(
  lpnb-copy-versions
  COMMAND ${CMAKE_COMMAND} -E copy
    ${BRIDLE_BASE}/doc/versions.json
    ${HTML_DIR}/versions.json
)

add_custom_target(lpnb)
add_dependencies(lpnb lpnb-html lpnb-copy-versions)

#
# Add targets for building the shared Kconfig reference
#

# The Kconfig reference is a separate documentation set that's shared between
# all modules (LPNB, Zephyr, etc.). This makes it possible to link to Kconfig
# symbols regardless of where they are defined.
#
# We rely on the Zephyr Kconfig files pulling in the other Kconfig files, and
# use the --modules option to gen_kconfig_rest.py to split the documentation
# into a separate page for each module.

set(KCONFIG_RST_OUT ${KCONFIG_BINARY_DIR}/rst)
get_directory_property(
  ZEPHYR_KCONFIG_MODULES
  DIRECTORY ${ZEPHYR_BASE}/doc
  DEFINITION ZEPHYR_KCONFIG_MODULES
)

# The 'kconfig-content' target uses gen_kconfig_rest.py to generate .rst files
# for all Kconfig symbols, as well as index pages that point to them.
add_custom_target(
  kconfig-content
  COMMAND ${CMAKE_COMMAND} -E make_directory ${KCONFIG_RST_OUT}
  COMMAND ${CMAKE_COMMAND} -E env
    PYTHONPATH=${ZEPHYR_BASE}/scripts/kconfig${SEP}$ENV{PYTHONPATH}
    ZEPHYR_BASE=${ZEPHYR_BASE}
    srctree=${ZEPHYR_BASE}
    BOARD_DIR=boards/*/*/
    ARCH=*
    ARCH_DIR=arch/
    SOC_DIR=soc/
    KCONFIG_BINARY_DIR=${KCONFIG_BINARY_DIR}
    KCONFIG_WARN_UNDEF=y
    KCONFIG_TURBO_MODE=${KCONFIG_TURBO_MODE}
    KCONFIG_DOC_MODE=1
    ${ZEPHYR_KCONFIG_MODULES}
      ${PYTHON_EXECUTABLE}
        ${ZEPHYR_BASE}/doc/scripts/gen_kconfig_rest.py ${KCONFIG_RST_OUT}
        --separate-all-index
        --keep-module-paths
        --modules "Zephyr Architecture,zephyr-arch,${ZEPHYR_BASE}/arch"
                  "Zephyr SoC,zephyr-soc,${ZEPHYR_BASE}/soc"
                  "Zephyr Driver,zephyr-drivers,${ZEPHYR_BASE}/drivers"
                  "Zephyr Boards,zephyr-boards,${ZEPHYR_BASE}/boards"
                  "Zephyr Kernel,zephyr-kernel,${ZEPHYR_BASE}/kernel"
                  "Zephyr Library,zephyr-lib,${ZEPHYR_BASE}/lib"
                  "Zephyr Subsystem,zephyr-subsys,${ZEPHYR_BASE}/subsys"
                  "Zephyr Modules,zephyr-modules,${ZEPHYR_BASE}/modules"
                  "Li-Pro.Net bridle,lpnb,${BRIDLE_BASE}"
        --no-index-modules BuildDir,${CMAKE_BINARY_DIR}
  VERBATIM
)

# LPNB-specific parameters to pass these through to doc/kconfig/conf.py (the
# Sphinx configuration file). We use it for HTML Templates and Intersphinx.
set(kconfig_sphinx_environment
  ZEPHYR_BASE=${ZEPHYR_BASE}
  ZEPHYR_BUILD=${CMAKE_CURRENT_BINARY_DIR}
  BRIDLE_BASE=${BRIDLE_BASE}
)

# No 'kconfig' target exists, because it clashes with the imported 'kconfig'
# target from the Zephyr repository.

add_custom_target(
  kconfig-html
  COMMAND ${CMAKE_COMMAND} -E env
    ${kconfig_sphinx_environment}
      ${SPHINXBUILD}
        -b html
        -c ${BRIDLE_BASE}/doc/kconfig
        -d ${KCONFIG_BINARY_DIR}/doctrees
        -N
        -w ${KCONFIG_BINARY_DIR}/sphinx.log
        # The Kconfig reference build doesn't use Breathe, so we can safely
        # parallelize it
        -j auto
        ${KCONFIG_RST_OUT}
        ${HTML_DIR}/kconfig
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT "Generating Kconfig HTML reference with ${SPHINXBUILD} to ${HTML_DIR}/kconfig"
  USES_TERMINAL
)
add_dependencies(kconfig-html kconfig-content)

#
# Add targets for building the shared Devicetree bindings
#

# The Devicetree bindings is a separate documentation set that's shared
# between all modules (LPNB, Zephyr, etc.). This makes it possible to link
# to Devicetree symbols regardless of where they are defined.
#
# LPNB-specific parameters to pass these through to doc/kconfig/conf.py (the
# Sphinx configuration file). We use it for HTML Templates and Intersphinx.
set(devicetree_sphinx_environment
  ZEPHYR_BASE=${ZEPHYR_BASE}
  ZEPHYR_BUILD=${CMAKE_CURRENT_BINARY_DIR}
  ZEPHYR_OUTPUT=${SPHINX_OUTPUT_DIR}
  DTS_BINDINGS_OUTPUT=${DTS_BINDINGS_OUTPUT}
  BRIDLE_BASE=${BRIDLE_BASE}
)

# No 'devicetree' target exists, because it clashes with the imported
# 'devicetree' target from the Zephyr repository that generates .rst files
# for all Devicetree bindings, as well as index pages that point to them.

add_custom_target(
  devicetree-html
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
    ${BRIDLE_BASE}/doc/devicetree/*.rst
    ${DTS_BINDINGS_RST_OUT}
  COMMAND ${CMAKE_COMMAND} -E env
    ${devicetree_sphinx_environment}
      ${SPHINXBUILD}
        -b html
        -c ${BRIDLE_BASE}/doc/devicetree
        -d ${DTS_BINDINGS_BINARY_DIR}/doctrees
        -N
        -w ${DTS_BINDINGS_BINARY_DIR}/sphinx.log
        # The Kconfig reference build doesn't use Breathe, so we can safely
        # parallelize it
        -j auto
        ${DTS_BINDINGS_RST_OUT}
        ${HTML_DIR}/devicetree
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT "Generating Devicetree HTML bindings with ${SPHINXBUILD} to ${HTML_DIR}/devicetree"
  USES_TERMINAL
)
add_dependencies(devicetree-html devicetree)

add_custom_target(
  build-all
  COMMAND ${CMAKE_MAKE_PROGRAM} kconfig-html
  COMMAND ${CMAKE_MAKE_PROGRAM} devicetree-html
  COMMAND ${CMAKE_MAKE_PROGRAM} zephyr
  COMMAND ${CMAKE_MAKE_PROGRAM} lpnb
  COMMENT "Generating all Li-Pro.Net bridle HTML documentation to ${HTML_DIR}"
  USES_TERMINAL
)

#
# Add targets for checking links
#

add_custom_target(
  lpnb-linkcheck
  COMMAND ${CMAKE_COMMAND} -E env
    ${lpnb_sphinx_environment}
      ${SPHINXBUILD}
        -w ${BRIDLE_SPHINX_LOG}
	-N
	-b linkcheck
	${BRIDLE_SPHINXOPTS}
	${BRIDLE_RST_OUT}/doc/lpnb
	${BRIDLE_BINARY_DIR}
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  USES_TERMINAL
)

add_dependencies(lpnb-linkcheck lpnb-doxy lpnb-content kconfig-html devicetree-html zephyr)

add_custom_target(linkcheck)
add_dependencies(linkcheck lpnb-linkcheck)
