/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const note_t song_folksong[] = {
	/* 2/4 */
	{.pitch = C5, .duration = quarter},
	{.pitch = D5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = E5, .duration = quarter},
	{.pitch = F5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = G5, .duration = quarter},
	{.pitch = A5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = G5, .duration = half},
	/* bar */
	{.pitch = F5, .duration = quarter},
	{.pitch = D5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = H5, .duration = half},
	/* bar */
	{.pitch = G5, .duration = quarter},
	{.pitch = E5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = C6, .duration = half},
	/* bar */
	{.pitch = C5, .duration = quarter},
	{.pitch = D5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = E5, .duration = quarter},
	{.pitch = F5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = G5, .duration = quarter},
	{.pitch = A5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = G5, .duration = half},
	/* bar */
	{.pitch = F5, .duration = quarter},
	{.pitch = D5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = H5, .duration = quarter},
	{.pitch = D6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = C6, .duration = half},
	{.pitch = REST, .duration = half},
	/* bar */
	{.pitch = A5, .duration = quarter},
	{.pitch = F5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = C6, .duration = quarter},
	{.pitch = H5, .duration = eighth},
	{.pitch = A5, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	/* bar */
	{.pitch = G5, .duration = quarter},
	{.pitch = E5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = G5, .duration = half},
	/* bar */
	{.pitch = F5, .duration = quarter},
	{.pitch = D5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = H5, .duration = half},
	/* bar */
	{.pitch = G5, .duration = quarter},
	{.pitch = E5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = C6, .duration = half},
	/* bar */
	{.pitch = A5, .duration = quarter},
	{.pitch = F5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = C6, .duration = quarter},
	{.pitch = H5, .duration = eighth},
	{.pitch = A5, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	/* bar */
	{.pitch = G5, .duration = quarter},
	{.pitch = E5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = G5, .duration = half},
	/* bar */
	{.pitch = F5, .duration = quarter},
	{.pitch = D5, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = H5, .duration = quarter},
	{.pitch = D6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = C6, .duration = half},
};
const size_t song_folksong_notes = ARRAY_SIZE(song_folksong);
