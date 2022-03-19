# Copyright (c) 2021-2022 TiaC Systems
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
project(bridle-doc LANGUAGES)

set(NO_BOILERPLATE TRUE)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE} ..)

#-------------------------------------------------------------------------------
# Options

set(SPHINXOPTS_DEFAULT -j auto CACHE INTERNAL "Default Sphinx Options")
set(SPHINXOPTS_EXTRA "" CACHE STRING "Extra Sphinx Options (from CLI/CI)")

if(WIN32)
  set(SEP $<SEMICOLON>)
else()
  set(SEP :)
endif()

#-------------------------------------------------------------------------------
# Dependencies

find_package(PythonInterp 3.6)
set(DOXYGEN_SKIP_DOT True)  # Skip the otional Dot component
find_package(Doxygen REQUIRED)

find_program(SPHINXBUILD sphinx-build)
if(NOT SPHINXBUILD)
  message(FATAL_ERROR "The 'sphinx-build' command was not found. Make sure you have Sphinx installed.")
endif()

find_program(WEST west)
if(NOT WEST)
  message(FATAL_ERROR "The 'west' command was not found")
endif()

set(KCONFIG_BINARY_DIR ${CMAKE_BINARY_DIR}/kconfig)
list(INSERT MODULE_EXT_ROOT 0 ${ZEPHYR_BASE})
file(MAKE_DIRECTORY ${KCONFIG_BINARY_DIR})

include(${ZEPHYR_BASE}/cmake/extensions.cmake)
include(${ZEPHYR_BASE}/cmake/zephyr_module.cmake)

#-------------------------------------------------------------------------------
# Functions

# Add a new docset.
#
# Args:
# - name: Docset name.
# - env: Environment passed to the Sphinx build.
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
# - ${name}-inventory: Run Sphinx "inventory" build. It requires to enable
#   the "inventory" builder on the docset conf.py. This target can be used
#   to solve circular dependencies between docsets.
# - ${name}-html: Run Sphinx "html" build.
# - ${name}-linkcheck: Run Sphinx "linkcheck" target.
# - ${name}-clean: Clean build artifacts.
#
function(add_docset name env sphinxopts)
  set(DOCSET_CFG_DIR ${CMAKE_CURRENT_LIST_DIR}/${name})
  set(DOCSET_BUILD_DIR ${CMAKE_BINARY_DIR}/${name})
  set(DOCSET_SRC_DIR ${CMAKE_BINARY_DIR}/${name}/src)
  set(DOCSET_DOX_DIR ${CMAKE_BINARY_DIR}/${name}/doxygen)
  set(DOCSET_HTML_DIR ${CMAKE_BINARY_DIR}/html/${name})
  set(DOCSET_MAKE_DIRS ${DOCSET_BUILD_DIR};${DOCSET_SRC_DIR};${DOCSET_DOX_DIR})
  set(DOCSET_CLEAN_DIRS ${DOCSET_SRC_DIR};${DOCSET_DOX_DIR};${DOCSET_HTML_DIR})

  add_doc_target(
    ${name}-inventory
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOCSET_MAKE_DIRS}
    COMMAND ${CMAKE_COMMAND} -E env ${env}
    ${SPHINXBUILD} -v
      -b inventory
      -c ${DOCSET_CFG_DIR}
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
    COMMAND ${CMAKE_COMMAND} -E env ${env}
    ${SPHINXBUILD} -v
      -b html
      -c ${DOCSET_CFG_DIR}
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
    COMMAND ${CMAKE_COMMAND} -E env ${env}
    ${SPHINXBUILD} -v
      -b linkcheck
      -c ${DOCSET_CFG_DIR}
      -w ${DOCSET_BUILD_DIR}/linkcheck.log
      ${SPHINXOPTS_DEFAULT}
      ${SPHINXOPTS_EXTRA}
      ${sphinxopts}
      ${DOCSET_SRC_DIR}
      ${DOCSET_BUILD_DIR}
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

  if(${CMAKE_VERSION} VERSION_LESS 3.17)
    add_custom_target(
      ${name}-clean
      COMMAND ${CMAKE_COMMAND} -E remove_directory ${DOCSET_CLEAN_DIRS}
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
# Environment & Paths

# Set various *_BASE variables pointing to the bridle/, zephyr/, etc.,
# directories. Derive them automatically if they're not set in the environment,
# by assuming that e.g. bridlexlib can be found at ../../bridlexlib/. Also add
# them to the environment if they're not there.
#

get_filename_component(BRIDLE_BASE ${CMAKE_CURRENT_LIST_DIR}../ DIRECTORY)
set(ENV{BRIDLE_BASE} ${BRIDLE_BASE})

message(STATUS "ZEPHYR_BASE: ${ZEPHYR_BASE}")
message(STATUS "BRIDLE_BASE: $ENV{BRIDLE_BASE}")

set(DTS_ROOTS)
list(APPEND DTS_ROOTS ${ZEPHYR_BASE})
list(APPEND DTS_ROOTS ${BRIDLE_BASE})

set(ZEPHYR_BINARY_DIR ${CMAKE_BINARY_DIR}/zephyr)
set(BRIDLE_BINARY_DIR ${CMAKE_BINARY_DIR}/bridle)
set(DTS_BINDINGS_BINARY_DIR ${CMAKE_BINARY_DIR}/devicetree)

# HTML output directory
set(HTML_DIR ${CMAKE_BINARY_DIR}/html)
file(MAKE_DIRECTORY ${HTML_DIR})

#-------------------------------------------------------------------------------
# docset: Zephyr

set(zephyr_kws_files
    ${ZEPHYR_BASE}/doc/known-warnings.txt
    ${BRIDLE_BASE}/doc/zephyr/known-warnings.txt
)
string(REPLACE ";" "\\;" zephyr_kws_files_escaped "${zephyr_kws_files}")

add_custom_command(
  OUTPUT ${ZEPHYR_BINARY_DIR}/known-warnings.txt
  COMMAND ${CMAKE_COMMAND}
    -DIN_FILES="${zephyr_kws_files_escaped}"
    -DOUT_FILE=${ZEPHYR_BINARY_DIR}/known-warnings.txt
    -P ${BRIDLE_BASE}/doc/update_appends.cmake
  DEPENDS
    ${zephyr_kws_files}
)

add_custom_target(
  zephyr-known-warnings
  DEPENDS
    ${ZEPHYR_BINARY_DIR}/known-warnings.txt
)

set(zephyr_env
  BRIDLE_BASE=${BRIDLE_BASE}
  ZEPHYR_BASE=${ZEPHYR_BASE}
  ZEPHYR_BUILD=${ZEPHYR_BINARY_DIR}
  DOXYGEN_EXECUTABLE=${DOXYGEN_EXECUTABLE}
)

add_docset(zephyr "${zephyr_env}" "")
add_dependencies(zephyr-inventory zephyr-known-warnings kconfig-inventory)
add_dependencies(zephyr-inventory-all zephyr-known-warnings kconfig-inventory-all)
add_dependencies(zephyr-html zephyr-known-warnings kconfig-inventory)
add_dependencies(zephyr-html-all zephyr-known-warnings kconfig-inventory-all)

#-------------------------------------------------------------------------------
# docset: devicetree

# The CMake variable GEN_DEVICETREE_REST_ZEPHYR_DOCSET will
# be passed to the script in the environment. This allows separating
# the bindings documentation into a standalone Sphinx docset that
# nonetheless can link to Zephyr documentation using intersphinx.
# If empty, the variable has no effect on the script.

set(GEN_DEVICETREE_REST_SCRIPT ${ZEPHYR_BASE}/doc/_scripts/gen_devicetree_rest.py)
set(GEN_DEVICETREE_REST_ZEPHYR_DOCSET zephyr)

# The devicetree bindings discovered in ${DTS_ROOTS} are parsed and
# documentation for them is generated in the directory
# ${DTS_BINDINGS_RST_OUT}.

if(NOT DTS_ROOTS)
  set(DTS_ROOTS ${ZEPHYR_BASE})
endif()

set(DTS_ROOT_ARGS)
foreach(root ${DTS_ROOTS})
  list(APPEND DTS_ROOT_ARGS --dts-root ${root})
endforeach()

set(DTS_BINDINGS_RST_OUT ${DTS_BINDINGS_BINARY_DIR}/src)

add_custom_target(
  devicetree-content
  COMMAND ${CMAKE_COMMAND} -E make_directory ${DTS_BINDINGS_RST_OUT}
  COMMAND ${CMAKE_COMMAND} -E env
  PYTHONPATH=${ZEPHYR_BASE}/scripts/dts/python-devicetree/src${SEP}$ENV{PYTHONPATH}
  ZEPHYR_BASE=${ZEPHYR_BASE}
  GEN_DEVICETREE_REST_ZEPHYR_DOCSET=${GEN_DEVICETREE_REST_ZEPHYR_DOCSET}
  ${PYTHON_EXECUTABLE} ${GEN_DEVICETREE_REST_SCRIPT}
    --vendor-prefixes ${ZEPHYR_BASE}/dts/bindings/vendor-prefixes.txt
    ${DTS_ROOT_ARGS} ${DTS_BINDINGS_RST_OUT}
  VERBATIM
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Running gen_devicetree_rest.py ${DTS_BINDINGS_RST_OUT}"
  USES_TERMINAL
)

set(devicetree_env
  ZEPHYR_BASE=${ZEPHYR_BASE}
  BRIDLE_BASE=${BRIDLE_BASE}
)

add_docset(devicetree "${devicetree_env}" "")
add_dependencies(devicetree-inventory devicetree-content zephyr-inventory)
add_dependencies(devicetree-inventory-all devicetree-content zephyr-inventory-all)
add_dependencies(devicetree-html devicetree-content zephyr-inventory)
add_dependencies(devicetree-html-all devicetree-content zephyr-inventory-all)

#-------------------------------------------------------------------------------
# docset: kconfig

file(WRITE ${KCONFIG_BINARY_DIR}/Kconfig.soc.defconfig
     "osource \"${ZEPHYR_BASE}/soc/$(ARCH)/*/Kconfig.defconfig\"\n"
)
file(WRITE ${KCONFIG_BINARY_DIR}/Kconfig.soc
     "osource \"${ZEPHYR_BASE}/soc/$(ARCH)/*/Kconfig.soc\"\n"
)
file(WRITE ${KCONFIG_BINARY_DIR}/Kconfig.shield.defconfig
     "osource \"${ZEPHYR_BASE}/boards/shields/*/Kconfig.defconfig\"\n"
)
file(WRITE ${KCONFIG_BINARY_DIR}/Kconfig.shield
     "osource \"${ZEPHYR_BASE}/boards/shields/*/Kconfig.shield\"\n"
)
file(WRITE ${KCONFIG_BINARY_DIR}/Kconfig.soc.arch
     "osource \"${ZEPHYR_BASE}/soc/$(ARCH)/Kconfig\"\n"
     "osource \"${ZEPHYR_BASE}/soc/$(ARCH)/*/Kconfig\"\n"
)

set(GEN_KCONFIG_REST_SCRIPT ${ZEPHYR_BASE}/doc/_scripts/gen_kconfig_rest.py)

foreach(module_name ${ZEPHYR_MODULE_NAMES})
  zephyr_string(SANITIZE TOUPPER MODULE_NAME_UPPER ${module_name})
  list(APPEND
       ZEPHYR_KCONFIG_MODULES
       "ZEPHYR_${MODULE_NAME_UPPER}_MODULE_DIR=${ZEPHYR_${MODULE_NAME_UPPER}_MODULE_DIR}"
  )

  if(ZEPHYR_${MODULE_NAME_UPPER}_KCONFIG)
    list(APPEND
         ZEPHYR_KCONFIG_MODULES
         "ZEPHYR_${MODULE_NAME_UPPER}_KCONFIG=${ZEPHYR_${MODULE_NAME_UPPER}_KCONFIG}"
  )
  endif()
endforeach()

set(KCONFIG_RST_OUT ${KCONFIG_BINARY_DIR}/src)

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
      ${PYTHON_EXECUTABLE} ${GEN_KCONFIG_REST_SCRIPT} ${KCONFIG_RST_OUT}
        --separate-all-index
        --modules "Zephyr Architecture,zephyr-arch,${ZEPHYR_BASE}/arch"
                  "Zephyr SoC,zephyr-soc,${ZEPHYR_BASE}/soc"
                  "Zephyr Driver,zephyr-drivers,${ZEPHYR_BASE}/drivers"
                  "Zephyr Boards,zephyr-boards,${ZEPHYR_BASE}/boards"
                  "Zephyr Kernel,zephyr-kernel,${ZEPHYR_BASE}/kernel"
                  "Zephyr Library,zephyr-lib,${ZEPHYR_BASE}/lib"
                  "Zephyr Subsystem,zephyr-subsys,${ZEPHYR_BASE}/subsys"
                  "External Modules,modules,${ZEPHYR_BASE}/modules"
                  "Bridle,bridle,${BRIDLE_BASE}"
        --no-index-modules BuildDir,${CMAKE_BINARY_DIR}
  VERBATIM
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
  COMMENT "Running gen_kconfig_rest.py ${KCONFIG_RST_OUT}"
  USES_TERMINAL
)

set(kconfig_env
  ZEPHYR_BASE=${ZEPHYR_BASE}
  BRIDLE_BASE=${BRIDLE_BASE}
)

add_docset(kconfig "${kconfig_env}" "")
add_dependencies(kconfig-inventory kconfig-content)
add_dependencies(kconfig-inventory-all kconfig-content)
add_dependencies(kconfig-html kconfig-content zephyr-inventory)
add_dependencies(kconfig-html-all kconfig-content zephyr-inventory-all)

#-------------------------------------------------------------------------------
# docset: bridle

set(tools_version_files
    ${BRIDLE_BASE}/scripts/tools-versions-minimum.txt
    ${BRIDLE_BASE}/scripts/tools-versions-macos.txt
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

set(BRIDLE_DOC_DIR ${BRIDLE_BASE}/doc/bridle)

add_custom_command(
  OUTPUT ${BRIDLE_BINARY_DIR}/src/versions.txt
  COMMAND ${CMAKE_COMMAND}
    -DTOOLS_VERSION_FILES="${tools_files_escaped}"
    -DPIP_REQUIREMENTS_FILES="${pip_files_escaped}"
    -DVERSION_IN=${BRIDLE_DOC_DIR}/versions.txt.in
    -DVERSION_OUT=${BRIDLE_BINARY_DIR}/src/versions.txt
    -P ${BRIDLE_BASE}/doc/update_versions.cmake
  DEPENDS
    ${BRIDLE_DOC_DIR}/versions.txt.in
    ${tools_version_files}
    ${pip_requirements_files}
)

add_custom_target(
  bridle-versions
  DEPENDS
    ${BRIDLE_BINARY_DIR}/src/versions.txt
)

set(bridle_env
  ZEPHYR_BASE=${ZEPHYR_BASE}
  BRIDLE_BASE=${BRIDLE_BASE}
  BRIDLE_BUILD=${BRIDLE_BINARY_DIR}
  DOXYGEN_EXECUTABLE=${DOXYGEN_EXECUTABLE}
)

add_docset(bridle "${bridle_env}" "-j 1")
add_dependencies(bridle-html bridle-versions devicetree-inventory zephyr-inventory)
add_dependencies(bridle-html-all bridle-versions devicetree-inventory-all zephyr-inventory-all)

#-------------------------------------------------------------------------------
# Global targets

add_custom_target(
  copy-extra-content
  COMMAND ${CMAKE_COMMAND} -E make_directory ${HTML_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_LIST_DIR}/_docroot/.htaccess
    ${CMAKE_CURRENT_LIST_DIR}/_docroot/index.html
    ${BRIDLE_BASE}/doc/versions.json
    ${HTML_DIR}
)

set_target_properties(
  copy-extra-content
  PROPERTIES
    ADDITIONAL_CLEAN_FILES "${HTML_DIR}"
)

add_dependencies(zephyr-html-all kconfig-html-all devicetree-html-all)
add_dependencies(bridle-html-all zephyr-html-all kconfig-html-all devicetree-html-all)

add_custom_target(build-all ALL)
add_dependencies(build-all
    copy-extra-content
    bridle-html-all
    zephyr-html-all
    kconfig-html-all
)

add_custom_target(linkcheck)
add_dependencies(linkcheck
    bridle-linkcheck
)
