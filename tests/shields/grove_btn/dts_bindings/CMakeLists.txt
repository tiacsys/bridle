# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project(grove_btn_shields)

target_sources(app PRIVATE src/main.c)

function(test_if config node_parent node_label node_dscr node_alt_dscr)
  if(${config})
    dt_nodelabel(node_path NODELABEL "${node_label}")
    if(DEFINED node_path AND "${node_path}" MATCHES "${node_parent}")
      dt_prop(node_prop PATH "${node_path}" PROPERTY "label")
      if(DEFINED node_prop AND ("${node_prop}" STREQUAL "${node_dscr}"
                            OR  "${node_prop}" STREQUAL "${node_alt_dscr}"))
        message(STATUS "Found label \"${node_label}\" at \"${node_path}\" "
                                "as \"${node_prop}\"")
      else()
        message(FATAL_ERROR "Test failed, "
          "actual either "
          "the node path \"${node_path}\" at label \"${node_label}\" "
          "was not found or has no \"label\" property with \"${node_dscr}\" or "
          "\"${node_alt_dscr}\" or the node labels are missing or misspelled."
        )
      endif()
    else()
      message(FATAL_ERROR "Test failed, "
        "actual the node path \"${node_path}\" "
        "was not found in DTS at \"${node_parent}\"."
      )
    endif()
  endif()
endfunction()

if(CONFIG_SHIELD_GROVE_BTN AND NOT CONFIG_GPIO)
  message(FATAL_ERROR "Test failed, "
    "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN} "
    "and CONFIG_GPIO=${CONFIG_GPIO}, expected CONFIG_GPIO=y"
  )
endif()

# disabled, because it is too common, GPIO is enabled by nearly all boards
#if(NOT CONFIG_SHIELD_GROVE_BTN AND CONFIG_GPIO)
#  message(FATAL_ERROR "Test failed, "
#    "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN} "
#    "and CONFIG_GPIO=${CONFIG_GPIO}, expected CONFIG_GPIO=n"
#  )
#endif()

test_if(CONFIG_SHIELD_GROVE_BTN_D0 "/grove_btns" "grove_btn_d0" "Grove Button D0" "Grove Button D0 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D1 "/grove_btns" "grove_btn_d1" "Grove Button D1" "Grove Button D1 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D2 "/grove_btns" "grove_btn_d2" "Grove Button D2" "Grove Button D2 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D3 "/grove_btns" "grove_btn_d3" "Grove Button D3" "Grove Button D3 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D4 "/grove_btns" "grove_btn_d4" "Grove Button D4" "Grove Button D4 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D5 "/grove_btns" "grove_btn_d5" "Grove Button D5" "Grove Button D5 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D6 "/grove_btns" "grove_btn_d6" "Grove Button D6" "Grove Button D6 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D7 "/grove_btns" "grove_btn_d7" "Grove Button D7" "Grove Button D7 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D8 "/grove_btns" "grove_btn_d8" "Grove Button D8" "Grove Button D8 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D9 "/grove_btns" "grove_btn_d9" "Grove Button D9" "Grove Button D9 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D10 "/grove_btns" "grove_btn_d10" "Grove Button D10" "Grove Button D10 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D11 "/grove_btns" "grove_btn_d11" "Grove Button D11" "Grove Button D11 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D12 "/grove_btns" "grove_btn_d12" "Grove Button D12" "Grove Button D12 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D13 "/grove_btns" "grove_btn_d13" "Grove Button D13" "Grove Button D13 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D14 "/grove_btns" "grove_btn_d14" "Grove Button D14" "Grove Button D14 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D15 "/grove_btns" "grove_btn_d15" "Grove Button D15" "Grove Button D15 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D16 "/grove_btns" "grove_btn_d16" "Grove Button D16" "Grove Button D16 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D17 "/grove_btns" "grove_btn_d17" "Grove Button D17" "Grove Button D17 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D18 "/grove_btns" "grove_btn_d18" "Grove Button D18" "Grove Button D18 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D19 "/grove_btns" "grove_btn_d19" "Grove Button D19" "Grove Button D19 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D20 "/grove_btns" "grove_btn_d20" "Grove Button D20" "Grove Button D20 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D21 "/grove_btns" "grove_btn_d21" "Grove Button D21" "Grove Button D21 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D22 "/grove_btns" "grove_btn_d22" "Grove Button D22" "Grove Button D22 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D23 "/grove_btns" "grove_btn_d23" "Grove Button D23" "Grove Button D23 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D24 "/grove_btns" "grove_btn_d24" "Grove Button D24" "Grove Button D24 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D25 "/grove_btns" "grove_btn_d25" "Grove Button D25" "Grove Button D25 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D26 "/grove_btns" "grove_btn_d26" "Grove Button D26" "Grove Button D26 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D27 "/grove_btns" "grove_btn_d27" "Grove Button D27" "Grove Button D27 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D28 "/grove_btns" "grove_btn_d28" "Grove Button D28" "Grove Button D28 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D29 "/grove_btns" "grove_btn_d29" "Grove Button D29" "Grove Button D29 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D30 "/grove_btns" "grove_btn_d30" "Grove Button D30" "Grove Button D30 (inverted)")
test_if(CONFIG_SHIELD_GROVE_BTN_D31 "/grove_btns" "grove_btn_d31" "Grove Button D31" "Grove Button D31 (inverted)")
