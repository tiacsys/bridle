/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_folksong[] =
{
	/* 2/4 */
	{.note = C5, .duration = quarter},
	{.note = D5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = E5, .duration = quarter},
	{.note = F5, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = A5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = H5, .duration = half},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = C6, .duration = half},
	/* bar */
	{.note = C5, .duration = quarter},
	{.note = D5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = E5, .duration = quarter},
	{.note = F5, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = A5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = H5, .duration = quarter},
	{.note = D6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = C6, .duration = half},
	{.note = REST, .duration = half},
	/* bar */
	{.note = A5, .duration = quarter},
	{.note = F5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = C6, .duration = quarter},
	{.note = H5, .duration = eigth},
	{.note = A5, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = H5, .duration = half},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = C6, .duration = half},
	/* bar */
	{.note = A5, .duration = quarter},
	{.note = F5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = C6, .duration = quarter},
	{.note = H5, .duration = eigth},
	{.note = A5, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	/* bar */
	{.note = G5, .duration = quarter},
	{.note = E5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = G5, .duration = half},
	/* bar */
	{.note = F5, .duration = quarter},
	{.note = D5, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = H5, .duration = quarter},
	{.note = D6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = C6, .duration = half},
};
const size_t song_folksong_notes = ARRAY_SIZE(song_folksong);
