/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_folksong[] = {
	/* 2/4 */
	{.note = C5, .duration = quarter},
	{.note = D5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = E5, .duration = quarter},
	{.note = F5, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = A5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = H5, .duration = half},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = C6, .duration = half},
	/* bar */
	{.note = C5, .duration = quarter},
	{.note = D5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = E5, .duration = quarter},
	{.note = F5, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = A5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = H5, .duration = quarter},
	{.note = D6, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = C6, .duration = half},
	{.note = REST, .duration = half},
	/* bar */
	{.note = A5, .duration = quarter},
	{.note = F5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = C6, .duration = quarter},
	{.note = H5, .duration = eighth},
	{.note = A5, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = H5, .duration = half},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = C6, .duration = half},
	/* bar */
	{.note = A5, .duration = quarter},
	{.note = F5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = C6, .duration = quarter},
	{.note = H5, .duration = eighth},
	{.note = A5, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = H5, .duration = quarter},
	{.note = D6, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = C6, .duration = half},
};
const size_t song_folksong_notes = ARRAY_SIZE(song_folksong);
