/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const note_t song_beep[] = {
	{.pitch = Db6, .duration = eighth},
};
const size_t song_beep_notes = ARRAY_SIZE(song_beep);
