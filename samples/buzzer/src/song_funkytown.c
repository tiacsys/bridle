/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_funkytown[] = {
	{.note = C5, .duration = quarter},
	{.note = REST, .duration = eighth},
	{.note = C5, .duration = quarter},
	{.note = Bb4, .duration = quarter},
	{.note = C5, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = G4, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = G4, .duration = quarter},
	{.note = C5, .duration = quarter},
	{.note = F5, .duration = quarter},
	{.note = E5, .duration = quarter},
	{.note = C5, .duration = quarter},
};
const size_t song_funkytown_notes = ARRAY_SIZE(song_funkytown);
