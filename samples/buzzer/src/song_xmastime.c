/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_xmastime[] =
{
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = H6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = A6, .duration = (quarter+sixteenth)},
	{.note = REST, .duration = sixteenth},
	{.note = G6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = Fs6, .duration = quarter},
	{.note = G6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = H6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = A6, .duration = (quarter+sixteenth)},
	{.note = REST, .duration = sixteenth},
	{.note = G6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = Fs6, .duration = quarter},
	{.note = G6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = H6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = Cs7, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = D7, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = Cs7, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = H6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = A6, .duration = (half+quarter)},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = E6, .duration = (quarter+eigth)},
	{.note = Fs6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = E6, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = Fs6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = G6, .duration = (quarter+eigth)},
	{.note = A6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = G6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = Fs6, .duration = (quarter+eigth)},
	{.note = G6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = Fs6, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = G6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = A6, .duration = (quarter+eigth)},
	{.note = H6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = D7, .duration = quarter},
	{.note = Cs7, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = H6, .duration = quarter},
	{.note = A6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = D7, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = H6, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = A6, .duration = eigth},
	{.note = REST, .duration = eigth},
	{.note = G6, .duration = eigth},
	{.note = REST, .duration = eigth},
	/* bar */
	{.note = Fs6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = E6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = D6, .duration = whole},
};
const size_t song_xmastime_notes = ARRAY_SIZE(song_xmastime);
