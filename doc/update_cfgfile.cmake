# SPDX-FileCopyrightText: 2022-2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if(IN_FILE AND OUT_FILE)
  configure_file(${IN_FILE} ${OUT_FILE} @ONLY)
else()
  message(FATAL_ERROR "wrong arguments")
endif()
