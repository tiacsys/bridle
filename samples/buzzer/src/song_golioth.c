/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const note_t song_golioth[] = {
	{.pitch = C6, .duration = quarter},   {.pitch = REST, .duration = sixth},
	{.pitch = G5, .duration = sixth},     {.pitch = A5, .duration = sixth},
	{.pitch = Bb5, .duration = sixth},    {.pitch = REST, .duration = sixth},
	{.pitch = Bb5, .duration = sixth},    {.pitch = REST, .duration = quarter},
	{.pitch = C5, .duration = half},      {.pitch = REST, .duration = half},
	{.pitch = REST, .duration = quarter}, {.pitch = C6, .duration = quarter}};
const size_t song_golioth_notes = ARRAY_SIZE(song_golioth);
