# Trinamic Startrampe board revisions

# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

set(STARTRAMPE_REVISIONS "uartcons" "usbcons")
if (NOT DEFINED BOARD_REVISION)
  set(BOARD_REVISION "uartcons")
else()
  if (NOT BOARD_REVISION IN_LIST STARTRAMPE_REVISIONS)
    message(FATAL_ERROR
        "${BOARD_REVISION} is not a valid revision for Startrampe. "
        "Accepted revisions: ${STARTRAMPE_REVISIONS}")
  endif()
endif()
