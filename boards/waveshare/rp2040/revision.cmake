# Copyright (c) 2023-2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if (BOARD STREQUAL "waveshare_rp2040_plus")
  set(WAVESHARE_RP2040_REVISIONS "4mb" "16mb")
  if (NOT DEFINED BOARD_REVISION)
    set(BOARD_REVISION "4mb")
  else()
    if (NOT BOARD_REVISION IN_LIST WAVESHARE_RP2040_REVISIONS)
      message(FATAL_ERROR
          "${BOARD_REVISION} is not a valid revision for Waveshare RP2040. "
          "Accepted revisions: ${WAVESHARE_RP2040_REVISIONS}")
    endif()
  endif()
endif()
