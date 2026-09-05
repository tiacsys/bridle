# SPDX-License-Identifier: Apache-2.0
#
# Downstream FORK POINT for Zephyr's dts build module.
#
# This directory sits on CMAKE_MODULE_PATH ahead of Zephyr's own module
# directory, so zephyr_default.cmake's include(dts) resolves to THIS file,
# shadowing ${ZEPHYR_BASE}/cmake/modules/dts.cmake.
#
# Plain build (no -DRIG): defer to the ORIGINAL dts.cmake unchanged, so
# every other build behaves exactly as upstream.
#
# Rig build (-DRIG set): this is where the whole rig story lives — expand
# the rig into a devicetree overlay (+ Kconfig fragment), resolve the
# shields it instantiated, and hand both off to the REAL dts.cmake, which
# this file includes as its own last act (zephyr_default.cmake then calls
# the real module's own dts_init, as usual — this fork never wraps
# anything in a function, since dts.cmake/kconfig.cmake read the variables
# steps 5-7 below set from FILE scope).
#
# Nine steps, in order:
#   1. include(pre_dt)         -- the real one, first run (SHIELD_DIRS still
#                                  empty; harmless, see step 6)
#   2. pass-1 recipe           -- --include-dir/--bindings-dir args from the
#                                  REAL DTS_ROOT / DTS_ROOT_SYSTEM_INCLUDE_DIRS
#                                  (step 1's output) + BOARD_DIRECTORIES;
#                                  board dts via _rig_resolve_board_dts()
#                                  (boards.cmake fork)
#   3. run rigc                -- rig->folder + qualifier-axis resolution,
#                                  OR a promoted shield (which has no folder
#                                  at all), reuses the boards.cmake fork's
#                                  _RIG_RESOLVED_DIR/REVISION/VARIANT/PROMOTED
#                                  stash, avoiding a second resolution of the
#                                  same target; falls back to its own
#                                  list_rigs.py --rig= run if that stash is
#                                  absent), VERBOSE render, rerun-expand.sh,
#                                  RIGC_COMMAND knob, error reporting
#   4. context.cmake handoff   -- RIG_NAME/RIG_BOARD/RIG_SHIELDS/
#                                  RIG_REVISION/RIG_VARIANT, RIG_DEPENDS +
#                                  static CMAKE_CONFIGURE_DEPENDS
#   5. shield resolution       -- list_shields discovery, rig-template-marker
#                                  collision preference, SHIELD_DIRS,
#                                  pre_dt_shield.cmake includes,
#                                  shield_conf_files, SHIELD_AS_LIST
#   6. pre_dt_module_run()     -- SECOND run, now with SHIELD_DIRS known:
#                                  recomputes DTS_ROOT / DTS_ROOT_SYSTEM_
#                                  INCLUDE_DIRS for pass 2 (shield bindings
#                                  included)
#   7. overlay/conf handoff    -- prepend to EXTRA_DTC_OVERLAY_FILE; APPEND
#                                  to shield_conf_files (see the asymmetry
#                                  note at step 7 below); collects the
#                                  per-variant/-revision fragments too, base
#                                  -> variant -> revision (no delta
#                                  engine yet -- .overlay/_defconfig only)
#   8. build_info provenance   -- + the selected revision/variant and the
#                                  applied fragment list
#   9. include(real dts.cmake) -- LAST line

include_guard(GLOBAL)

include(extensions)
include(python)

if(NOT DEFINED RIG)
  include(${ZEPHYR_BASE}/cmake/modules/dts.cmake)
  return()
endif()

# ===========================================================================
# Rig build: everything below runs at FILE scope (zephyr_default's include
# scope) -- never wrap this in a function; steps 5-7 set variables
# (shield_conf_files, SHIELD_AS_LIST, EXTRA_*) that dts.cmake/kconfig.cmake
# read from that scope.
# ===========================================================================

# _RIG_MODULE_ROOT is this module's own repository root
# (cmake/modules/../.. == the repository root).
get_filename_component(_RIG_MODULE_ROOT "${CMAKE_CURRENT_LIST_DIR}/../.." ABSOLUTE)

# ---------------------------------------------------------------------------
# Debuggability: render a command line copy-pasteably into a shell (zsh/bash),
# for message(VERBOSE ...) below and for rerun-expand.sh. Activate VERBOSE
# output with west build ... -- -DRIG=<name> -DCMAKE_MESSAGE_LOG_LEVEL=VERBOSE
# (reuses CMake's own log-level machinery — no new flag of our own).
#
# _rig_shell_quote_token: one argument, quoted ONLY if it actually needs
# it -- a bareword (letters/digits/`_@%+=:,./-`) renders as-is; anything
# else gets POSIX '...'-quoting (safe for ANY content, including spaces/
# globs/embedded quotes; an embedded ' becomes '\''). The safe set mirrors
# Python's own shlex.quote, so a rendered line reads the way a human would
# type it -- quotes only around the one argument that actually needs them,
# not wrapped around every argument on the line.
function(_rig_shell_quote_token out_var token)
  if("${token}" STREQUAL "" OR "${token}" MATCHES "[^A-Za-z0-9_@%+=:,./-]")
    string(REPLACE "'" "'\\''" _rig_tok_esc "${token}")
    set(${out_var} "'${_rig_tok_esc}'" PARENT_SCOPE)
  else()
    set(${out_var} "${token}" PARENT_SCOPE)
  endif()
endfunction()

# _rig_shell_quote_argv: renders a whole argv, each token quoted only as
# needed (see _rig_shell_quote_token) -- for plain positional arguments.
function(_rig_shell_quote_argv out_var)
  set(_rig_rendered "")
  foreach(_rig_tok ${ARGN})
    _rig_shell_quote_token(_rig_tok_render "${_rig_tok}")
    string(APPEND _rig_rendered "${_rig_tok_render} ")
  endforeach()
  string(STRIP "${_rig_rendered}" _rig_rendered)
  set(${out_var} "${_rig_rendered}" PARENT_SCOPE)
endfunction()

# _rig_shell_quote_env: renders a list of "NAME=value" strings as
# NAME=value, the value quoted only as needed (see _rig_shell_quote_token)
# and NAME always left bare — a shell only recognizes NAME=value as an
# env-assignment prefix when NAME itself is UNQUOTED (verified: quoting
# the whole token, e.g. 'NAME=value', makes both bash and zsh treat it as
# the command to run, not an assignment).
function(_rig_shell_quote_env out_var)
  set(_rig_rendered "")
  foreach(_rig_pair ${ARGN})
    string(FIND "${_rig_pair}" "=" _rig_eq_pos)
    string(SUBSTRING "${_rig_pair}" 0 ${_rig_eq_pos} _rig_name)
    math(EXPR _rig_val_start "${_rig_eq_pos} + 1")
    string(SUBSTRING "${_rig_pair}" ${_rig_val_start} -1 _rig_value)
    _rig_shell_quote_token(_rig_value_render "${_rig_value}")
    string(APPEND _rig_rendered "${_rig_name}=${_rig_value_render} ")
  endforeach()
  string(STRIP "${_rig_rendered}" _rig_rendered)
  set(${out_var} "${_rig_rendered}" PARENT_SCOPE)
endfunction()
# ---------------------------------------------------------------------------

# Overrideable knobs (a probe/test can substitute a stub via RIGC_COMMAND).
# The interpreter is NOT a knob: we use Zephyr's PYTHON_EXECUTABLE (set by the
# python module included above, and already used for list_rigs.py below) so
# the RIGC_COMPILE CLI runs in the same venv as the rest of the build — no
# hardcoded path. RIGC_PYTHONPATH is module-relative (derived from
# _RIG_MODULE_ROOT, this module's own tree — that is the location of OUR
# mechanics, the package RIGC_COMPILE names below, which is
# legitimately ours). The shield LIBRARY, by contrast, is discoverable
# CONTENT, not mechanics: rig shield templates may live in any board_root of
# any Zephyr module (a repository may ship some as default content, but that
# must not be hardcoded as THE source). So it is derived from BOARD_ROOT
# below, exactly as list_shields.py discovers shields — not a fixed knob.
#
# RIGC_COMPILE: the Python module name of the CLI this fork invokes
# (`python -m <this> expand ...`) -- rigc by default, and the only such CLI
# this fork ships; the knob exists as cheap insurance for a future
# re-implementation under a different module name, without editing every
# call site here. Precedence: an explicit -D wins; else $ENV{RIGC_COMPILE}
# (same name as the test-side constant, so a subprocess that merely inherits
# the invoking pytest process's environment — as most of this suite's
# build-marked tests do — still reaches this cache default without having to
# thread an explicit -D at every call site); else the "rigc" default.
# RIGC_COMMAND (below) stays the whole-command override and keeps its
# own, separate precedence over BOTH of these.
if(DEFINED RIGC_COMPILE)
  set(_rig_expand_compile_default "${RIGC_COMPILE}")
elseif(DEFINED ENV{RIGC_COMPILE})
  set(_rig_expand_compile_default "$ENV{RIGC_COMPILE}")
else()
  set(_rig_expand_compile_default "rigc")
endif()
set(RIGC_COMPILE "${_rig_expand_compile_default}"
  CACHE STRING "Python module name of the rigc CLI (python -m <this> expand ...); also names the source tree CMAKE_CONFIGURE_DEPENDS globs to retrigger configure on edit")
set(RIGC_PYTHONPATH "${_RIG_MODULE_ROOT}/scripts"
  CACHE PATH "PYTHONPATH so 'python -m ${RIGC_COMPILE}' finds this repository's scripts/${RIGC_COMPILE}")
set(RIGC_COMMAND ""
  CACHE STRING "Override: full command (semicolon list) to run instead of the ${RIGC_COMPILE} CLI")

# ---------------------------------------------------------------------------
# Step 1: pre_dt, first run. include(pre_dt) resolves to the real
# ${ZEPHYR_BASE}/cmake/modules/pre_dt.cmake (no fork of it exists — its
# global include_guard trips here, the FIRST time it is ever included in
# this configure) and, per its own file-scope pre_dt_module_run() call,
# folds APPLICATION_SOURCE_DIR/BOARD_DIR/SHIELD_DIRS/ZEPHYR_BASE into
# DTS_ROOT and derives DTS_ROOT_SYSTEM_INCLUDE_DIRS
include(pre_dt)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 2: pass-1 recipe. The board .dts + the cpp include dirs / edtlib
# bindings dirs rigc's OWN edtlib.EDT needs to read the REAL board
# devicetree (boarddt.py / board_edt.py / edt_build.py) -- derived directly
# from step 1's real DTS_ROOT / DTS_ROOT_SYSTEM_INCLUDE_DIRS, no hand-rolled
# mirror: this fork runs AFTER hwm_v2, so ARCH_V2_NAME_LIST is set and
# pre_dt's own computation is already correct for pass 1.
#
set(_rig_include_dir_args)
foreach(_rig_dts_dir ${DTS_ROOT_SYSTEM_INCLUDE_DIRS})
  list(APPEND _rig_include_dir_args --include-dir "${_rig_dts_dir}")
endforeach()
# BOARD_DIRECTORIES themselves (not just the fixed subpaths pre_dt.cmake
# derives, mirrored into DTS_ROOT_SYSTEM_INCLUDE_DIRS above) so an hwmv2
# board EXTENSION variant's own dts (which lives in a DIFFERENT directory
# than the base board it #includes) can resolve that quoted include via
# the ordinary cpp search-path fallback. A no-op for a plain, unextended board
# (BOARD_DIRECTORIES == [BOARD_DIR], already covered by
# DTS_ROOT_SYSTEM_INCLUDE_DIRS's own BOARD_DIR entry).
foreach(_rig_bdir ${BOARD_DIRECTORIES})
  list(APPEND _rig_include_dir_args --include-dir "${_rig_bdir}")
endforeach()

# Bindings dirs: the same <dts_root>/dts/bindings rule dts.cmake's own
# dts_configuration_files() uses to derive DTS_ROOT_BINDINGS (that function
# does not run until step 9, so it is not available here).
set(_rig_bindings_dir_args)
foreach(_rig_dts_root_dir ${DTS_ROOT})
  if(EXISTS "${_rig_dts_root_dir}/dts/bindings")
    list(APPEND _rig_bindings_dir_args --bindings-dir "${_rig_dts_root_dir}/dts/bindings")
  endif()
endforeach()

# Connector-type dirs: the SAME <dts_root>/dts/bindings/connectors rule
# registry.py's own BINDINGS default encodes, but threaded explicitly here
# rather than left to that fallback. The connector-type registry
# (registry.load_types, consulted by loader/shields.py's plug-matching) is
# a DIFFERENT consumer from edtlib's own bindings scan above: a connector
# type's unified binding is INSIDE a threaded --bindings-dir, so edtlib
# can schema-validate a real board's socket node against it, but that
# does not make the type itself visible to rigc's own registry, which
# never runs through edtlib at all (registry.py reads the same YAML files
# with a plain yaml.safe_load). Without --connector-dir here, the registry
# silently falls back to its own module-root-relative default
# (registry.BINDINGS = MODULE_ROOT/dts/bindings/connectors) -- MODULE_ROOT
# being wherever rigc's OWN source happens to live, not this DTS_ROOT.
# That default is correct only by coincidence, for as long as rigc's
# source and the real connector types share one repository; every rig
# build would otherwise fail with an "unknown connector type"
# (lang-shield-type) diagnostic that names no missing --connector-dir at
# all, far from this actual cause.
set(_rig_connector_dir_args)
foreach(_rig_dts_root_dir ${DTS_ROOT})
  if(EXISTS "${_rig_dts_root_dir}/dts/bindings/connectors")
    list(APPEND _rig_connector_dir_args --connector-dir "${_rig_dts_root_dir}/dts/bindings/connectors")
  endif()
endforeach()

# Load the board's own devicetree
_rig_resolve_board_dts(_rig_board_dts)

if(NOT _rig_board_dts)
  message(FATAL_ERROR
    "Rig: could not locate a board .dts for BOARD=${BOARD} "
    "BOARD_QUALIFIERS=${BOARD_QUALIFIERS} in any of: ${BOARD_DIRECTORIES}")
endif()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 3: run rigc.

# Resolve -DRIG=<target> to a rig folder + its SELECTED qualifier axes
# (@rev/variant, or the declared defaults for a bare target) -- OR to a
# PROMOTED SHIELD, which has no folder at all. THE TRAP: every fragment
# filename built below derives from _rig_name/_rig_revision/_rig_variant,
# NEVER from ${RIG} itself, which genuinely carries "name@rev/variant" —
# using it directly would silently look for the wrong (nonexistent)
# fragment files.
#
# Fall back to a fresh list_rigs.py --rig= resolution only if the
# boards.cmake fork's stash is absent — e.g. a standalone SUB_COMPONENTS
# configure that reaches dts without ever loading boards. Same resolver,
# same --cmakeformat keys as boards.cmake's Step 1: this file must never
# re-derive rig->folder/axis resolution by hand (design rule 1).
#
# _RIG_RESOLVED_NAME (never _RIG_RESOLVED_DIR) is the "did the stash
# actually run" sentinel: DIR is now legitimately EMPTY for a promoted
# shield even though the stash DID run, whereas NAME is always a real,
# non-empty string for either outcome of a successful resolution.
if(DEFINED _RIG_RESOLVED_NAME)
  set(_rig_dir "${_RIG_RESOLVED_DIR}")
  set(_rig_name "${_RIG_RESOLVED_NAME}")
  set(_rig_revision "${_RIG_RESOLVED_REVISION}")
  set(_rig_variant "${_RIG_RESOLVED_VARIANT}")
  set(_rig_promoted "${_RIG_RESOLVED_PROMOTED}")
else()
  message(VERBOSE
    "Rig: _RIG_RESOLVED_NAME is unset -- boards.cmake's fork did not run "
    "before this file in this configure; resolving -DRIG=${RIG} again via "
    "list_rigs.py --rig=.")

  list(TRANSFORM BOARD_ROOT PREPEND "--board-root=" OUTPUT_VARIABLE _rig_board_root_args)

  # "--rig=${RIG}" MUST be quoted: a list promotion target legitimately
  # contains a `;`, and an UNQUOTED expansion here would list-split it
  # into several execute_process COMMAND arguments, handing list_rigs.py
  # only the first element -- the SAME hazard boards.cmake's own Step 1
  # call guards against.
  execute_process(
    COMMAND ${PYTHON_EXECUTABLE} ${_RIG_MODULE_ROOT}/scripts/list_rigs.py
      ${_rig_board_root_args} "--rig=${RIG}"
      --cmakeformat={NAME}\;{DIR}\;{BOARD}\;{REVISION}\;{VARIANT}\;{PROMOTED}
    OUTPUT_VARIABLE _rig_fallback_out
    ERROR_VARIABLE _rig_fallback_err
    RESULT_VARIABLE _rig_fallback_rv)
  if(_rig_fallback_rv)
    message(FATAL_ERROR "Rig: -DRIG=${RIG} did not resolve:\n${_rig_fallback_err}")
  endif()
  string(STRIP "${_rig_fallback_out}" _rig_fallback_out)
  cmake_parse_arguments(_RIG_FALLBACK "" "NAME;DIR;BOARD;REVISION;VARIANT;PROMOTED" "" ${_rig_fallback_out})

  set(_rig_dir "${_RIG_FALLBACK_DIR}")
  set(_rig_name "${_RIG_FALLBACK_NAME}")
  set(_rig_revision "${_RIG_FALLBACK_REVISION}")
  set(_rig_variant "${_RIG_FALLBACK_VARIANT}")
  set(_rig_promoted "${_RIG_FALLBACK_PROMOTED}")
endif()
if(_rig_revision STREQUAL "NOTFOUND")
  set(_rig_revision "")
endif()
if(_rig_variant STREQUAL "NOTFOUND")
  set(_rig_variant "")
endif()
if(_rig_promoted STREQUAL "NOTFOUND")
  set(_rig_promoted "")
endif()
if(_rig_dir STREQUAL "NOTFOUND")
  set(_rig_dir "")
endif()

# A promoted shield has no rig folder at all: rig.yml, the content file
# and every hand-authored overlay/defconfig fragment below are all empty
# rather than constructed from an empty _rig_dir, which would otherwise
# silently concatenate into a bogus absolute path (e.g. "/rig.yml",
# EXISTS'd against the filesystem root). EXISTS on an empty string is
# FALSE (verified against this cmake), so every EXISTS-guarded consumer of
# these further down (steps 6-8: overlay/defconfig application, build_info
# provenance) already skips cleanly with no extra guard needed there --
# this is the ONE place that has to know the difference.
if(_rig_promoted)
  set(_rig_yml "")
  set(_rig_content_yml "")
  set(_rig_user_overlay "")
  set(_rig_conf_file "")
  set(_rig_revision_norm "")
  if(_rig_revision)
    string(REPLACE "." "_" _rig_revision_norm "${_rig_revision}")
  endif()
  set(_rig_variant_overlay "")
  set(_rig_variant_conf_file "")
  # A promoted shield's REVISION is the SHIELD's own -- baked
  # directly into the synthesized content file's `shield:` reference by
  # --promote below, never a `<rigname>_<rev>_defconfig`-shaped fragment
  # file this rig folder does not have, so _rig_rev_conf_file stays empty
  # even though _rig_revision itself may be non-empty.
  set(_rig_rev_conf_file "")
  set(_rig_combined_overlay "")
  set(_rig_combined_conf_file "")
else()
  set(_rig_yml "${_rig_dir}/rig.yml")
  if(NOT EXISTS "${_rig_yml}")
    message(FATAL_ERROR
      "Rig: -DRIG=${RIG} resolved to '${_rig_dir}' but it has no rig.yml:\n"
      "  Expected: ${_rig_yml}")
  endif()

  # The rig's REQUIRED content file (metadata/content split: rig.yml is
  # metadata-only, instances:/wires: live in <rigname>.yml).
  # Its name depends on the RESOLVED rig name, already in hand above (from
  # either boards.cmake's stash or the list_rigs.py fallback) -- never
  # parsed from rig.yml itself, per THE TRAP note on the axis fragments
  # below. No EXISTS check here: an absent content file is the loader's own
  # lang-content diagnostic (it names the file it looked for), not a
  # cmake-level FATAL_ERROR -- cmake only needs the constructed PATH, added
  # to the static CMAKE_CONFIGURE_DEPENDS set alongside rig.yml (step 4).
  # That static registration is the ordering fix this file needs: a content
  # file broken enough that expansion fails never reaches the point of
  # writing RIG_DEPENDS, so relying solely on rigc's own dynamic
  # report would leave editing a MISSING or malformed content file unable to
  # ever retrigger configure -- the exact failure mode CMAKE_CONFIGURE_DEPENDS
  # exists to close for rig.yml itself already.
  set(_rig_content_yml "${_rig_dir}/${_rig_name}.yml")

  set(_rig_user_overlay "${_rig_dir}/${_rig_name}.overlay")
  set(_rig_conf_file "${_rig_dir}/${_rig_name}_defconfig")

  # Per-axis fragment filenames (constructed by _-joining the resolved name
  # + selected axis, never parsed) -- built from
  # _rig_name/_rig_revision/_rig_variant, per THE TRAP note above. Empty
  # string (axis not selected / not declared) means no fragment of that kind
  # exists to look for.
  #
  # _rig_revision_norm: hwmv2's own revision normalization
  # (zephyr_build_string, extensions.cmake:1772) -- a dotted revision id
  # becomes underscores in the constructed filename (1.2 -> 1_2). Applied
  # everywhere a revision segment joins into a fragment filename; _rig_revision
  # itself (the SELECTED value used for validation/provenance) stays
  # unnormalized.
  set(_rig_revision_norm "")
  if(_rig_revision)
    string(REPLACE "." "_" _rig_revision_norm "${_rig_revision}")
  endif()

  set(_rig_variant_overlay "")
  set(_rig_variant_conf_file "")
  set(_rig_rev_conf_file "")
  if(_rig_variant)
    set(_rig_variant_overlay "${_rig_dir}/${_rig_name}_${_rig_variant}.overlay")
    set(_rig_variant_conf_file "${_rig_dir}/${_rig_name}_${_rig_variant}_defconfig")
  endif()
  if(_rig_revision)
    set(_rig_rev_conf_file "${_rig_dir}/${_rig_name}_${_rig_revision_norm}_defconfig")
  endif()

  # Combined per-(variant, revision) fragments:
  # ORDER IS REVISION LAST (<rigname>_<variant>_<rev>...), matching hwmv2
  # exactly -- zephyr_build_string() (extensions.cmake:1774) joins
  # board -> qualifiers (soc/cpucluster/variant) -> revision, confirmed
  # against nrf9160dk_nrf9160_ns_0_14_0.overlay. Upstream deliberately does
  # NOT mirror its own selection grammar (which puts revision first); this
  # is not "fixed" here. Collected only when BOTH axes are selected.
  set(_rig_combined_overlay "")
  set(_rig_combined_conf_file "")
  if(_rig_variant AND _rig_revision)
    set(_rig_combined_overlay
      "${_rig_dir}/${_rig_name}_${_rig_variant}_${_rig_revision_norm}.overlay")
    set(_rig_combined_conf_file
      "${_rig_dir}/${_rig_name}_${_rig_variant}_${_rig_revision_norm}_defconfig")
  endif()
endif()

set(_rig_out_dir "${CMAKE_BINARY_DIR}/rig")
file(MAKE_DIRECTORY "${_rig_out_dir}")
# The CLI writes the literal emitter keys into --out-dir: "rig-gen.overlay",
# "config-sheet.md", "expectations.yml" (rig-gen.* = generated counterparts
# of the rig folder's own hand-authored <RIG>_defconfig/<RIG>.overlay).
set(_rig_overlay "${_rig_out_dir}/rig-gen.overlay")
set(_rig_conf "${_rig_out_dir}/rig-gen.conf")

# Shield-library roots: every board_root's boards/shields, mirroring how
# list_shields.py itself discovers shields (root/boards/shields). rigc
# unions them and self-filters to rig templates (a folder is a template if
# and only if it holds <name>.shield).
set(_rig_shield_dir_args)
foreach(_root ${BOARD_ROOT})
  if(EXISTS "${_root}/boards/shields")
    list(APPEND _rig_shield_dir_args --shield-dir "${_root}/boards/shields")
  endif()
endforeach()

# _rig_debug_env / _rig_debug_argv split out the env-prefix from the argv
# (rather than composing _rig_cmd's cmake -E env ... tokens directly) so
# BOTH the VERBOSE render below AND rerun-expand.sh can show the invocation
# in native shell syntax (NAME=val NAME=val exe args...), not cmake's own
# -E env spelling — that's what's actually copy-pasteable into zsh with a
# debugger prepended (e.g. python3 -m pdb -m ${RIGC_COMPILE} expand
# ...). _rig_cmd (what execute_process actually runs) is composed FROM them.
if(RIGC_COMMAND)
  set(_rig_debug_env "")
  set(_rig_debug_argv ${RIGC_COMMAND})
  set(_rig_cmd ${RIGC_COMMAND})
else()
  set(_rig_debug_env
    "PYTHONPATH=${RIGC_PYTHONPATH}"
    "ZEPHYR_BASE=${ZEPHYR_BASE}")
  # --board <target> is passed ALWAYS, not only when the user gave
  # -DBOARD themselves: by this point
  # BOARD is cmake's own final answer, given or inferred by boards.cmake's
  # fork -- cmake is the single authority on which board is actually being
  # built, so RIG_BOARD (context.cmake, read by the message(STATUS ...)
  # and build_info() calls below) always reports the board this build
  # used, matching whatever rig.board resolves to whether that came from
  # rig.yml or from -DBOARD.
  #
  # <target> is BOARD[@BOARD_REVISION][/BOARD_QUALIFIERS] -- the SAME
  # "board[@revision]/soc/variant" shape rig.yml's own board: declares and
  # a user may pass to -DBOARD, reassembled in the exact order upstream's
  # own parse_board_components() (zephyr cmake/modules/boards.cmake:67-83)
  # splits it apart. Plain ${BOARD} alone is the WRONG value here, and
  # ${BOARD}/${BOARD_QUALIFIERS} alone is STILL wrong: by the time this
  # file runs, the real boards.cmake module (step 2, included above) has
  # already SPLIT a full target given via -DBOARD into THREE separate
  # variables -- bare ${BOARD}, ${BOARD_REVISION}, ${BOARD_QUALIFIERS} --
  # so reassembling only two of them silently drops the revision from
  # RIG_BOARD for any revisioned board target -- verified against a real
  # configure: -DRIG=<a boardless rig> -DBOARD=nrf9160dk@0.14.0/nrf9160
  # (upstream's own revisioned board, reachable via ${ZEPHYR_BASE}'s
  # default BOARD_ROOT entry) renders the expand command with
  # `--board nrf9160dk@0.14.0/nrf9160` intact, and the phys-board
  # rejection that follows (nrf9160dk declares no socket,* node -- no rig
  # shield mates it, so the rig itself never accepts) echoes the same
  # string back verbatim in its own diagnostic. Confirms the JOIN; the
  # rig's own accept path was not and could not be exercised with a
  # revisioned board this way, since no board in any BOARD_ROOT this
  # workspace carries both a socket,* node and a revisions: axis.
  set(_rig_board_target "${BOARD}")
  if(BOARD_REVISION)
    set(_rig_board_target "${_rig_board_target}@${BOARD_REVISION}")
  endif()
  if(BOARD_QUALIFIERS)
    set(_rig_board_target "${_rig_board_target}/${BOARD_QUALIFIERS}")
  endif()
  set(_rig_debug_argv
    "${PYTHON_EXECUTABLE}" -m ${RIGC_COMPILE} expand)
  # A promoted shield has no rig.yml on disk: --promote takes its place
  # as rigc's own positional slot, and rigc synthesizes the pair
  # itself, into its OWN workdir, rather than cmake ever writing one into
  # the source tree.
  if(_rig_promoted)
    # _rig_promoted may legitimately carry a `;` (a list promotion
    # target) -- list_rigs.py's own
    # {PROMOTED} value already survived ONE escaped round trip through
    # cmake_parse_arguments above (this file's Step 3 / boards.cmake's
    # Step 1), landing back here as the real, un-escaped string. TWO
    # MORE unquoted-list-expansion hops still stand between here and the
    # actual subprocess argv -- composing _rig_cmd below (`set(_rig_cmd
    # ... ${_rig_debug_argv})`) and the execute_process(COMMAND
    # ${_rig_cmd} ...) that runs it -- so the value is escaped TWICE
    # more here, mirroring list_rigs.py's own `_cmake_list_escape`
    # (verified empirically against this tree's CMake: each unquoted hop
    # consumes exactly one level of `\;` -> `;`, so two hops need two
    # levels). A value with no `;` at all round-trips through this as an
    # identity.
    set(_rig_promoted_listsafe "${_rig_promoted}")
    string(REPLACE ";" "\;" _rig_promoted_listsafe "${_rig_promoted_listsafe}")
    string(REPLACE ";" "\;" _rig_promoted_listsafe "${_rig_promoted_listsafe}")
    list(APPEND _rig_debug_argv --promote "${_rig_promoted_listsafe}")
  else()
    list(APPEND _rig_debug_argv "${_rig_yml}")
  endif()
  list(APPEND _rig_debug_argv
    ${_rig_shield_dir_args}
    --board "${_rig_board_target}"
    --board-dts "${_rig_board_dts}"
    ${_rig_include_dir_args}
    ${_rig_bindings_dir_args}
    ${_rig_connector_dir_args}
    --out-dir "${_rig_out_dir}")
  # --revision/--variant carry the SELECTED axis (empty = not selected /
  # not declared), so the loader validates against rig.yml's own
  # declarations and applies defaults exactly as list_rigs.py already did
  # for cmake's own filename construction above -- omitted entirely rather
  # than passed empty, so the loader sees "bare target" (None), not a
  # selected empty-string axis. For a promoted shield, --revision means
  # something else entirely to rigc (the SHIELD's own revision) --
  # _rig_variant is always empty there (a promoted shield's own resolver
  # already refuses one before this point is ever reached), so only
  # --revision can carry anything in that case.
  if(_rig_revision)
    list(APPEND _rig_debug_argv --revision "${_rig_revision}")
  endif()
  if(_rig_variant)
    list(APPEND _rig_debug_argv --variant "${_rig_variant}")
  endif()
  set(_rig_cmd "${CMAKE_COMMAND}" -E env ${_rig_debug_env} ${_rig_debug_argv})
endif()

_rig_shell_quote_env(_rig_expand_env_render ${_rig_debug_env})
_rig_shell_quote_argv(_rig_expand_argv_render ${_rig_debug_argv})
if(_rig_expand_env_render)
  set(_rig_expand_render "${_rig_expand_env_render} ${_rig_expand_argv_render}")
else()
  set(_rig_expand_render "${_rig_expand_argv_render}")
endif()
message(VERBOSE "Rig: expand command:\n${_rig_expand_render}")

# rerun-expand.sh: always written, BEFORE execute_process — so even a FAILED
# expand leaves behind a standalone, executable re-run of the exact pass-1
# invocation (e.g. python3 -m pdb -m ${RIGC_COMPILE} expand ..., copied
# from the exec line below). Rewritten every configure; nothing here is
# durable. The debugger hint line below is interpolated with the module
# actually run (RIGC_COMPILE), not hardcoded, so it never names the
# wrong module if RIGC_COMPILE is ever overridden -- a rerun script naming
# the wrong module would be worse than no rerun script at all.
set(_rig_rerun_script "${_rig_out_dir}/rerun-expand.sh")
set(_rig_rerun_lines
  "#!/bin/sh"
  "# regenerate: this file is rewritten on every configure -- edits here do not persist."
  "# Re-runs cmake/modules/dts.cmake's pass-1 invocation standalone (e.g. under"
  "# a debugger: copy the env + argv below into 'python3 -m pdb -m ${RIGC_COMPILE} expand ...')."
  "set -e")
foreach(_rig_env_pair ${_rig_debug_env})
  string(FIND "${_rig_env_pair}" "=" _rig_eq_pos)
  string(SUBSTRING "${_rig_env_pair}" 0 ${_rig_eq_pos} _rig_env_name)
  math(EXPR _rig_val_start "${_rig_eq_pos} + 1")
  string(SUBSTRING "${_rig_env_pair}" ${_rig_val_start} -1 _rig_env_value)
  _rig_shell_quote_token(_rig_env_value_render "${_rig_env_value}")
  list(APPEND _rig_rerun_lines "export ${_rig_env_name}=${_rig_env_value_render}")
endforeach()
list(APPEND _rig_rerun_lines "exec ${_rig_expand_argv_render} \"$@\"")
list(JOIN _rig_rerun_lines "\n" _rig_rerun_content)
file(WRITE "${_rig_rerun_script}" "${_rig_rerun_content}\n")
file(CHMOD "${_rig_rerun_script}" PERMISSIONS
  OWNER_READ OWNER_WRITE OWNER_EXECUTE
  GROUP_READ GROUP_EXECUTE
  WORLD_READ WORLD_EXECUTE)

if(_rig_promoted)
  message(STATUS "Rig: expanding promoted shield '${_rig_promoted}' -> ${_rig_out_dir}")
else()
  message(STATUS "Rig: expanding ${_rig_yml} -> ${_rig_out_dir}")
endif()
execute_process(
  COMMAND ${_rig_cmd}
  RESULT_VARIABLE _rig_result
  OUTPUT_VARIABLE _rig_stdout
  ERROR_VARIABLE _rig_stderr)

if(NOT _rig_result EQUAL 0)
  message(FATAL_ERROR
    "Rig: ${RIGC_COMPILE} expand failed for -DRIG=${RIG} (exit ${_rig_result})\n"
    "--- command ---\n${_rig_cmd}\n"
    "--- stdout ---\n${_rig_stdout}\n--- stderr ---\n${_rig_stderr}")
endif()
if(_rig_stdout OR _rig_stderr)
  message(STATUS "Rig: ${RIGC_COMPILE} output:\n${_rig_stdout}${_rig_stderr}")
endif()
if(NOT EXISTS "${_rig_overlay}")
  message(FATAL_ERROR
    "Rig: expand reported success but wrote no overlay:\n  ${_rig_overlay}")
endif()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 4: context.cmake handoff.
#
# _rig_yml/_rig_content_yml are both empty for a promoted shield (no rig
# folder exists to hold either), so these two are skipped rather than
# registering a bogus concatenated path -- its equivalent STATIC
# dependency is the shield's own <name>.shield template and shield.yml,
# which RIG_DEPENDS below already records dynamically through the SAME
# shield-library scan rigc's --promote path still runs (rigc opens
# them regardless of which positional slot it was given).
if(_rig_yml)
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${_rig_yml}")
endif()
# The content file (see its own comment above): registered unconditionally,
# same as rig.yml, regardless of whether it currently EXISTS -- the whole
# point is to retrigger configure once a missing/broken one gets fixed.
if(_rig_content_yml)
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${_rig_content_yml}")
endif()
if(EXISTS "${_rig_conf_file}")
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${_rig_conf_file}")
endif()
if(EXISTS "${_rig_user_overlay}")
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${_rig_user_overlay}")
endif()
file(GLOB _rig_rigc_sources "${_RIG_MODULE_ROOT}/scripts/${RIGC_COMPILE}/*.py")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${_rig_rigc_sources})
# The -DRIG=<name> resolver itself (list_rigs.py) — an obvious static miss:
# renaming/adding a rig.yml rig.name changes what -DRIG resolves to.
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS
  "${_RIG_MODULE_ROOT}/scripts/list_rigs.py")

# Handoff: rigc wrote context.cmake telling us what the rig instantiated
# (RIG_NAME / RIG_BOARD / RIG_SHIELDS / RIG_SHIELD_REVISIONS / RIG_REVISION /
# RIG_VARIANT). Step 5 drives its Kconfig/bookkeeping loop over RIG_SHIELDS
# instead of -DSHIELD, consulting RIG_SHIELD_REVISIONS ("<name>@<rev>" per
# distinct shield revision resolved) for each shield's own
# revision Kconfig fragment.
include(${_rig_out_dir}/context.cmake OPTIONAL)
set(_rig_qualifier_desc "")
if(RIG_REVISION)
  string(APPEND _rig_qualifier_desc " revision=${RIG_REVISION}")
  # hwmv2 nearest-lower match: only set by context.cmake when a request
  # was actually made AND it resolved to something else (emitter/context.py
  # render()) -- an axis simply defaulted never prints this.
  if(RIG_REVISION_REQUESTED)
    string(APPEND _rig_qualifier_desc " (requested ${RIG_REVISION_REQUESTED})")
  endif()
endif()
if(RIG_VARIANT)
  string(APPEND _rig_qualifier_desc " variant=${RIG_VARIANT}")
endif()
message(STATUS "Rig: '${RIG_NAME}' board=${RIG_BOARD} shields=[${RIG_SHIELDS}]${_rig_qualifier_desc}")

# _rig_applied_fragments: every axis/revision fragment actually collected --
# initialized HERE (rather than at step 7, where its own rig-level fragments
# used to be its first writer) so step 5's per-shield loop, below, can
# append a selected shield revision's own Kconfig fragment to the SAME list
# and get the SAME dependency-tracking + build_info treatment step 7/8
# already give every other applied fragment.
set(_rig_applied_fragments)

# Dependency-tracking handoff (dynamic half): RIG_DEPENDS is every real
# source-tree file THIS expand actually read — rig.yml, every parsed
# .shield template (+ its cpp-included files), connector plug/socket
# bindings, index headers, the board .dts — rigc is the single
# authority on what pass 1 opened, so it is the one that reports this, not a
# glob re-derived here. Appended on top of the static registrations above,
# which cover the PRE-expansion trigger set (rig.yml itself, rigc's
# own sources, list_rigs.py): editing e.g. a .shield template not yet named
# by any instance in this rig is untracked until the rig names it and one
# configure runs to pick it up (a one-configure lag, acceptable — the static
# set guarantees that configure happens whenever the rig FILE itself changes).
if(DEFINED RIG_DEPENDS AND RIG_DEPENDS)
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${RIG_DEPENDS})
endif()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 5: shield resolution
#
# Unlike stock shields.cmake, shields here are never selected via -DSHIELD;
# they come from the rig's own instances (RIG_SHIELDS, set by context.cmake
# above). DT is entirely rigc's domain — it already emitted the
# overlay set (step 3's ${_rig_overlay}, handed off in step 7) — so this
# step's job is Kconfig + bookkeeping only:
#   - keep the list_shields.py discovery block (SHIELD_LIST/SHIELD_DIR_<name>)
#     unchanged: our shield folders have matching shield.yml names, so it
#     finds them exactly as it would for a stock shield;
#   - validate each rig shield resolves to a real shield folder, else
#     FATAL_ERROR (retargeted from the stock "invalid SHIELD" error);
#   - collect each shield's <name>.conf plus board-specific CONF_FILES (KCONF
#     only — the <name>.overlay / DTS collection is dropped entirely, rigc
#     owns DT);
#   - set SHIELD_AS_LIST so kconfig.cmake's shields_list_contains (which
#     every shield's Kconfig.shield calls) turns SHIELD_<NAME> on. Reusing
#     SHIELD_AS_LIST here is safe: stock shields.cmake's DTS-collection use of
#     it never runs for a rig build (the shields.cmake fork dispatches away
#     from it whenever -DRIG is set), so there is no double-overlay risk.
#   - drop the stock zephyr_check_cache(SHIELD WATCH) / SHIELD-from-cache
#     seeding entirely: shields come from the rig file, already tracked via
#     CMAKE_CONFIGURE_DEPENDS on the .rig.yml above.
# ---------------------------------------------------------------------------

# Prepare list shields command.
# This command is used for locating the shield dir as well as printing all shields
# in the system in the following cases:
# - A rig names a shield with no matching folder
# - User invokes <build-command> shields target
list(TRANSFORM BOARD_ROOT PREPEND "--board-root=" OUTPUT_VARIABLE board_root_args)

set(list_shields_commands
  COMMAND ${PYTHON_EXECUTABLE} ${ZEPHYR_BASE}/scripts/list_shields.py
  ${board_root_args} --json
)

# Get list of shields in JSON format
execute_process(${list_shields_commands}
  OUTPUT_VARIABLE shields_json
  ERROR_VARIABLE err_shields
  RESULT_VARIABLE ret_val
)

if(ret_val)
  message(FATAL_ERROR "Error finding shields\nError message: ${err_shields}")
endif()

string(JSON shields_length LENGTH ${shields_json})

# Collect every candidate dir per shield name first (list_shields.py's own
# output is unfiltered stock-Zephyr content: BOARD_ROOT commonly contains
# BOTH this module and the ZEPHYR_BASE tree it builds against, and a name
# collision is real -- e.g. this module's own boards/shields/
# adafruit_data_logger shares its name with the stock Zephyr shield of the
# same name.
set(SHIELD_LIST)
if(shields_length GREATER 0)
  math(EXPR shields_length "${shields_length} - 1")

  foreach(i RANGE ${shields_length})
    string(JSON shield GET "${shields_json}" "${i}")
    string(JSON shield_name GET ${shield} name)
    string(JSON shield_dir GET ${shield} dir)
    if(NOT shield_name IN_LIST SHIELD_LIST)
      list(APPEND SHIELD_LIST ${shield_name})
    endif()
    list(APPEND _rig_shield_candidate_dirs_${shield_name} ${shield_dir})
  endforeach()
endif()
list(SORT SHIELD_LIST)

# Resolve each name's candidate(s) to ONE dir. Discovery rule (matches
# rigc's own load_shield_library, loader_yml.py): a folder is a rig
# TEMPLATE if and only if it holds <name>.shield, so on a collision that
# marker is what rigc actually used to build the overlay -- prefer it. A
# single dir needs no resolution; report an ambiguity (0 or >=2 marked
# candidates) so it's visible instead of silently picking whichever root
# came last.
foreach(shield_name ${SHIELD_LIST})
  set(_rig_shield_candidates ${_rig_shield_candidate_dirs_${shield_name}})
  list(REMOVE_DUPLICATES _rig_shield_candidates)
  list(LENGTH _rig_shield_candidates _rig_shield_ncand)
  if(_rig_shield_ncand EQUAL 1)
    list(GET _rig_shield_candidates 0 _rig_shield_chosen)
  else()
    set(_rig_shield_marked)
    foreach(_rig_shield_cand ${_rig_shield_candidates})
      if(EXISTS "${_rig_shield_cand}/${shield_name}.shield")
        list(APPEND _rig_shield_marked "${_rig_shield_cand}")
      endif()
    endforeach()
    list(LENGTH _rig_shield_marked _rig_shield_nmarked)
    if(_rig_shield_nmarked EQUAL 1)
      # Exactly one candidate is a rig template -- the unambiguous, expected
      # case for a same-named stock/rig-template collision. No warning.
      list(GET _rig_shield_marked 0 _rig_shield_chosen)
    else()
      # 0 or >=2 candidates carry the marker: genuinely ambiguous. Choose
      # deterministically (alphabetically first among the marked dirs if
      # any are marked, else alphabetically first among all candidates) and
      # say so loudly, naming every candidate.
      if(_rig_shield_nmarked GREATER 0)
        set(_rig_shield_pool ${_rig_shield_marked})
      else()
        set(_rig_shield_pool ${_rig_shield_candidates})
      endif()
      list(SORT _rig_shield_pool)
      list(GET _rig_shield_pool 0 _rig_shield_chosen)
      string(REPLACE ";" "\n  " _rig_shield_candidates_str "${_rig_shield_candidates}")
      if(_rig_shield_nmarked GREATER 0)
        set(_rig_shield_pool_desc "alphabetically first among the marked candidates")
      else()
        set(_rig_shield_pool_desc "alphabetically first among all candidates (none marked)")
      endif()
      message(WARNING
        "Rig: shield name '${shield_name}' is offered by ${_rig_shield_ncand} "
        "different BOARD_ROOT directories, and ${_rig_shield_nmarked} of them "
        "carry the rig-template marker '${shield_name}.shield' (expected "
        "exactly 1):\n  ${_rig_shield_candidates_str}\n"
        "Rig: choosing (${_rig_shield_pool_desc}): ${_rig_shield_chosen}")
    endif()
  endif()
  set(SHIELD_DIR_${shield_name} ${_rig_shield_chosen})
endforeach()

# Process the rig's shields (RIG_SHIELDS from context.cmake, not -DSHIELD).
foreach(s ${RIG_SHIELDS})
  if(NOT s IN_LIST SHIELD_LIST)
    string(REPLACE ";" "\n" shield_string "${SHIELD_LIST}")
    message("No shield named '${s}' found")
    message("Please choose from among the following shields:\n"
            "${shield_string}"
    )
    message(FATAL_ERROR
      "Rig: '${RIG_NAME}' names shield '${s}', which has no matching shield "
      "folder; see above.")
  endif()

  # Add the shield's directory to the SHIELD_DIRS output variable.
  list(APPEND
    SHIELD_DIRS
    ${SHIELD_DIR_${s}}
    )

  # Provenance: which folder won for this shield name — non-obvious whenever
  # the rig-template-marker collision preference above had a choice to make.
  # A resolved shield revision (RIG_SHIELD_REVISIONS entries are
  # "<name>@<rev>") is shown alongside it, since it decides which
  # DT/Kconfig content this shield actually contributed. Present for every
  # shield declaring a revisions: axis, defaults included -- a build log
  # that named only non-default revisions could not distinguish "revision
  # 1" from "this shield has no revisions at all".
  set(_rig_shield_rev "")
  foreach(_rig_sr ${RIG_SHIELD_REVISIONS})
    string(FIND "${_rig_sr}" "@" _rig_sr_at)
    string(SUBSTRING "${_rig_sr}" 0 ${_rig_sr_at} _rig_sr_name)
    if(_rig_sr_name STREQUAL s)
      math(EXPR _rig_sr_rev_start "${_rig_sr_at} + 1")
      string(SUBSTRING "${_rig_sr}" ${_rig_sr_rev_start} -1 _rig_shield_rev)
    endif()
  endforeach()
  if(_rig_shield_rev)
    message(STATUS "Rig: shield '${s}' <- ${SHIELD_DIR_${s}} (revision ${_rig_shield_rev})")
  else()
    message(STATUS "Rig: shield '${s}' <- ${SHIELD_DIR_${s}}")
  endif()

  include(${SHIELD_DIR_${s}}/pre_dt_shield.cmake OPTIONAL)

  # Search for shield/shield.conf file (DT collection intentionally dropped —
  # rigc already emitted the overlay set, handed off in step 7).
  if(EXISTS ${SHIELD_DIR_${s}}/${s}.conf)
    list(APPEND
      shield_conf_files
      ${SHIELD_DIR_${s}}/${s}.conf
      )
  endif()

  # The selected shield revision's OWN Kconfig fragment (<name>_<rev>.conf,
  # shield convention — the rig-vs-shield fragment-naming table), collected
  # in the precedence position that matches the DT layering (base .shield
  # first, revision .shield cpp-included after it into the same TU): this
  # fragment lands AFTER the shield's own base .conf above. hwmv2's
  # revision dot-normalization applies to the segment here exactly as it
  # does to a rig axis fragment's own filename. Optional, like every other
  # axis Kconfig fragment: a revision may carry DT only.
  if(_rig_shield_rev)
    string(REPLACE "." "_" _rig_shield_rev_norm "${_rig_shield_rev}")
    set(_rig_shield_rev_conf "${SHIELD_DIR_${s}}/${s}_${_rig_shield_rev_norm}.conf")
    if(EXISTS "${_rig_shield_rev_conf}")
      list(APPEND shield_conf_files "${_rig_shield_rev_conf}")
      list(APPEND _rig_applied_fragments "${_rig_shield_rev_conf}")
      message(STATUS "Rig: applying shield revision Kconfig ${_rig_shield_rev_conf}")
    endif()
  endif()

  # Add board-specific .conf files to shield_conf_files (KCONF only).
  zephyr_file(CONF_FILES ${SHIELD_DIR_${s}}/boards
              KCONF shield_conf_files
  )
  zephyr_file(CONF_FILES ${SHIELD_DIR_${s}}/boards/${s}
              KCONF shield_conf_files
  )
endforeach()

# The Kconfig activation trigger: kconfig.cmake passes SHIELD_AS_LIST into
# Kconfig, and each shield's Kconfig.shield (def_bool
# $(shields_list_contains,<name>)) makes SHIELD_<NAME> true, firing its
# Kconfig.defconfig.
set(SHIELD_AS_LIST "${RIG_SHIELDS}")

# Prepend each shield with COMMAND <cmake> -E echo <shield>" for printing.
# Each shield is printed as new command because build files are not fond of newlines.
list(TRANSFORM SHIELD_LIST PREPEND "COMMAND;${CMAKE_COMMAND};-E;echo;"
     OUTPUT_VARIABLE shields_target_cmd
)

add_custom_target(shields ${shields_target_cmd} USES_TERMINAL)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 6: pre_dt_module_run(), second run. SHIELD_DIRS is now known (step 5),
# so calling the function directly (NOT include(pre_dt) again -- its
# global include_guard already tripped in step 1 and would make a second
# include a silent no-op) recomputes DTS_ROOT / DTS_ROOT_SYSTEM_INCLUDE_DIRS
# for pass 2 with shield bindings folded in, exactly as a plain --shield
# build gets them.
pre_dt_module_run()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 7: overlay/conf handoff. DT and Kconfig ride DIFFERENT slots, and that
# asymmetry is deliberate, not an oversight: rigc is the SOLE author
# of DT (step 5's shield loop drops every shield's own <name>.overlay
# entirely), so the rig's own DT fragments have no existing slot to join and
# must PREPEND onto EXTRA_DTC_OVERLAY_FILE instead. Kconfig, by contrast, DOES
# have an existing slot every rig build already populates -- shield_conf_files
# (step 5) -- so the rig's own Kconfig fragments simply APPEND onto it, no
# separate prepend mechanism needed. Should rigc ever start
# authoring DT the shield loop currently drops (a rig-level shield overlay
# override), this asymmetry is the first thing to revisit.
#
# EXTRA_DTC_OVERLAY_FILE handoff (unchanged): by this point in the module
# chain, configuration_files.cmake has already finalized
# EXTRA_DTC_OVERLAY_FILE as a plain variable (zephyr_get(... MERGE)), folding
# in any user -DEXTRA_DTC_OVERLAY_FILE=/-DOVERLAY_CONFIG=. A cache-FORCE
# write here would silently clobber that user value; instead we PREPEND our
# rig fragments onto the existing plain variable -- user extras WIN, since a
# user-passed value applies after all rig fragments (EXTRA_DTC_OVERLAY_FILE
# applies its files in list order, later files taking precedence) and can
# override them. Internal ordering: rigc's generated overlay first,
# then the rig folder's own hand-authored <RIG>.overlay (if present) --
# the DT counterpart of <RIG>_defconfig, a rig author supplying DT rigc
# cannot emit, notably the board pinctrl pinmux fragment a function
# needs to route on real silicon: rigc only enables the controller
# (status="okay") and names the pin in the config sheet; it does not
# author SoC pinmux. Applied after rigc's own overlay so it can augment
# nodes rigc created.
# _rig_applied_fragments is already initialized (step 4, above step 5) --
# NOT reset here, since step 5's shield loop may already have appended a
# selected shield revision's own Kconfig fragment to it.
set(_rig_overlay_files "${_rig_overlay}")
if(EXISTS "${_rig_user_overlay}")
  list(APPEND _rig_overlay_files "${_rig_user_overlay}")
  message(STATUS "Rig: applying ${_rig_user_overlay}")
endif()
# Per-variant DT fragment (variant only -- revisions have no single-axis
# .overlay kind): base -> variant, most specific last, same list-order
# precedence EXTRA_DTC_OVERLAY_FILE already gives the base pair above.
if(_rig_variant_overlay AND EXISTS "${_rig_variant_overlay}")
  list(APPEND _rig_overlay_files "${_rig_variant_overlay}")
  list(APPEND _rig_applied_fragments "${_rig_variant_overlay}")
  message(STATUS "Rig: applying variant overlay ${_rig_variant_overlay}")
endif()
# Combined per-(variant, revision) DT fragment: the most specific of
# all, so it collects last -- after the single-axis variant overlay above.
if(_rig_combined_overlay AND EXISTS "${_rig_combined_overlay}")
  list(APPEND _rig_overlay_files "${_rig_combined_overlay}")
  list(APPEND _rig_applied_fragments "${_rig_combined_overlay}")
  message(STATUS "Rig: applying combined overlay ${_rig_combined_overlay}")
endif()
set(EXTRA_DTC_OVERLAY_FILE ${_rig_overlay_files} ${EXTRA_DTC_OVERLAY_FILE})

# shield_conf_files handoff: rigc's generated fragment (${_rig_conf},
# e.g. Kconfig facts derived from the topology) first, then the rig folder's
# own hand-authored <RIG>_defconfig
if(EXISTS "${_rig_conf}")
  list(APPEND shield_conf_files "${_rig_conf}")
else()
  message(STATUS "Rig: no Kconfig fragment produced")
endif()

if(EXISTS "${_rig_conf_file}")
  list(APPEND shield_conf_files "${_rig_conf_file}")
  message(STATUS "Rig: applying ${_rig_conf_file}")
endif()

# Per-axis Kconfig fragments, base -> variant -> revision (most specific
# last) -- same APPEND slot the base pair above already rides.
if(_rig_variant_conf_file AND EXISTS "${_rig_variant_conf_file}")
  list(APPEND shield_conf_files "${_rig_variant_conf_file}")
  list(APPEND _rig_applied_fragments "${_rig_variant_conf_file}")
  message(STATUS "Rig: applying variant defconfig ${_rig_variant_conf_file}")
endif()
if(_rig_rev_conf_file AND EXISTS "${_rig_rev_conf_file}")
  list(APPEND shield_conf_files "${_rig_rev_conf_file}")
  list(APPEND _rig_applied_fragments "${_rig_rev_conf_file}")
  message(STATUS "Rig: applying revision defconfig ${_rig_rev_conf_file}")
endif()
# Combined per-(variant, revision) Kconfig fragment: most specific of
# all, so it collects last of the whole chain.
if(_rig_combined_conf_file AND EXISTS "${_rig_combined_conf_file}")
  list(APPEND shield_conf_files "${_rig_combined_conf_file}")
  list(APPEND _rig_applied_fragments "${_rig_combined_conf_file}")
  message(STATUS "Rig: applying combined defconfig ${_rig_combined_conf_file}")
endif()

# Dependency-tracking (item 4/7): every APPLIED fragment must retrigger
# configure on edit, same as the base pair already registered in step 4 --
# these are cmake-known (constructed + EXISTS-checked above, never opened
# by the loader), so they are added directly rather than round-tripped
# through rigc's own RIG_DEPENDS report.
if(_rig_applied_fragments)
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${_rig_applied_fragments})
endif()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 8: build-info provenance (rig-build provenance requirement): record
# what THIS rig build looked at, via zephyr's own build_info()
# (cmake/modules/extensions.cmake) — the same mechanism the real dts.cmake
# uses for its own devicetree section.
list(JOIN RIG_SHIELDS ", " _rig_shields_joined)
list(JOIN SHIELD_DIRS ", " _rig_shield_dirs_joined)
list(JOIN _rig_applied_fragments ", " _rig_fragments_joined)

build_info(vendor-specific rig name VALUE "${RIG_NAME}")
build_info(vendor-specific rig board VALUE "${RIG_BOARD}")
# Both empty for a promoted shield (no rig folder, see step 3) -- guarded
# rather than recorded as an empty VALUE, same convention as revision/
# variant below.
if(_rig_yml)
  build_info(vendor-specific rig yml VALUE "${_rig_yml}")
endif()
if(_rig_content_yml)
  build_info(vendor-specific rig content-yml VALUE "${_rig_content_yml}")
endif()
if(_rig_promoted)
  # _rig_promoted may legitimately carry a `;` (a list promotion
  # target). Zephyr's own build_info()/
  # yaml_set() (extensions.cmake/yaml.cmake) chain the value through
  # TWO MORE unquoted-list-expansion hops of their own beyond this
  # file's control -- build_info()'s `set(arg_list ${ARGV})`, then
  # yaml_set()'s own `cmake_parse_arguments(... "NAME;VALUE" ... ${ARGN})`
  # (a single-value keyword, and cmake_parse_arguments itself consumes
  # TWO levels internally, empirically, the same non-obvious behavior
  # this file's own `_rig_promoted_listsafe` comment already names).
  # FIVE levels of `\;` -> `;` escaping survive that whole chain intact
  # -- verified empirically against a standalone build_info()/yaml_set()
  # call in this tree's actual zephyr checkout (four is NOT enough; the
  # value truncates silently at the first element). This is NOT a
  # documented CMake/Zephyr contract, only a measured fact about the
  # current implementations of both macros -- fragile against a version
  # bump of either.
  set(_rig_promoted_buildinfo "${_rig_promoted}")
  foreach(_rig_bi_escape_pass RANGE 1 5)
    string(REPLACE ";" "\;" _rig_promoted_buildinfo "${_rig_promoted_buildinfo}")
  endforeach()
  build_info(vendor-specific rig promoted-shield VALUE "${_rig_promoted_buildinfo}")
endif()
build_info(vendor-specific rig board-dts VALUE "${_rig_board_dts}")
build_info(vendor-specific rig shields VALUE "${_rig_shields_joined}")
build_info(vendor-specific rig shield-dirs VALUE "${_rig_shield_dirs_joined}")
# Symmetric with the rig's own revision/variant below: every DISTINCT
# shield revision resolved, "<name>@<rev>", defaults included exactly as
# RIG_REVISION records a defaulted rig revision -- absent entirely when no
# shield declares an axis, the same "no declaration, no key" precedent.
if(RIG_SHIELD_REVISIONS)
  list(JOIN RIG_SHIELD_REVISIONS ", " _rig_shield_revisions_joined)
  build_info(vendor-specific rig shield-revisions VALUE "${_rig_shield_revisions_joined}")
endif()
build_info(vendor-specific rig out-dir VALUE "${_rig_out_dir}")
build_info(vendor-specific rig overlay-gen VALUE "${_rig_overlay}")
if(_rig_revision)
  build_info(vendor-specific rig revision VALUE "${_rig_revision}")
endif()
if(_rig_variant)
  build_info(vendor-specific rig variant VALUE "${_rig_variant}")
endif()
if(_rig_applied_fragments)
  build_info(vendor-specific rig fragments VALUE "${_rig_fragments_joined}")
endif()
if(EXISTS "${_rig_conf}")
  build_info(vendor-specific rig defconfig-gen VALUE "${_rig_conf}")
endif()
if(EXISTS "${_rig_conf_file}")
  build_info(vendor-specific rig defconfig VALUE "${_rig_conf_file}")
endif()
if(EXISTS "${_rig_user_overlay}")
  build_info(vendor-specific rig overlay VALUE "${_rig_user_overlay}")
endif()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 9: delegate to the real dts.cmake, last line. zephyr_default.cmake's
# module loop calls dts_init right after include(dts) returns (the
# <module>_init convention) — dts_init is defined by the real dts.cmake
# included here, so it is ready by the time control returns to that loop.
include(${ZEPHYR_BASE}/cmake/modules/dts.cmake)
# ---------------------------------------------------------------------------
