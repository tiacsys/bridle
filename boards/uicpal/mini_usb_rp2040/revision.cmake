# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if (BOARD STREQUAL "mini_usb_rp2040")
  set(MINI_USB_RP2040_REVISIONS "neopixel" "chipled")
  if (NOT DEFINED BOARD_REVISION)
    set(BOARD_REVISION "neopixel")
  else()
    if (NOT BOARD_REVISION IN_LIST MINI_USB_RP2040_REVISIONS)
      message(FATAL_ERROR
          "${BOARD_REVISION} is not a valid revision for Mini USB RP2040. "
          "Accepted revisions: ${MINI_USB_RP2040_REVISIONS}")
    endif()
  endif()
endif()
