# SPDX-License-Identifier: Apache-2.0
#
# Downstream FORK POINT for Zephyr's boards build module.
#
# This directory sits on CMAKE_MODULE_PATH ahead of Zephyr's own module
# directory, so zephyr_default.cmake's include(boards) resolves to THIS
# file, shadowing ${ZEPHYR_BASE}/cmake/modules/boards.cmake.
#
#   1. -DRIG target resolution: BOARD is an INDEPENDENT coordinate, and
#      its ONLY source is the invocation -- a rig names a TOPOLOGY, not a
#      board, so it has none of its own to fall back to. -DRIG without
#      -DBOARD is therefore a configure-time FATAL_ERROR — worded to name
#      whether the target was a persisted rig or a PROMOTED SHIELD (the
#      resolver's {PROMOTED} key says which), since a shield never had a
#      board axis at all while a rig merely stopped having one. The
#      resolver (scripts/list_rigs.py's query mode) is still asked for the
#      FULL, verbatim ${RIG} target string, because the rig's own
#      NAME/DIR/revision/variant are still needed downstream — only its
#      board answer stopped being consumed.
#   2. the REAL boards module, unconditionally (rig build or plain), reached
#      by absolute path — include(boards) would recurse back into this file
#      via the prepended module path.
#
# After that, this module owns the rig-specific
# board-DTS resolution mechanics that gets consumed later (shields, dts):
#
#   - _rig_resolve_board_dts(): resolve the current board target's own
#     .dts file, including hwmv2 board-EXTENSION variants.
#
#   - the hwmv2 board-EXTENSION cpp include-path fix (DTS_EXTRA_CPPFLAGS),
#     which runs for EVERY build, rig or plain.

include_guard(GLOBAL)

include(extensions)

# ---------------------------------------------------------------------------
# Step 1: -DRIG target resolution. One resolver call per configure, whose
# answer supplies the rig's NAME/DIR/revision/variant (and {PROMOTED}) to
# everything downstream. Its board answer is no longer consumed: the
# invocation is the only source of BOARD.
if(DEFINED RIG)
  list(TRANSFORM BOARD_ROOT PREPEND "--board-root=" OUTPUT_VARIABLE _rig_broot_args)
  # "--rig=${RIG}" MUST be quoted: a list promotion target legitimately
  # contains a `;`, and an UNQUOTED expansion here would list-split it into
  # several execute_process COMMAND arguments, handing list_rigs.py only
  # the first element.
  execute_process(
    COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/../../scripts/list_rigs.py
      ${_rig_broot_args} "--rig=${RIG}"
      --cmakeformat={NAME}\;{DIR}\;{BOARD}\;{REVISION}\;{VARIANT}\;{PROMOTED}
    OUTPUT_VARIABLE _rig_resolve_out
    ERROR_VARIABLE _rig_resolve_err
    RESULT_VARIABLE _rig_resolve_rv)
  if(_rig_resolve_rv)
    message(FATAL_ERROR "Rig: -DRIG=${RIG} did not resolve:\n${_rig_resolve_err}")
  endif()
  string(STRIP "${_rig_resolve_out}" _rig_resolve_out)

  # REVISION/VARIANT are the SELECTED qualifier axes -- list_rigs.py
  # already validated them against the rig's own declarations and applied
  # defaults for a bare target, so what comes back here is either
  # NOTFOUND (axis undeclared / not selected) or the concrete string every
  # fragment filename downstream is built from.
  cmake_parse_arguments(_RIG_RESOLVED "" "NAME;DIR;BOARD;REVISION;VARIANT;PROMOTED" "" ${_rig_resolve_out})
  if(_RIG_RESOLVED_REVISION STREQUAL "NOTFOUND")
    set(_RIG_RESOLVED_REVISION "")
  endif()
  if(_RIG_RESOLVED_VARIANT STREQUAL "NOTFOUND")
    set(_RIG_RESOLVED_VARIANT "")
  endif()
  # PROMOTED is the shield name when ${RIG} resolved as a promoted shield
  # rather than a persisted rig, empty otherwise -- the ONLY key this file
  # uses to tell the two apart, since DIR/BOARD are both legitimately
  # empty for either a promoted shield OR (DIR excepted) a boardless rig.
  if(_RIG_RESOLVED_PROMOTED STREQUAL "NOTFOUND")
    set(_RIG_RESOLVED_PROMOTED "")
  endif()
  # DIR is NOTFOUND for a promoted shield (no rig folder exists at all) --
  # normalized to empty the same way BOARD/REVISION/VARIANT already are,
  # even though THIS file never itself constructs a path from it (dts.cmake
  # does); left un-normalized here, "NOTFOUND" would read as a real,
  # non-empty DIR to anything checking "was the stash populated".
  if(_RIG_RESOLVED_DIR STREQUAL "NOTFOUND")
    set(_RIG_RESOLVED_DIR "")
  endif()
  # BOARD is UNCONDITIONALLY NOTFOUND now: no rig of any shape, persisted
  # or promoted, has one of its own to declare, so list_rigs.py's {BOARD}
  # key never renders anything else. Normalized to empty the same way
  # REVISION/VARIANT/DIR are above -- this file alone decides whether that
  # is fatal (below), since only THIS file knows whether -DBOARD filled in
  # for it.
  if(_RIG_RESOLVED_BOARD STREQUAL "NOTFOUND")
    set(_RIG_RESOLVED_BOARD "")
  endif()

  # BOARD is the ONLY source of a rig build's board: a rig describes a
  # topology, not a board, so the invocation supplies it.
  #
  # zephyr_check_cache(BOARD) only WARNS on a changed BOARD in an existing
  # build dir and silently REVERTS to the cached value -- that footgun is
  # not fixed here. It is not RIG-specific either: a rig build is exposed
  # to it exactly like any other Zephyr build, and nothing here
  # special-cases it.
  if(NOT DEFINED BOARD)
    if(_RIG_RESOLVED_PROMOTED)
      message(FATAL_ERROR
        "Rig: -DRIG=${RIG} names the shield '${_RIG_RESOLVED_PROMOTED}', "
        "which has no board axis of its own at all, and no -DBOARD was "
        "given -- pass -DBOARD=<name>.")
    else()
      message(FATAL_ERROR
        "Rig: -DRIG=${RIG} names a topology, not a board, and no -DBOARD "
        "was given -- a rig has no board of its own to fall back to; "
        "pass -DBOARD=<name>.")
    endif()
  endif()

  set(_rig_boards_qualifiers_desc "")
  if(_RIG_RESOLVED_REVISION)
    string(APPEND _rig_boards_qualifiers_desc " revision: ${_RIG_RESOLVED_REVISION}")
  endif()
  if(_RIG_RESOLVED_VARIANT)
    string(APPEND _rig_boards_qualifiers_desc " variant: ${_RIG_RESOLVED_VARIANT}")
  endif()
  # ${BOARD}, never ${_RIG_RESOLVED_BOARD}: the board actually being built
  # is the only one worth printing now that the invocation is its sole
  # source. _RIG_RESOLVED_BOARD is ALWAYS empty for a promoted shield (a
  # shield has no board axis), so printing it directly would render a
  # blank "board: " field for every one of them.
  if(_RIG_RESOLVED_PROMOTED)
    message(STATUS "Rig: '${_RIG_RESOLVED_NAME}' (promoted shield), board: ${BOARD}${_rig_boards_qualifiers_desc}")
  else()
    message(STATUS "Rig: ${_RIG_RESOLVED_NAME} (${_RIG_RESOLVED_DIR}/rig.yml), board: ${BOARD}${_rig_boards_qualifiers_desc}")
  endif()
endif()
# ---------------------------------------------------------------------------

# Step 2: the real boards module, unconditionally (rig build or plain).
include(${ZEPHYR_BASE}/cmake/modules/boards.cmake)

# ---------------------------------------------------------------------------
# _rig_resolve_board_dts(<out-var>): resolve the CURRENT board target's own
# .dts file. Defined here because BOTH this fork's own use just below (the
# plain-build -isystem guard) AND the dts.cmake fork (its pass-1 recipe)
# need it; a single definition means the two never duplicate zephyr's own
# board-target naming logic between them.
#
# Sets <out-var>, in the caller's scope, to the resolved absolute path, or
# to an empty string if no candidate exists in any BOARD_DIRECTORIES
# entry. Mirrors dts.cmake's own per-directory precedence (later
# directories in BOARD_DIRECTORIES win on a match, full form preferred over
# short within one directory) but does NOT reproduce its multi-SoC conflict
# diagnostics -- out of scope for a helper only ever used against
# single-SoC boards/extensions so far; callers needing a hard failure raise
# their own diagnostic.
function(_rig_resolve_board_dts out_var)
  zephyr_build_string(_rbd_board_string SHORT _rbd_board_string_short
    BOARD ${BOARD} BOARD_QUALIFIERS "${BOARD_QUALIFIERS}"
  )

  set(_rbd_board_dts)
  foreach(_rbd_dir ${BOARD_DIRECTORIES})
    if(EXISTS "${_rbd_dir}/${_rbd_board_string}.dts")
      set(_rbd_board_dts "${_rbd_dir}/${_rbd_board_string}.dts")
    elseif(EXISTS "${_rbd_dir}/${_rbd_board_string_short}.dts")
      set(_rbd_board_dts "${_rbd_dir}/${_rbd_board_string_short}.dts")
    endif()
  endforeach()

  set(${out_var} "${_rbd_board_dts}" PARENT_SCOPE)
endfunction()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# hwmv2 board-EXTENSION cpp include-path fix (data-driven -- consumes only
# this module's own outputs, zero board names/paths hardcoded here).
#
# An extension variant's own .dts (board.yml extend:, e.g.
# boards/extend/st/nucleo_f401re/nucleo_f401re_stm32f401xe_rig.dts) wants to
# #include the REAL base board's own top-level .dts -- the whole point
# of an extension over a clone: inherit upstream content instead of
# duplicating it. But the C-preprocessor include search path pre_dt.cmake
# builds only ever adds FIXED SUBPATHS of each DTS_ROOT entry (include,
# dts, ...) -- never a board directory's own root -- so a bare
# #include "nucleo_f401re.dts" from a SIBLING directory (the extension's
# own dir) cannot resolve via the ordinary search path (verified
# empirically: cmake configure fails "No such file or directory").
#
# Fix: append every OTHER BOARD_DIRECTORIES entry (at minimum the base
# board's own dir, directories[0]) as an extra -isystem to
# DTS_EXTRA_CPPFLAGS -- an EXISTING, documented dts.cmake extension point
# ("DTS_EXTRA_CPPFLAGS: extra command line options ... to the C
# preprocessor", cmake/modules/dts.cmake). This module (the fork point) runs
# for EVERY build -- rig or plain -- and runs after the real boards.cmake
# include above (BOARD_DIRECTORIES already resolved) but before dts.cmake
# (still in time for DTS_EXTRA_CPPFLAGS to be picked up), so a genuinely
# plain -b nucleo_f401re/stm32f401xe/rig build is covered too, not just a
# -DRIG one.
#
# Guarded so this is a total no-op for every OTHER build (plain, non-rig
# boards, and even a PLAIN build of an EXTENDED board's base target):
# resolve the CURRENT target's own .dts (the shared
# _rig_resolve_board_dts helper above) and act only if it lives in a
# directory OTHER than BOARD_DIRECTORIES's first entry (the base board's
# own directory -- always directories[0], per list_boards.py's
# extend_v2_boards()). A plain nucleo_f401re build's own BOARD_DIRECTORIES
# already lists the extension dir too (list_boards.py registers the
# extension against the base regardless of which qualifier/variant is
# ultimately selected) -- the length check alone would NOT distinguish it,
# hence keying on where the RESOLVED dts actually lives, not on list length.
list(LENGTH BOARD_DIRECTORIES _rig_boards_dir_count)
if(_rig_boards_dir_count GREATER 1)
  _rig_resolve_board_dts(_rig_boards_board_dts)
  if(_rig_boards_board_dts)
    get_filename_component(_rig_boards_dts_dir "${_rig_boards_board_dts}" DIRECTORY)
    list(GET BOARD_DIRECTORIES 0 _rig_boards_base_dir)
    file(REAL_PATH "${_rig_boards_dts_dir}" _rig_boards_dts_dir_real)
    file(REAL_PATH "${_rig_boards_base_dir}" _rig_boards_base_dir_real)
    if(NOT _rig_boards_dts_dir_real STREQUAL _rig_boards_base_dir_real)
      foreach(_rig_boards_dir ${BOARD_DIRECTORIES})
        file(REAL_PATH "${_rig_boards_dir}" _rig_boards_dir_real)
        if(NOT _rig_boards_dir_real STREQUAL _rig_boards_dts_dir_real)
          list(APPEND DTS_EXTRA_CPPFLAGS "-isystem" "${_rig_boards_dir}")
        endif()
      endforeach()
    endif()
  endif()
endif()
# ---------------------------------------------------------------------------
