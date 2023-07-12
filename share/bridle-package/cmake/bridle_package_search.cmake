# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# The purpose of this file is to provide search mechanism for locating
# Bridle in-work-tree package even when they are not installed into
# CMake package system:
# Linux/MacOS: ~/.cmake/packages
# Windows:     Registry database

# Relative directory of workspace project dir as seen from Bridle package file
set(WORKSPACE_RELATIVE_DIR "../../../../..")

# Relative directory of Bridle dir as seen from Bridle package file
set(BRIDLE_RELATIVE_DIR "../../../..")

# This function updates Bridle_DIR to the point to the candidate dir.
# For Bridle 3.0 and earlier, the Bridle_DIR might in some cases be
# `Bridle_DIR-NOTFOUND` or pointing to the Bridle package including the
# boilerplate code instead of the Bridle package of the included boilerplate.
# This code ensures that when Bridle releases <=3.0 is loaded, then Bridle_DIR
# will point correctly.
function(set_bridle_dir bridle_candidate)
  get_filename_component(bridle_candidate_dir "${bridle_candidate}" DIRECTORY)
  if(NOT "${bridle_candidate_dir}" STREQUAL "${Bridle_DIR}")
    set(Bridle_DIR ${bridle_candidate_dir} CACHE PATH
        "The directory containing a CMake configuration file for Bridle." FORCE
    )
  endif()
endfunction()

# This macro returns a list of parent folders to use for later searches.
macro(get_bridle_search_paths START_PATH SEARCH_PATHS PREFERENCE_LIST)
  get_filename_component(SEARCH_PATH ${START_PATH} DIRECTORY)
  while(NOT (SEARCH_PATH STREQUAL SEARCH_PATH_PREV))
    foreach(preference ${PREFERENCE_LIST})
      list(APPEND SEARCH_PATHS ${SEARCH_PATH}/${preference})
    endforeach()
    list(APPEND SEARCH_PATHS ${SEARCH_PATH}/bridle)
    list(APPEND SEARCH_PATHS ${SEARCH_PATH})
    set(SEARCH_PATH_PREV ${SEARCH_PATH})
    get_filename_component(SEARCH_PATH ${SEARCH_PATH} DIRECTORY)
  endwhile()
endmacro()

# This macro can check for additional Bridle package that has a better match
# Options:
# - BRIDLE_BASE                : Use the specified BRIDLE_BASE directly.
# - WORKSPACE_DIR              : Search for projects in specified  workspace.
# - SEARCH_PARENTS             : Search parent folder of current source file
#                                (application) to locate in-project-tree Bridle
#                                candidates.
# - CHECK_ONLY                 : Only set PACKAGE_VERSION_COMPATIBLE to false
#                                if a better candidate is found, default is to
#                                also include the found candidate.
# - VERSION_CHECK              : This is the version check stage by CMake find
#                                package.
# - CANDIDATES_PREFERENCE_LIST : List of candidate to be preferred, if installed.
macro(check_bridle_package)
  set(options CHECK_ONLY SEARCH_PARENTS VERSION_CHECK)
  set(single_args WORKSPACE_DIR BRIDLE_BASE)
  set(list_args CANDIDATES_PREFERENCE_LIST)
  cmake_parse_arguments(CHECK_BRIDLE_PACKAGE "${options}" "${single_args}"
                                             "${list_args}" ${ARGN})

  if(CHECK_BRIDLE_PACKAGE_BRIDLE_BASE)
    set(SEARCH_SETTINGS PATHS ${CHECK_BRIDLE_PACKAGE_BRIDLE_BASE}
                        NO_DEFAULT_PATH)
  endif()

  if(CHECK_BRIDLE_PACKAGE_WORKSPACE_DIR)
    set(SEARCH_SETTINGS PATHS ${CHECK_BRIDLE_PACKAGE_WORKSPACE_DIR}/bridle
                              ${CHECK_BRIDLE_PACKAGE_WORKSPACE_DIR}
                        NO_DEFAULT_PATH)
  endif()

  if(CHECK_BRIDLE_PACKAGE_SEARCH_PARENTS)
    get_bridle_search_paths(${CMAKE_CURRENT_SOURCE_DIR} SEARCH_PATHS
                            "${CHECK_BRIDLE_PACKAGE_CANDIDATES_PREFERENCE_LIST}")
    set(SEARCH_SETTINGS PATHS ${SEARCH_PATHS} NO_DEFAULT_PATH)
  endif()

  ### OFF ### # Searching for version zero means there will be no match, but we obtain
  ### OFF ### # a list of all potential Bridle candidates in the tree to consider.
  ### OFF ### find_package(Bridle 0.0.0 EXACT QUIET ${SEARCH_SETTINGS})

  # The find package will also find ourself when searching using installed
  # candidates. So avoid re-including unless NO_DEFAULT_PATH is set.
  # NO_DEFAULT_PATH means explicit search and we could be part of a
  # preference list.
  if(NOT (NO_DEFAULT_PATH IN_LIST SEARCH_SETTINGS))
    list(REMOVE_ITEM Bridle_CONSIDERED_CONFIGS
                     ${CMAKE_CURRENT_LIST_DIR}/BridleConfig.cmake)
  endif()
  list(REMOVE_DUPLICATES Bridle_CONSIDERED_CONFIGS)

  foreach(BRIDLE_CANDIDATE ${Bridle_CONSIDERED_CONFIGS})
    if(CHECK_BRIDLE_PACKAGE_WORKSPACE_DIR)
      # Check is done in Bridle workspace already,
      # thus check only for pure Bridle candidates.
      get_filename_component(CANDIDATE_DIR
                             ${BRIDLE_CANDIDATE}/${BRIDLE_RELATIVE_DIR}
                             ABSOLUTE)
    else()
      get_filename_component(CANDIDATE_DIR
                             ${BRIDLE_CANDIDATE}/${WORKSPACE_RELATIVE_DIR}
                             ABSOLUTE)
    endif()

    if(CHECK_BRIDLE_PACKAGE_BRIDLE_BASE)
        if(CHECK_BRIDLE_PACKAGE_VERSION_CHECK)
          string(REGEX REPLACE "\.cmake$" "Version.cmake"
                 BRIDLE_VERSION_CANDIDATE ${BRIDLE_CANDIDATE})
          include(${BRIDLE_VERSION_CANDIDATE} NO_POLICY_SCOPE)
          return()
        else()
          include(${BRIDLE_CANDIDATE} NO_POLICY_SCOPE)
          set_bridle_dir(${BRIDLE_CANDIDATE})
          return()
        endif()
    endif()

    string(FIND "${CMAKE_CURRENT_SOURCE_DIR}" "${CANDIDATE_DIR}/" COMMON_INDEX)
    if (COMMON_INDEX EQUAL 0)
      if(CHECK_BRIDLE_PACKAGE_CHECK_ONLY)
        # A better candidate exists, thus return
        set(PACKAGE_VERSION_COMPATIBLE FALSE)
        return()
      elseif(BRIDLE_CANDIDATE STREQUAL
             ${CMAKE_CURRENT_LIST_DIR}/BridleConfig.cmake)
        # Current Bridle is preferred one, let's just break
        # the loop and continue processing.
        break()
      else()
        if(CHECK_BRIDLE_PACKAGE_VERSION_CHECK)
          string(REGEX REPLACE "\.cmake$" "Version.cmake"
                 BRIDLE_VERSION_CANDIDATE ${BRIDLE_CANDIDATE})
          include(${BRIDLE_VERSION_CANDIDATE} NO_POLICY_SCOPE)
          return()
	else()
          include(${BRIDLE_CANDIDATE} NO_POLICY_SCOPE)
          set_bridle_dir(${BRIDLE_CANDIDATE})
	  return()
        endif()
      endif()
    endif()
  endforeach()
endmacro()
