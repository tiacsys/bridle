# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2019-2021 Li-Pro.Net
# Copyright (c) 2019-2021 Nordic Semiconductor ASA
# SPDX-License-Identifier: LicenseRef-Nordic-5-Clause

# Builds combined documentation for all documentation sets: Bridle, Zephyr, etc.
#
# We use our own Sphinx configuration files when building the documentation set
# for each repository, instead of reusing configuration files. See e.g.
# doc/bridle/conf.py and doc/zephyr/conf.py.
#
# Intersphinx (http://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html)
# is used to link documentation sets together. It is configured in the Sphinx
# configuration files.
#
# The *-content targets copy/create .rst files that later get built by Sphinx.

cmake_minimum_required(VERSION 3.20.0)
project(bridle-doc LANGUAGES NONE)

#-------------------------------------------------------------------------------
# Dependencies

set(ZEPHYR_NAME "Zephyr")
set(ZEPHYR_BRIEF "A Scalable Open Source RTOS")
find_package(${ZEPHYR_NAME} REQUIRED HINTS $ENV{ZEPHYR_BASE} COMPONENTS doc)
file(TO_CMAKE_PATH "${ZEPHYR_BASE}" ZEPHYR_BASE)

set(BRIDLE_NAME "Bridle")
set(BRIDLE_BRIEF "A Zephyr based application framework")
find_package(${BRIDLE_NAME} REQUIRED HINTS $ENV{BRIDLE_BASE} COMPONENTS doc)
file(TO_CMAKE_PATH "${BRIDLE_BASE}" BRIDLE_BASE)

#-------------------------------------------------------------------------------
# Options

set(SPHINXOPTS_DEFAULT "-j auto -W --keep-going -T" CACHE INTERNAL "Default Sphinx Options")
set(SPHINXOPTS_EXTRA "" CACHE STRING "Extra Sphinx Options (from CLI/CI)")
set(DT_TURBO_MODE OFF CACHE BOOL "Enable DT turbo mode")
set(HW_FEATURES_TURBO_MODE OFF CACHE BOOL "Enable HW features turbo mode")

separate_arguments(SPHINXOPTS_DEFAULT)
separate_arguments(SPHINXOPTS_EXTRA)

set(DTS_ROOTS "" CACHE STRING "DT bindings root folders")
list(APPEND DTS_ROOTS ${ZEPHYR_BASE})
list(APPEND DTS_ROOTS ${BRIDLE_BASE})

if(WIN32)
  set(SEP $<SEMICOLON>)
else()
  set(SEP :)
endif()

#-------------------------------------------------------------------------------
# Functions

# Add a new docset.
#
# Args:
# - name: Docset name.
# - sphinxopts: Local options passed to the Sphinx build.
# - API: Enable/disable "API" mode. If enabled, Doxygen will be executed.
# - DODGY: Enable/disable "dodgy" mode. If enabled, the ${SPHINXOPTS_DEFAULT}
#   option (used to enable things like -W) will not be passed to Sphinx. It can
#   be useful for external docsets that are likely to generate build warnings.
#
# This function configures multiple targets which can be used to build a docset.
# The docset configuration (conf.py) is expected to be at the ${name} folder
# (relative to the current directory). The sources are taken from the
# ${name}/src folder (relative to the build directory). This means that docsets
# need to make use of the external_content extension in order to gather all
# docset sources into that folder.
#
# Configured targets:
# - ${name}: Alias for ${name}-html.
# - ${name}-html: Run Sphinx "html" build.
# - ${name}-inventory: Run Sphinx "inventory" build. It requires to enable
#   the "inventory" builder on the docset conf.py. This target can be used
#   to solve circular dependencies between docsets.
# - ${name}-linkcheck: Run Sphinx "linkcheck" target.
# - ${name}-clean: Clean build artifacts.
#
function(add_docset name sphinxopts)
  cmake_parse_arguments(DOCSET "API" "" "" ${ARGN})
  cmake_parse_arguments(DOCSET "DODGY" "" "" ${ARGN})

  string(TOUPPER ${name} NAME)
  set(DOCSET_BASE ${${NAME}_BASE})
  set(DOCSET_NAME ${${NAME}_NAME})
  set(DOCSET_VERSION ${${DOCSET_NAME}_VERSION})
  set(DOCSET_BRIEF ${${NAME}_BRIEF})

  set(PROJECT_DOXYGEN_DIR ${DOCSET_BASE}/doc/_doxygen)
  set(SHARED_DOXYGEN_DIR ${CMAKE_CURRENT_LIST_DIR}/_doxygen)
  set(DOCSET_SPHINX_DIR ${CMAKE_CURRENT_LIST_DIR}/${name})
  set(DOCSET_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/${name})
  set(DOCSET_SRC_DIR ${CMAKE_CURRENT_BINARY_DIR}/${name}/src)
  set(DOCSET_DOCTREE_DIR ${CMAKE_CURRENT_BINARY_DIR}/${name}/doctree)
  set(DOCSET_HTML_DIR ${CMAKE_CURRENT_BINARY_DIR}/html/${name})
  set(DOCSET_LINKCHECK_DIR ${CMAKE_CURRENT_BINARY_DIR}/linkcheck/${name})
  set(DOCSET_DOXY_DIR ${CMAKE_CURRENT_BINARY_DIR}/doxygen/${name})
  set(DOCSET_MAKE_DIRS ${DOCSET_BUILD_DIR};${DOCSET_SRC_DIR})
  set(DOCSET_CLEAN_DIRS ${DOCSET_SRC_DIR};${DOCSET_DOCTREE_DIR};${DOCSET_HTML_DIR})
  set(DOCSET_ENV
    DOXYGEN_EXECUTABLE=${DOXYGEN_EXECUTABLE}
    DOT_EXECUTABLE=${DOXYGEN_DOT_EXECUTABLE}
    MSCGEN_EXECUTABLE=${DOXYGEN_MSCGEN_EXECUTABLE}
    DOCSET_DOXY_IN=${SHARED_DOXYGEN_DIR}/doxyfile-${name}.in
    DOCSET_DOXY_PRJ=${PROJECT_DOXYGEN_DIR}
    DOCSET_BASE=${DOCSET_BASE}
    DOCSET_NAME=${DOCSET_NAME}
    DOCSET_BRIEF=${DOCSET_BRIEF}
    DOCSET_VERSION=${DOCSET_VERSION}
  )

  separate_arguments(sphinxopts)

  if(${DOCSET_DODGY})
    list(REMOVE_ITEM SPHINXOPTS_DEFAULT "-W" "--keep-going")
  endif()

  add_doc_target(
    ${name}-inventory
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOCSET_MAKE_DIRS}
    COMMAND ${CMAKE_COMMAND} -E env ${DOCSET_ENV}
      OUTPUT_DIR=${DOCSET_HTML_DIR}
      ${SPHINXBUILD} -v
        -b inventory
        -c ${DOCSET_SPHINX_DIR}
        -d ${DOCSET_DOCTREE_DIR}
        -w ${DOCSET_BUILD_DIR}/inventory.log
           ${SPHINXOPTS_DEFAULT}
           ${SPHINXOPTS_EXTRA}
           ${sphinxopts}
           ${DOCSET_SRC_DIR}
           ${DOCSET_HTML_DIR}
    VERBATIM
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    COMMENT "Generating documentation inventory for ${name}"
    USES_TERMINAL
  )

  add_doc_target(
    ${name}-html
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOCSET_MAKE_DIRS}
    COMMAND ${CMAKE_COMMAND} -E env ${DOCSET_ENV}
      OUTPUT_DIR=${DOCSET_HTML_DIR}
      ${SPHINXBUILD} -v
        -b html
        -c ${DOCSET_SPHINX_DIR}
        -d ${DOCSET_DOCTREE_DIR}
        -w ${DOCSET_BUILD_DIR}/html.log
           ${SPHINXOPTS_DEFAULT}
           ${SPHINXOPTS_EXTRA}
           ${sphinxopts}
           ${DOCSET_SRC_DIR}
           ${DOCSET_HTML_DIR}
    VERBATIM
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    COMMENT "Generating HTML documentation for ${name}"
    USES_TERMINAL
  )

  add_custom_target(
    ${name}-linkcheck
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOCSET_MAKE_DIRS}
    COMMAND ${CMAKE_COMMAND} -E env ${DOCSET_ENV}
      OUTPUT_DIR=${DOCSET_LINKCHECK_DIR}
      ${SPHINXBUILD} -v
        -b linkcheck
        -c ${DOCSET_SPHINX_DIR}
        -d ${DOCSET_DOCTREE_DIR}
        -w ${DOCSET_BUILD_DIR}/linkcheck.log
           ${SPHINXOPTS_DEFAULT}
           ${SPHINXOPTS_EXTRA}
           ${sphinxopts}
           ${DOCSET_SRC_DIR}
           ${DOCSET_HTML_DIR}
    VERBATIM
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    COMMENT "Running documentation linkcheck for ${name}"
    USES_TERMINAL
  )

  set_target_properties(
    ${name}-inventory ${name}-inventory-all
    ${name}-html ${name}-html-all
    ${name}-linkcheck
    PROPERTIES
      ADDITIONAL_CLEAN_FILES "${DOCSET_CLEAN_DIRS}"
  )

  if(${DOCSET_API})
    add_custom_target(
      ${name}-clean
      COMMAND ${CMAKE_COMMAND} -E rm -rf ${DOCSET_CLEAN_DIRS}
      COMMAND ${CMAKE_COMMAND} -E rm -rf ${DOCSET_DOXY_DIR}
      VERBATIM
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      COMMENT "Cleaning documentation sources for ${name}"
      USES_TERMINAL
    )
  else()
    add_custom_target(
      ${name}-clean
      COMMAND ${CMAKE_COMMAND} -E rm -rf ${DOCSET_CLEAN_DIRS}
      VERBATIM
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      COMMENT "Cleaning documentation sources for ${name}"
      USES_TERMINAL
    )
  endif()

  if(${DOCSET_API})
    add_doc_target(
      ${name}-doxygen
      DEPENDS "${DOCSET_DOXY_DIR}/doxyfile"
      COMMAND ${CMAKE_COMMAND} -E make_directory ${DOCSET_DOXY_DIR}
      COMMAND ${CMAKE_COMMAND} -E env ${DOCSET_ENV}
        ${DOXYGEN_EXECUTABLE} ${DOCSET_DOXY_DIR}/doxyfile
      VERBATIM
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      COMMENT "Generating API documentation for ${name}"
      USES_TERMINAL
    )

    set_target_properties(
      ${name}-doxygen
      PROPERTIES
        ADDITIONAL_CLEAN_FILES "${DOCSET_DOXY_DIR}"
    )

    separate_arguments(DOCSET_BRIEF)
    add_custom_command(
      OUTPUT ${DOCSET_DOXY_DIR}/doxyfile
      DEPENDS
        "${BRIDLE_BASE}/doc/update_cfgfile.cmake"
        "${SHARED_DOXYGEN_DIR}/doxyfile-${name}.in"
      COMMAND_EXPAND_LISTS
      COMMAND ${CMAKE_COMMAND} -E touch_nocreate ${DOCSET_DOXY_DIR}/doxyfile
      COMMAND ${CMAKE_COMMAND}
        -DOUT_FILE="${DOCSET_DOXY_DIR}/doxyfile"
        -DIN_FILE="${SHARED_DOXYGEN_DIR}/doxyfile-${name}.in"
        -DDOXY_SET="${name}"
        -DDOXY_OUT="${DOCSET_DOXY_DIR}"
        -DDOXY_IN="${SHARED_DOXYGEN_DIR}"
        -DDOXY_LAYOUT="standalone"
        -DDOXY_LOGOUT="${DOCSET_DOXY_DIR}"
        -DDOXY_LOGWRN="warnings.txt"
        -DPROJECT_DOXY="${PROJECT_DOXYGEN_DIR}"
        -DPROJECT_BASE=${DOCSET_BASE}
        -DPROJECT_NAME="${DOCSET_NAME}"
        -DPROJECT_VERSION="${DOCSET_VERSION}"
        -DPROJECT_BRIEF="${DOCSET_BRIEF}"
        -P ${BRIDLE_BASE}/doc/update_cfgfile.cmake
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      COMMENT "Update doxyfile in ${DOCSET_DOXY_DIR}"
      USES_TERMINAL
    )
  endif()

  add_custom_target(${name})
  add_dependencies(${name} ${name}-html)
endfunction()

# Create a custom doc target.
#
# This function has the same signature as `add_custom_target()`
#
# The function will create two targets for the doc build system.
# - Target 1 named: `<name>`
# - Target 2 named: `<name>-all`
#
# Both targets will produce same result, but target 1 is useful when only
# wanting to build a subset of the docs and missing references to other targets
# are acceptable (warnings will be generated).
#
# Target 2 is used for complete docset builds where it is important that build
# order of each target is under full control.
#
function(add_doc_target name)
  add_custom_target(${name} ${ARGN})
  add_custom_target(${name}-all ${ARGN})
endfunction()

#-------------------------------------------------------------------------------
# Paths

set(ZEPHYR_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/zephyr)
set(BRIDLE_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/bridle)
set(DTS_BINDINGS_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/devicetree)

# HTML output directory
set(HTML_DIR ${CMAKE_CURRENT_BINARY_DIR}/html)
file(MAKE_DIRECTORY ${HTML_DIR})

#-------------------------------------------------------------------------------
# docset: Zephyr

set(zephyr_kws_files
    ${BRIDLE_BASE}/doc/zephyr/known-warnings.txt
)
string(REPLACE ";" "\\;" zephyr_kws_files_escaped "${zephyr_kws_files}")

add_custom_command(
  OUTPUT ${ZEPHYR_BINARY_DIR}/known-warnings.txt
  DEPENDS
    ${BRIDLE_BASE}/doc/update_appends.cmake
    ${zephyr_kws_files}
  COMMAND ${CMAKE_COMMAND}
    -DIN_FILES="${zephyr_kws_files_escaped}"
    -DOUT_FILE=${ZEPHYR_BINARY_DIR}/known-warnings.txt
    -P ${BRIDLE_BASE}/doc/update_appends.cmake
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Update known-warnings.txt in ${ZEPHYR_BINARY_DIR}"
  USES_TERMINAL
)

set(zephyr_kwsi_files
    ${BRIDLE_BASE}/doc/zephyr/known-warnings-inventory.txt
)
string(REPLACE ";" "\\;" zephyr_kwsi_files_escaped "${zephyr_kwsi_files}")

add_custom_command(
  OUTPUT ${ZEPHYR_BINARY_DIR}/known-warnings-inventory.txt
  DEPENDS
    ${BRIDLE_BASE}/doc/update_appends.cmake
    ${zephyr_kwsi_files}
  COMMAND ${CMAKE_COMMAND}
    -DIN_FILES="${zephyr_kwsi_files_escaped}"
    -DOUT_FILE=${ZEPHYR_BINARY_DIR}/known-warnings-inventory.txt
    -P ${BRIDLE_BASE}/doc/update_appends.cmake
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Update known-warnings-inventory.txt in ${ZEPHYR_BINARY_DIR}"
  USES_TERMINAL
)

add_custom_target(
  zephyr-known-warnings
  DEPENDS
    ${ZEPHYR_BINARY_DIR}/known-warnings.txt
    ${ZEPHYR_BINARY_DIR}/known-warnings-inventory.txt
  COMMENT "Generating known warnings lists for zephyr"
)

if(HW_FEATURES_TURBO_MODE)
  message(STATUS "Stub-out the documentation of supported board features in Zephyr")
  add_docset(zephyr "-t hw_features_turbo" API)
else()
  add_docset(zephyr "" API)
endif()

add_dependencies(zephyr-inventory zephyr-known-warnings)
add_dependencies(zephyr-html zephyr-known-warnings)
add_dependencies(zephyr-html-all
    zephyr-known-warnings
    devicetree-inventory
    kconfig-inventory
)

#-------------------------------------------------------------------------------
# docset: devicetree

set(devicetree_bvp_files
    ${ZEPHYR_BASE}/dts/bindings/vendor-prefixes.txt
    ${BRIDLE_BASE}/dts/bindings/vendor-prefixes.txt
)
string(REPLACE ";" "\\;" devicetree_bvp_files_escaped "${devicetree_bvp_files}")

add_custom_command(
  OUTPUT ${DTS_BINDINGS_BINARY_DIR}/vendor-prefixes.txt
  DEPENDS
    ${BRIDLE_BASE}/doc/update_appends.cmake
    ${devicetree_bvp_files}
  COMMAND ${CMAKE_COMMAND}
    -DIN_FILES="${devicetree_bvp_files_escaped}"
    -DOUT_FILE=${DTS_BINDINGS_BINARY_DIR}/vendor-prefixes.txt
    -P ${BRIDLE_BASE}/doc/update_appends.cmake
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Update vendor-prefixes.txt in ${DTS_BINDINGS_BINARY_DIR}"
  USES_TERMINAL
)

add_custom_target(
  devicetree-vendor-prefixes
  DEPENDS
    ${DTS_BINDINGS_BINARY_DIR}/vendor-prefixes.txt
  COMMENT "Generating vendor prefixes list for devicetree"
)

# The devicetree bindings discovered in ${DTS_ROOTS} are parsed and
# documentation for them is generated in the directory
# ${DTS_BINDINGS_RST_OUT}.

set(DTS_ROOT_ARGS)
foreach(root ${DTS_ROOTS})
  list(APPEND DTS_ROOT_ARGS --dts-root ${root})
endforeach()

if(DT_TURBO_MODE)
  message(STATUS "Stub-out the auto-generated Devicetree bindings documentation")
  list(APPEND DTS_ROOT_ARGS --turbo-mode)
endif()

# The CMake variable GEN_DEVICETREE_REST_ZEPHYR_DOCSET will
# be passed to the script in the environment. This allows separating
# the bindings documentation into a standalone Sphinx docset that
# nonetheless can link to Zephyr documentation using intersphinx.
# If empty, the variable has no effect on the script.

set(GEN_DEVICETREE_REST_ZEPHYR_DOCSET zephyr)

set(GEN_DEVICETREE_REST_SCRIPT ${ZEPHYR_BASE}/doc/_scripts/gen_devicetree_rest.py)
set(DTS_BINDINGS_RST_OUT ${DTS_BINDINGS_BINARY_DIR}/src)

add_custom_target(
  devicetree-content
  COMMAND ${CMAKE_COMMAND} -E make_directory ${DTS_BINDINGS_RST_OUT}
  COMMAND ${CMAKE_COMMAND} -E env
    PYTHONPATH=${ZEPHYR_BASE}/scripts/dts/python-devicetree/src${SEP}$ENV{PYTHONPATH}
    ZEPHYR_BASE=${ZEPHYR_BASE}
    GEN_DEVICETREE_REST_ZEPHYR_DOCSET=${GEN_DEVICETREE_REST_ZEPHYR_DOCSET}
    ${PYTHON_EXECUTABLE}
      ${GEN_DEVICETREE_REST_SCRIPT}
        --vendor-prefixes ${DTS_BINDINGS_BINARY_DIR}/vendor-prefixes.txt
                          ${DTS_ROOT_ARGS} ${DTS_BINDINGS_RST_OUT}
  VERBATIM
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Running gen_devicetree_rest.py ${DTS_BINDINGS_RST_OUT}"
  USES_TERMINAL
)

set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${GEN_DEVICETREE_REST_SCRIPT})

add_docset(devicetree "")

add_dependencies(devicetree-content devicetree-vendor-prefixes)
add_dependencies(devicetree-inventory devicetree-content)
add_dependencies(devicetree-html devicetree-content)
add_dependencies(devicetree-html-all
    devicetree-content
    zephyr-inventory
)

#-------------------------------------------------------------------------------
# docset: kconfig

add_docset(kconfig "")

add_dependencies(kconfig-html-all zephyr-inventory)

#-------------------------------------------------------------------------------
# docset: bridle

set(tools_version_files
    ${BRIDLE_BASE}/scripts/tools-versions-minimum.txt
    ${BRIDLE_BASE}/scripts/tools-versions-macos.txt
    ${BRIDLE_BASE}/scripts/tools-versions-win1x.txt
    ${BRIDLE_BASE}/scripts/tools-versions-linux.txt
)

set(pip_requirements_files
    ${ZEPHYR_BASE}/doc/requirements.txt
    ${ZEPHYR_BASE}/scripts/requirements-base.txt
    ${BRIDLE_BASE}/scripts/requirements-base.txt
    ${BRIDLE_BASE}/scripts/requirements-doc.txt
    ${BRIDLE_BASE}/scripts/requirements-build.txt
    ${BRIDLE_BASE}/scripts/requirements-extras.txt
)

string(REPLACE ";" "\\;" tools_files_escaped "${tools_version_files}")
string(REPLACE ";" "\\;" pip_files_escaped "${pip_requirements_files}")

set(BRIDLE_DOC_DIR ${BRIDLE_BASE}/doc/bridle)

add_custom_command(
  OUTPUT ${BRIDLE_BINARY_DIR}/src/versions.txt
  DEPENDS
    ${BRIDLE_BASE}/doc/update_versions.cmake
    ${BRIDLE_DOC_DIR}/versions.txt.in
    ${tools_version_files}
    ${pip_requirements_files}
  COMMAND ${CMAKE_COMMAND}
    -DTOOLS_VERSION_FILES="${tools_files_escaped}"
    -DPIP_REQUIREMENTS_FILES="${pip_files_escaped}"
    -DVERSION_IN=${BRIDLE_DOC_DIR}/versions.txt.in
    -DVERSION_OUT=${BRIDLE_BINARY_DIR}/src/versions.txt
    -P ${BRIDLE_BASE}/doc/update_versions.cmake
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Update versions.txt in ${BRIDLE_BINARY_DIR}"
  USES_TERMINAL
)

add_custom_target(
  bridle-versions
  DEPENDS
    ${BRIDLE_BINARY_DIR}/src/versions.txt
  COMMENT "Generating versions list for bridle"
)

if(HW_FEATURES_TURBO_MODE)
  message(STATUS "Stub-out the documentation of supported board features in Bridle")
  add_docset(bridle "-t hw_features_turbo" API)
else()
  add_docset(bridle "" API)
endif()

add_dependencies(bridle-inventory bridle-versions)
add_dependencies(bridle-html bridle-versions)
add_dependencies(bridle-html-all
    bridle-versions
    devicetree-inventory
    kconfig-inventory
    zephyr-inventory
)

#-------------------------------------------------------------------------------
# Deployment targets

add_custom_target(
  copy-extra-content
  COMMAND ${CMAKE_COMMAND} -E make_directory ${HTML_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_LIST_DIR}/_docroot/.htaccess
    ${CMAKE_CURRENT_LIST_DIR}/_docroot/index.html
    ${BRIDLE_BASE}/doc/versions.json
    ${HTML_DIR}
  VERBATIM
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Copy HTML extra content"
  USES_TERMINAL
)

set_target_properties(
  copy-extra-content
  PROPERTIES
    ADDITIONAL_CLEAN_FILES "${HTML_DIR}"
)

add_custom_target(
  merge-search-indexes
  COMMAND
    ${PYTHON_EXECUTABLE}
      ${BRIDLE_BASE}/doc/_scripts/merge_search_indexes.py
        -b ${CMAKE_CURRENT_BINARY_DIR}
  VERBATIM
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Merging HTML search indexes"
  USES_TERMINAL
)

add_dependencies(merge-search-indexes
    bridle-html-all
    zephyr-html-all
)

#-------------------------------------------------------------------------------
# Global targets

add_dependencies(zephyr-html-all
    kconfig-html-all
    devicetree-html-all
)

add_dependencies(bridle-html-all
    zephyr-html-all
)

add_custom_target(build-all ALL)
add_dependencies(build-all
    copy-extra-content
    merge-search-indexes
    bridle-html-all
)

add_custom_target(linkcheck)
add_dependencies(linkcheck
    bridle-linkcheck
    zephyr-linkcheck
)
