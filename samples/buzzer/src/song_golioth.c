/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_golioth[] = {
	{.note = C6, .duration = quarter},
	{.note = REST, .duration = sixth},
	{.note = G5, .duration = sixth},
	{.note = A5, .duration = sixth},
	{.note = Bb5, .duration = sixth},
	{.note = REST, .duration = sixth},
	{.note = Bb5, .duration = sixth},
	{.note = REST, .duration = quarter},
	{.note = C5, .duration = half},
	{.note = REST, .duration = half},
	{.note = REST, .duration = quarter},
	{.note = C6, .duration = quarter}
};
const size_t song_golioth_notes = ARRAY_SIZE(song_golioth);
