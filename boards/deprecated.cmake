# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# This file contains boards in Bridle which has been replaced with a new board
# name. This allows the system to automatically change the board while at the
# same time prints a warning to the user, that the board name is deprecated.
#
# To add a board rename, add a line in following format:
# set(<old_board_name>_DEPRECATED <new_board_name>)

set(seeed_xiao_samd21_DEPRECATED
    xiao_samd21
)
set(tiac_magpie_DEPRECATED
    magpie_f777ni
)
