/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const note_t song_mario[] = {
	{.pitch = E6, .duration = quarter},
	{.pitch = REST, .duration = eighth},
	{.pitch = E6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = E6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = C6, .duration = quarter},
	{.pitch = E6, .duration = half},
	{.pitch = G6, .duration = half},
	{.pitch = REST, .duration = quarter},
	{.pitch = G4, .duration = whole},
	{.pitch = REST, .duration = whole},
	/* break in sound */
	{.pitch = C6, .duration = half},
	{.pitch = REST, .duration = quarter},
	{.pitch = G5, .duration = half},
	{.pitch = REST, .duration = quarter},
	{.pitch = E5, .duration = half},
	{.pitch = REST, .duration = quarter},
	{.pitch = A5, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = B5, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = Bb5, .duration = quarter},
	{.pitch = A5, .duration = half},
	{.pitch = G5, .duration = quarter},
	{.pitch = E6, .duration = quarter},
	{.pitch = G6, .duration = quarter},
	{.pitch = A6, .duration = half},
	{.pitch = F6, .duration = quarter},
	{.pitch = G6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = E6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = C6, .duration = quarter},
	{.pitch = D6, .duration = quarter},
	{.pitch = B5, .duration = quarter},
};
const size_t song_mario_notes = ARRAY_SIZE(song_mario);
