# Copyright (c) 2021-2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# This file provides Bridle Config Package functionality.
#
# The purpose of this files is to allow users to decide if they want to:
# - Use BRIDLE_BASE environment setting for explicitly
#   set select a bridle installation.
# - Support automatic Bridle installation lookup through
#   the use of find_package(Bridle).

macro(include_bridle_boilerplate location)
  set(Bridle_DIR ${BRIDLE_BASE}/share/bridle-package/cmake CACHE PATH
      "The directory containing a CMake configuration file for Bridle." FORCE
  )
  list(PREPEND CMAKE_MODULE_PATH ${BRIDLE_BASE}/cmake/modules)

  if(NOT NO_BOILERPLATE)
    list(LENGTH Bridle_FIND_COMPONENTS components_length)
    # The module messages are intentionally higher than STATUS to avoid the
    # "--" prefix and make them more visible to users. This does result in them
    # being output to stderr, but that is an implementation detail of cmake.
    if(components_length EQUAL 0)
      message(NOTICE "Loading Bridle default modules (${location}).")
      include(bridle/default NO_POLICY_SCOPE)
    else()
      list(PREPEND Bridle_FIND_COMPONENTS requirements)
      message(NOTICE "Loading Bridle module(s) (${location}): ${Bridle_FIND_COMPONENTS}")
      foreach(component ${Bridle_FIND_COMPONENTS})
        if(${component} MATCHES "^\([^:]*\):\(.*\)$")
          string(REPLACE "," ";" SUB_COMPONENTS ${CMAKE_MATCH_2})
          set(component ${CMAKE_MATCH_1})
        endif()
        include(bridle/${component})
      endforeach()
    endif()
  else()
    message(WARNING "The NO_BOILERPLATE setting has been deprecated.\n"
                    "Please use: 'find_package(Bridle COMPONENTS <components>)'"
    )
  endif()
endmacro()

# If BRIDLE_ZephyrBuildConfig is set, it means this file was include by
# ZephyrBuildConfig instead of called via find_package directly. When
# called directly, the Bridle package have to redirect back to the Zephyr
# package immediately and let it include again by ZephyrBuildConfig.
if(NOT DEFINED BRIDLE_ZephyrBuildConfig OR NOT BRIDLE_ZephyrBuildConfig)
  list(LENGTH Bridle_FIND_COMPONENTS components_length)
  if(components_length EQUAL 0)
    find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
    return()
  endif()
endif()

# First check to see if user has provided a Bridle base manually and
# it is first run (cache not set). Set Bridle base to environment setting.
# It will be empty if not set in environment.
set(ENV_BRIDLE_BASE $ENV{BRIDLE_BASE})
if((NOT DEFINED BRIDLE_BASE) AND (DEFINED ENV_BRIDLE_BASE))
  # Get rid of any double folder string before comparison, as example,
  # user provides: BRIDLE_BASE=//path/to//bridle_base/
  # must also work.
  get_filename_component(BRIDLE_BASE ${ENV_BRIDLE_BASE} ABSOLUTE)
  set(BRIDLE_BASE ${BRIDLE_BASE} CACHE PATH "Bridle base")
  include_bridle_boilerplate("Bridle base")
  return()
endif()

if(DEFINED BRIDLE_BASE)
  include_bridle_boilerplate("Bridle base (cached)")
  return()
endif()

# If BRIDLE_CANDIDATE is set, it means this file was include instead
# of called via find_package directly.
if(BRIDLE_CANDIDATE)
  set(IS_INCLUDED TRUE)
else()
  include(${CMAKE_CURRENT_LIST_DIR}/bridle_package_search.cmake)
endif()

# Find out the current Bridle base.
get_filename_component(CURRENT_BRIDLE_DIR
                       ${CMAKE_CURRENT_LIST_FILE}/${BRIDLE_RELATIVE_DIR}
                       ABSOLUTE)
get_filename_component(CURRENT_WORKSPACE_DIR
                       ${CMAKE_CURRENT_LIST_FILE}/${WORKSPACE_RELATIVE_DIR}
                       ABSOLUTE)

string(FIND "${CMAKE_CURRENT_SOURCE_DIR}"
            "${CURRENT_BRIDLE_DIR}/" COMMON_INDEX)
if(COMMON_INDEX EQUAL 0)
  # Project is in Bridle repository.
  # We are in Bridle repository.
  set(BRIDLE_BASE ${CURRENT_BRIDLE_DIR} CACHE PATH "Bridle base")
  include_bridle_boilerplate("Bridle repository")
  return()
endif()

if(IS_INCLUDED)
  # A higher level did the checking and included us and as we are not in Bridle
  # repository (checked above) then we must be in Bridle workspace.
  set(BRIDLE_BASE ${CURRENT_BRIDLE_DIR} CACHE PATH "Bridle base")
  include_bridle_boilerplate("Bridle workspace")
else()
  string(FIND "${CMAKE_CURRENT_SOURCE_DIR}"
              "${CURRENT_WORKSPACE_DIR}/" COMMON_INDEX)
  if(COMMON_INDEX EQUAL 0)
    # Project is in Bridle workspace. This means this Bridle is likely the
    # correct one, but there could be an alternative installed along-side.
    # Thus, check if there is an even better candidate. This check works the
    # following way. CMake finds packages will look all packages registered
    # in the user package registry. As this code is processed inside registered
    # packages, we simply test if another package has a common path with the
    # current sample. and if so, we will return here, and let CMake call into
    # the other registered package for real version checking.
    check_bridle_package(CURRENT_WORKSPACE_DIR ${CURRENT_WORKSPACE_DIR})

    if(BRIDLE_PREFER)
      check_bridle_package(SEARCH_PARENTS CANDIDATES_PREFERENCE_LIST
                           ${BRIDLE_PREFER})
    endif()

    # We are the best candidate, so let's include boiler plate.
    set(BRIDLE_BASE ${CURRENT_BRIDLE_DIR} CACHE PATH "Bridle base")
    include_bridle_boilerplate("Bridle workspace")
    return()
  endif()

  check_bridle_package(SEARCH_PARENTS CANDIDATES_PREFERENCE_LIST
                       ${BRIDLE_PREFER})

  # Ending here means there were no candidates in workspace of the app. Thus,
  # the app is built as a Bridle Freestanding application. CMake find_package
  # has already done the version checking, so let's just include boiler plate.
  # Previous find_package would have cleared Bridle_FOUND variable, thus set
  # it again.
  set(BRIDLE_BASE ${CURRENT_BRIDLE_DIR} CACHE PATH "Bridle base")
  include_bridle_boilerplate("Freestanding")
endif()
