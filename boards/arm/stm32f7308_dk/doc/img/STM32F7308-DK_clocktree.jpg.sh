#!/bin/bash

P="../STM32F7308-DK.pdf"
I="STM32F7308-DK_clocktree.jpg"

N=$(pdfimages -list ${P} | awk '/jpeg/{print $1}' | awk 'FNR == 2 {print}')
pdfimages -j -f ${N} -l ${N} ${P} PI
mv PI-000.jpg ${I}
