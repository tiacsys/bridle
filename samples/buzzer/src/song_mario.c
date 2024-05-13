/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_mario[] = {
	{.note = E6, .duration = quarter},
	{.note = REST, .duration = eighth},
	{.note = E6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = E6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = C6, .duration = quarter},
	{.note = E6, .duration = half},
	{.note = G6, .duration = half},
	{.note = REST, .duration = quarter},
	{.note = G4, .duration = whole},
	{.note = REST, .duration = whole},
	/* break in sound */
	{.note = C6, .duration = half},
	{.note = REST, .duration = quarter},
	{.note = G5, .duration = half},
	{.note = REST, .duration = quarter},
	{.note = E5, .duration = half},
	{.note = REST, .duration = quarter},
	{.note = A5, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = B5, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = Bb5, .duration = quarter},
	{.note = A5, .duration = half},
	{.note = G5, .duration = quarter},
	{.note = E6, .duration = quarter},
	{.note = G6, .duration = quarter},
	{.note = A6, .duration = half},
	{.note = F6, .duration = quarter},
	{.note = G6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = E6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = C6, .duration = quarter},
	{.note = D6, .duration = quarter},
	{.note = B5, .duration = quarter},
};
const size_t song_mario_notes = ARRAY_SIZE(song_mario);
