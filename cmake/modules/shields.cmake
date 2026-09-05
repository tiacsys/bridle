# SPDX-License-Identifier: Apache-2.0
#
# Downstream FORK POINT for Zephyr's shields build module.
#
# This directory sits on CMAKE_MODULE_PATH ahead of Zephyr's own module
# directory, so zephyr_default.cmake's include(shields) resolves to THIS
# file, shadowing ${ZEPHYR_BASE}/cmake/modules/shields.cmake.
#
# A rig build has NO shields phase: shield selection is a consequence of rig
# expansion, not a standalone phase driven by -DSHIELD. The dts.cmake fork's
# rig block (run later in the module chain) resolves RIG_SHIELDS from
# rigc's own output and sets every variable this module would otherwise
# own (shield_conf_files/SHIELD_AS_LIST/SHIELD_DIRS) directly. So this fork
# is pure dispatch:
#
#   - rig build (-DRIG set): reject -DSHIELD (see the guard below), then
#     early-exit -- nothing else. (This is the draft upstream patch for
#     shields.cmake: "rig builds have no shields phase; -DSHIELD is
#     rejected, not silently ignored.")
#   - otherwise: defer to the ORIGINAL shields.cmake unchanged, so --shield
#     and no-shield builds behave exactly as upstream.
#
# NOTE: reach the original by absolute path (NOT include(shields), which
# would recurse back into this file via the prepended module path).

include_guard(GLOBAL)

if(DEFINED RIG)
  # SHIELD/BOARD exclusivity
  # zephyr_get(SHIELD) (not a bare if(DEFINED SHIELD)) catches every
  # form the real shields.cmake itself would honor -- -DSHIELD on the
  # command line, a value already sitting in CACHE from an earlier
  # (possibly non-rig) configure of this SAME build dir, or $ENV{SHIELD} --
  # so switching a build dir from --shield to --rig use without a
  # pristine rebuild is caught too, not just a fresh dir's cmdline flag.
  zephyr_get(SHIELD)
  if(DEFINED SHIELD)
    message(FATAL_ERROR
      "Rig: -DSHIELD=${SHIELD} was given alongside -DRIG=${RIG}. Shields in "
      "a rig build come from the rig itself -- add an instance naming the "
      "shield, or (for a shield the rig template can't yet express) the "
      "rig folder's own hand-authored <rig-name>.overlay escape hatch. If "
      "this build directory was previously configured with --shield, "
      "pristine it (-p always): the cached SHIELD value is what tripped "
      "this guard.")
  endif()
else()
  include(${ZEPHYR_BASE}/cmake/modules/shields.cmake)
endif()
