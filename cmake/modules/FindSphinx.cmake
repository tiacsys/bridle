# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: BSD-3-Clause

# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

#[=======================================================================[.rst:
FindSphinx
----------

Sphinx is a documentation generation tool (see http://www.sphinx-doc.org).
This module looks for ``sphinx-build`` and some optional tools it supports:

``quickstart``
  `Sphinx Quickstart <https://www.sphinx-doc.org/en/master/man/sphinx-quickstart.html>`_
  ``sphinx-quickstart`` is an interactive tool that asks some questions about
  your project and then generates a complete documentation directory and sample
  Makefile to be used with ``sphinx-build``.

``autogen``
  `Sphinx RST Generator <https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html>`_
  ``sphinx-autogen`` is a tool for automatic generation of Sphinx sources that,
  using the **autodoc** extension, document items included in **autosummary**
  listing(s).

``apidoc``
  `Sphinx API Documentation <https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html>`_
  ``sphinx-apidoc`` is a tool for automatic generation of Sphinx sources that,
  using the **autodoc** extension, document a whole package in the style of
  other automatic API documentation tools.

  These tools are available as components in the :command:`find_package`
  command. For example:

.. code-block:: cmake

  # Require quickstart, treat the other components as optional
  find_package(Sphinx
               REQUIRED quickstart
               OPTIONAL_COMPONENTS autogen apidoc)

The following variables are defined by this module:

.. variable:: SHPHINX_FOUND

  True if the ``sphinx-build`` executable was found.

.. variable:: SPHINX_VERSION

  The version reported by ``sphinx-build --version``.

  The module defines ``IMPORTED`` targets for Sphinx and each component found.
  These can be used as part of custom commands, etc. and should be preferred over
  old-style (and now deprecated) variables like ``SPHINX_BUILD_EXECUTABLE``. The
  following import targets are defined if their corresponding executable could be
  found (the component import targets will only be defined if that component was
  requested):

::

  Sphinx::build
  Sphinx::quickstart
  Sphinx::autogen
  Sphinx::apidoc


Functions
^^^^^^^^^

.. command:: sphinx_add_docs

   .. todo:: not (yet) implemented


Deprecated Result Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. deprecated:: 3.9

For compatibility with previous versions of CMake, the following variables
are also defined but they are deprecated and should no longer be used:

.. variable:: SPHINX_BUILD_EXECUTABLE

  The path to the ``sphinx-build`` command. If projects need to refer to the
  ``sphinx-build`` executable directly, they should use the ``Sphinx::build``
  import target instead.

.. variable:: SPHINX_QUICKSTART_FOUND

  True if the ``sphinx-quickstart`` executable was found.

.. variable:: SPHINX_QUICKSTART_EXECUTABLE

  The path to the ``sphinx-quickstart`` command. If projects need to refer
  to the ``sphinx-quickstart`` executable directly, they should use the
  ``Sphinx::quickstart`` import target instead.

.. variable:: SPHINX_QUICKSTART_PATH

  The path to the directory containing the ``sphinx-quickstart``
  executable as reported in ``SPHINX_QUICKSTART_EXECUTABLE``. The
  path may have forward slashes even on Windows and is not suitable
  for direct substitution into a ``conf.py.in`` template. If you need
  this value, get the :prop_tgt:`IMPORTED_LOCATION` property of the
  ``Sphinx::quickstart`` target and use :command:`get_filename_component`
  to extract the directory part of that path. You may also want to
  consider using :command:`file(TO_NATIVE_PATH)` to prepare the path
  for a Sphinx configuration file.


Deprecated Hint Variables
^^^^^^^^^^^^^^^^^^^^^^^^^

.. deprecated:: 3.9

.. variable:: SPHINX_SKIP_QUICKSTART

  This variable has no effect for the component form of ``find_package``.
  In backward compatibility mode (i.e. without components list) it prevents
  the finder module from searching for Sphinx's ``sphinx-quickstart`` utility.

#]=======================================================================]

cmake_policy(PUSH)
cmake_policy(SET CMP0054 NEW) # quoted if arguments
cmake_policy(SET CMP0057 NEW) # if IN_LIST

# For backwards compatibility support
if(Sphinx_FIND_QUIETLY)
    set(SPHINX_FIND_QUIETLY TRUE)
endif()

#
# Find Sphinx...
#
macro(_Sphinx_find_build)
    find_program(
        SPHINX_BUILD_EXECUTABLE
        NAMES sphinx-build
        DOC "Sphinx documentation generation tool (http://www.sphinx-doc.org)"
    )
    mark_as_advanced(SPHINX_BUILD_EXECUTABLE)

    if(SPHINX_BUILD_EXECUTABLE)
        execute_process(
            COMMAND "${SPHINX_BUILD_EXECUTABLE}" --version
            OUTPUT_VARIABLE SPHINX_VERSION
            OUTPUT_STRIP_TRAILING_WHITESPACE
            RESULT_VARIABLE _Sphinx_version_result
        )
        if(_Sphinx_version_result)
            message(WARNING "Unable to determine Sphinx version: ${_Sphinx_version_result}")
        else()
          string(STRIP "${SPHINX_VERSION}" SPHINX_VERSION)
          string(REGEX MATCH "[0-9]+\\.[0-9]+\\.[0-9]+" SPHINX_VERSION "${SPHINX_VERSION}")
        endif()

        # Create an imported target for Sphinx
        if(NOT TARGET Sphinx::build)
            add_executable(Sphinx::build IMPORTED GLOBAL)
            set_target_properties(Sphinx::build PROPERTIES
                IMPORTED_LOCATION "${SPHINX_BUILD_EXECUTABLE}"
            )
        endif()
    endif()
endmacro()

#
# Find Quickstart...
#
macro(_Sphinx_find_quickstart)
    set(_x86 "(x86)")
    find_program(
        SPHINX_QUICKSTART_EXECUTABLE
        NAMES sphinx-quickstart
        DOC "Quickstart tool for use with Sphinx"
    )
    mark_as_advanced(SPHINX_QUICKSTART_EXECUTABLE)

    if(SPHINX_QUICKSTART_EXECUTABLE)
        # If one wants the path to the utility, not the entire path
        # including file name
        get_filename_component(SPHINX_QUICKSTART_PATH
                              "${SPHINX_QUICKSTART_EXECUTABLE}"
                              DIRECTORY)
        if(WIN32)
            file(TO_NATIVE_PATH "${SPHINX_QUICKSTART_PATH}" SPHINX_QUICKSTART_PATH)
        endif()

        # Create an imported target for component
        if(NOT TARGET Sphinx::quickstart)
            add_executable(Sphinx::quickstart IMPORTED GLOBAL)
            set_target_properties(Sphinx::quickstart PROPERTIES
                IMPORTED_LOCATION "${SPHINX_QUICKSTART_EXECUTABLE}"
            )
        endif()
    endif()

    unset(_x86)
endmacro()

#
# Find RST Generator...
#
macro(_Sphinx_find_autogen)
    set(_x86 "(x86)")
    find_program(
        SPHINX_AUTOGEN_EXECUTABLE
        NAMES sphinx-autogen
        DOC "RST Generator tool for use with Sphinx"
    )
    mark_as_advanced(SPHINX_AUTOGEN_EXECUTABLE)

    if(SPHINX_AUTOGEN_EXECUTABLE)
        # If one wants the path to the utility, not the entire path
        # including file name
        get_filename_component(SPHINX_AUTOGEN_PATH
                              "${SPHINX_AUTOGEN_EXECUTABLE}"
                              DIRECTORY)
        if(WIN32)
            file(TO_NATIVE_PATH "${SPHINX_AUTOGEN_PATH}" SPHINX_AUTOGEN_PATH)
        endif()

        # Create an imported target for component
        if(NOT TARGET Sphinx::autogen)
            add_executable(Sphinx::autogen IMPORTED GLOBAL)
            set_target_properties(Sphinx::autogen PROPERTIES
                IMPORTED_LOCATION "${SPHINX_AUTOGEN_EXECUTABLE}"
            )
        endif()
    endif()

    unset(_x86)
endmacro()

#
# Find API Documentation Generator...
#
macro(_Sphinx_find_apidoc)
    set(_x86 "(x86)")
    find_program(
        SPHINX_APIDOC_EXECUTABLE
        NAMES sphinx-apidoc
        DOC "API Documentation Generator tool for use with Sphinx"
    )
    mark_as_advanced(SPHINX_APIDOC_EXECUTABLE)

    if(SPHINX_APIDOC_EXECUTABLE)
        # If one wants the path to the utility, not the entire path
        # including file name
        get_filename_component(SPHINX_APIDOC_PATH
                              "${SPHINX_APIDOC_EXECUTABLE}"
                              DIRECTORY)
        if(WIN32)
            file(TO_NATIVE_PATH "${SPHINX_APIDOC_PATH}" SPHINX_APIDOC_PATH)
        endif()

        # Create an imported target for component
        if(NOT TARGET Sphinx::apidoc)
            add_executable(Sphinx::apidoc IMPORTED GLOBAL)
            set_target_properties(Sphinx::apidoc PROPERTIES
                IMPORTED_LOCATION "${SPHINX_APIDOC_EXECUTABLE}"
            )
        endif()
    endif()

    unset(_x86)
endmacro()

# Make sure `build` is one of the components to find
set(_Sphinx_keep_backward_compat FALSE)
if(NOT Sphinx_FIND_COMPONENTS)
    # Search at least for `build` executable
    set(Sphinx_FIND_COMPONENTS build)
    # Preserve backward compatibility:
    # search for `quickstart` also if `SPHINX_SKIP_QUICKSTART`
    # is not explicitly disable this.
    if(NOT SPHINX_SKIP_QUICKSTART)
        list(APPEND Sphinx_FIND_COMPONENTS quickstart)
    endif()
    set(_Sphinx_keep_backward_compat TRUE)
elseif(NOT build IN_LIST Sphinx_FIND_COMPONENTS)
    list(INSERT Sphinx_FIND_COMPONENTS 0 build)
endif()

#
# Find all requested components of Sphinx...
#
foreach(_comp IN LISTS Sphinx_FIND_COMPONENTS)
    if(_comp STREQUAL "build")
        _Sphinx_find_build()
    elseif(_comp STREQUAL "quickstart")
        _Sphinx_find_quickstart()
    elseif(_comp STREQUAL "autogen")
        _Sphinx_find_autogen()
    elseif(_comp STREQUAL "apidoc")
        _Sphinx_find_apidoc()
    else()
        message(WARNING "${_comp} is not a valid Sphinx component")
        set(Sphinx_${_comp}_FOUND FALSE)
        continue()
    endif()

    if(TARGET Sphinx::${_comp})
        set(Sphinx_${_comp}_FOUND TRUE)
    else()
        set(Sphinx_${_comp}_FOUND FALSE)
    endif()
endforeach()
unset(_comp)

# Verify find results
#include(${CMAKE_CURRENT_LIST_DIR}/FindPackageHandleStandardArgs.cmake)
find_package(PackageHandleStandardArgs MODULE REQUIRED)
find_package_handle_standard_args(
    Sphinx
    REQUIRED_VARS SPHINX_BUILD_EXECUTABLE
    VERSION_VAR SPHINX_VERSION
    HANDLE_COMPONENTS
)

# Maintain the _FOUND variables as "YES" or "NO" for backwards
# compatibility.
if(SHPHINX_FOUND)
    set(SHPHINX_FOUND "YES")
else()
    set(SHPHINX_FOUND "NO")
endif()
if(_Sphinx_keep_backward_compat)
    if(Sphinx_quickstart_FOUND)
        set(SPHINX_QUICKSTART_FOUND "YES")
    else()
        set(SPHINX_QUICKSTART_FOUND "NO")
    endif()

    # For backwards compatibility support for even older CMake versions
    set(SPHINX_BUILD ${SPHINX_BUILD_EXECUTABLE})
    set(SPHINX_QUICKSTART ${SPHINX_QUICKSTART_EXECUTABLE})

    # No need to keep any backward compatibility for `SPHINX_AUTOGEN_XXX`
    # and `SPHINX_APIDOC_XXX` since they were not supported before component
    # support was added
endif()
unset(_Sphinx_keep_backward_compat)

#
# Allow full control of Sphinx from CMakeLists.txt
#

# Prepare a template conf.py and Sphinx's default values CMake file
if(TARGET Sphinx::quickstart)
    message(AUTHOR_WARNING "TODO: sphinx_add_docs() not yet implemented. (${CMAKE_MESSAGE_LOG_LEVEL})")
    # If sphinx-quickstart was found, use it to generate a minimal default
    # conf.py. We will delete this file after we have finished using it below
    # to generate the other files that sphinx_add_docs() will use.
endif()

cmake_policy(POP)
