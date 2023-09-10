# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

set(WAVESHARE_RP2040_REVISIONS "uartcons" "usbcons")
set(WAVESHARE_RP2040_16MB_BOARDS "waveshare_rp2040_plus")
if (BOARD IN_LIST WAVESHARE_RP2040_16MB_BOARDS)
  list(APPEND WAVESHARE_RP2040_REVISIONS "16mb" "16mb@uartcons" "16mb@usbcons")
endif()
if (NOT DEFINED BOARD_REVISION)
  set(BOARD_REVISION "uartcons")
else()
  if (NOT BOARD_REVISION IN_LIST WAVESHARE_RP2040_REVISIONS)
    message(FATAL_ERROR
        "${BOARD_REVISION} is not a valid revision for Waveshare RP2040. "
        "Accepted revisions: ${WAVESHARE_RP2040_REVISIONS}")
  endif()
endif()
