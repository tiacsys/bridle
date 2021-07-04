# Copyright (c) 2021 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

foreach(file ${IN_FILES})
  file(READ ${file} CONTENTS)
  file(APPEND ${OUT_FILE} "${CONTENTS}")
endforeach()
