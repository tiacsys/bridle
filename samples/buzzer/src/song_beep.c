/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_beep[] =
{
	{.note = Db6, .duration = eigth},
};
const size_t song_beep_notes = ARRAY_SIZE(song_beep);
