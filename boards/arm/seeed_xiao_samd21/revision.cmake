# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

set(XIAO_REVISIONS "uartcons" "usbcons")
if (NOT DEFINED BOARD_REVISION)
  set(BOARD_REVISION "uartcons")
else()
  if (NOT BOARD_REVISION IN_LIST XIAO_REVISIONS)
    message(FATAL_ERROR
        "${BOARD_REVISION} is not a valid revision for Seeed Studio XIAO SAMD21. "
        "Accepted revisions: ${XIAO_REVISIONS}")
  endif()
endif()
