# Copyright (c) 2021-2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# This file provides Bridle Config Package version information.
#
# The purpose of the version file is to ensure that CMake find_package can
# correctly locate a usable Bridle installation for building of applications.

# Checking for version 0.0.0 is a way to allow other Bridle installation to
# determine if there is a better match. A better match would be an installed
# Bridle that has a common index with current source dir. Version 0.0.0
# indicates that we should just return, in order to obtain our path.
if(0.0.0 STREQUAL PACKAGE_FIND_VERSION)
  return()
endif()

macro(check_bridle_version)
  if(PACKAGE_VERSION VERSION_LESS PACKAGE_FIND_VERSION)
    if(IS_INCLUDED)
      # We are just a candidate, meaning we have been included from other
      # installed module.
      message("\n  The following Bridle repository configuration file were considered but not accepted:")
      message("\n    ${CMAKE_CURRENT_LIST_FILE}, version: ${PACKAGE_VERSION}\n")
    endif()

    set(PACKAGE_VERSION_COMPATIBLE FALSE)
  else()
    # For now, Bridle is capable to find the right base on all older versions
    # as long as they define a Bridle config package (This code). In future,
    # this is the place to update in case Bridle 3.x is not backward compatible
    # with version 2.x.
    set(PACKAGE_VERSION_COMPATIBLE TRUE)
    if(PACKAGE_FIND_VERSION STREQUAL PACKAGE_VERSION)
      set(PACKAGE_VERSION_EXACT TRUE)
    endif()
  endif()
endmacro()

# First check to see if user has provided a Bridle base manually and
# it is first run (cache not set). Set Bridle base to environment setting.
# It will be empty if not set in environment.
set(ENV_BRIDLE_BASE $ENV{BRIDLE_BASE})
if((NOT DEFINED BRIDLE_BASE) AND (DEFINED ENV_BRIDLE_BASE))
  # Get rid of any double folder string before comparison, as example,
  # user provides: BRIDLE_BASE=//path/to//bridle_base/
  # must also work.
  get_filename_component(BRIDLE_BASE $ENV{BRIDLE_BASE} ABSOLUTE)
endif()

# If BRIDLE_CANDIDATE is set, it means this file was include instead
# of called via find_package directly.
if(BRIDLE_CANDIDATE)
  set(IS_INCLUDED TRUE)
else()
  include(${CMAKE_CURRENT_LIST_DIR}/bridle_package_search.cmake)
endif()

if((DEFINED BRIDLE_BASE) OR (DEFINED ENV_BRIDLE_BASE))
  # BRIDLE_BASE was set in cache from earlier run or in environment (first run),
  # meaning the package version must be ignored and the Bridle pointed to by
  # BRIDLE_BASE is to be used regardless of version.
  if(${BRIDLE_BASE}/share/bridle-package/cmake STREQUAL ${CMAKE_CURRENT_LIST_DIR})
    # We are the Bridle to be used

    set(NO_PRINT_VERSION True)
    include(${BRIDLE_BASE}/cmake/modules/bridle/version.cmake)
    # Bridle uses project version, but CMake package uses PACKAGE_VERSION
    set(PACKAGE_VERSION ${PROJECT_VERSION})
    check_bridle_version()

    if(IS_INCLUDED)
      # We are included, so we need to ensure that the version of the top-level
      # package file is returned. This Bridle version has already been printed
      # as part of `check_bridle_version()`
      if(NOT ${PACKAGE_VERSION_COMPATIBLE}
        OR (Bridle_FIND_VERSION_EXACT AND NOT PACKAGE_VERSION_EXACT)
      )
        # When Bridle base is set and we are checked as an included file
        # (IS_INCLUDED=True), then we are unable to retrieve the version of the
        # parent Bridle, therefore just mark it as ignored.
        set(PACKAGE_VERSION "ignored (BRIDLE_BASE is set)")
      endif()
    endif()
  elseif((NOT IS_INCLUDED) AND (DEFINED BRIDLE_BASE))
    check_bridle_package(BRIDLE_BASE ${BRIDLE_BASE} VERSION_CHECK)
  else()
    # User has pointed to a different Bridle installation, so don't use this version
    set(PACKAGE_VERSION_COMPATIBLE FALSE)
  endif()
  return()
endif()

# Find out the current Bridle base.
get_filename_component(CURRENT_BRIDLE_DIR
                       ${CMAKE_CURRENT_LIST_FILE}/${BRIDLE_RELATIVE_DIR}
                       ABSOLUTE)
get_filename_component(CURRENT_WORKSPACE_DIR
                       ${CMAKE_CURRENT_LIST_FILE}/${WORKSPACE_RELATIVE_DIR}
                       ABSOLUTE)

# Temporary, set local Bridle base to allow using bridle/version.cmake to find
# this Bridle's repository current version.
set(BRIDLE_BASE ${CURRENT_BRIDLE_DIR})

# Temporary set local Zephyr base to allow using Zephyr's cmake extensions.
if(NOT DEFINED ZEPHYR_BASE)
  set(ZEPHYR_BASE ${CURRENT_WORKSPACE_DIR}/zephyr)
endif()

# Tell bridle/version.cmake to not print as printing version for all Bridle
# installations being tested will lead to confusion on which is being used.
set(NO_PRINT_VERSION True)
include(${BRIDLE_BASE}/cmake/modules/bridle/version.cmake)
# Bridle uses project version, but CMake package uses PACKAGE_VERSION
set(PACKAGE_VERSION ${PROJECT_VERSION})
set(BRIDLE_BASE)
if(DEFINED ZEPHYR_BASE)
  unset(ZEPHYR_BASE)
endif()

# Do we share common index, if so, this is the correct version to check.
string(FIND "${CMAKE_CURRENT_SOURCE_DIR}" "${CURRENT_BRIDLE_DIR}/" COMMON_INDEX)
if(COMMON_INDEX EQUAL 0)
  # Project is a Bridle repository app.
  check_bridle_version()
  return()
endif()

if(NOT IS_INCLUDED)
  # Only do this if we are an installed CMake Config package and checking
  # for workspace candidates.
  string(FIND "${CMAKE_CURRENT_SOURCE_DIR}" "${CURRENT_WORKSPACE_DIR}/" COMMON_INDEX)
  if(COMMON_INDEX EQUAL 0)
    # Project is a Bridle workspace app. This means this Bridle is likely
    # the correct one, but there could be an alternative installed along-side.
    # Thus, check if there is an even better candidate.
    check_bridle_package(CURRENT_WORKSPACE_DIR ${CURRENT_WORKSPACE_DIR} VERSION_CHECK)

    # We are the best candidate, so let's check our own version.
    check_bridle_version()
    return()
  endif()

  # Checking for installed candidates which could also be an workspace
  # candidates. This check works the following way. CMake finds packages
  # will look all packages registered in the user package registry. As this
  # code is processed inside registered packages, we simply test if another
  # package has a common path with the current sample, and if so, we will
  # return here, and let CMake call into the other registered package for
  # real version checking.
  check_bridle_package(CHECK_ONLY VERSION_CHECK)

  # Check for workspace candidates.
  check_bridle_package(SEARCH_PARENTS VERSION_CHECK)
endif()

# Ending here means there were no candidates in workspace of the app. Thus,
# the app is built as a Bridle Freestanding application. Let's do basic
# CMake version checking.
check_bridle_version()
