# Copyright (c) 2021-2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

include(${BRIDLE_BASE}/cmake/version.cmake)
configure_file(${BRIDLE_BASE}/version.h.in ${OUT_DIR}/${OUT_FILE})
file(APPEND ${OUT_DIR}/${EXT_FILE} "\n#include \"${OUT_FILE}\"\n")
