#!/bin/bash
#
# SPDX-FileCopyrightText: 2021-2026 TiaC Systems
# SPDX-License-Identifier: BSD-3-Clause
#

P="../STM32F777NIHx.pdf"
I="STM32F777NIHx_clocktree.jpg"

N=$(pdfimages -list ${P} | awk '/jpeg/{print $1}' | awk 'FNR == 2 {print}')
pdfimages -j -f ${N} -l ${N} ${P} PI
mv PI-000.jpg ${I}
