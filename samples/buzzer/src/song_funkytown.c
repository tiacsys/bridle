/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const note_t song_funkytown[] = {
	{.pitch = C5, .duration = quarter}, {.pitch = REST, .duration = eighth},
	{.pitch = C5, .duration = quarter}, {.pitch = Bb4, .duration = quarter},
	{.pitch = C5, .duration = quarter}, {.pitch = REST, .duration = quarter},
	{.pitch = G4, .duration = quarter}, {.pitch = REST, .duration = quarter},
	{.pitch = G4, .duration = quarter}, {.pitch = C5, .duration = quarter},
	{.pitch = F5, .duration = quarter}, {.pitch = E5, .duration = quarter},
	{.pitch = C5, .duration = quarter},
};
const size_t song_funkytown_notes = ARRAY_SIZE(song_funkytown);
