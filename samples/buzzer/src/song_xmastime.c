/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const struct note_duration song_xmastime[] = {
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
	{.note = G6, .duration = eighth},
	{.note = REST, .duration = eighth},
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
	{.note = G6, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = H6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = Cs7, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = D7, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = Cs7, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = H6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = A6, .duration = (half+quarter)},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = E6, .duration = (quarter+eighth)},
	{.note = Fs6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = E6, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = Fs6, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = G6, .duration = (quarter+eighth)},
	{.note = A6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = G6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = Fs6, .duration = (quarter+eighth)},
	{.note = G6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = Fs6, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = G6, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = A6, .duration = (quarter+eighth)},
	{.note = H6, .duration = sixteenth},
	{.note = REST, .duration = sixteenth},
	{.note = A6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = D7, .duration = quarter},
	{.note = Cs7, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = H6, .duration = quarter},
	{.note = A6, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = D7, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = H6, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = A6, .duration = eighth},
	{.note = REST, .duration = eighth},
	{.note = G6, .duration = eighth},
	{.note = REST, .duration = eighth},
	/* bar */
	{.note = Fs6, .duration = quarter},
	{.note = REST, .duration = quarter},
	{.note = E6, .duration = quarter},
	{.note = REST, .duration = quarter},
	/* bar */
	{.note = D6, .duration = whole},
};
const size_t song_xmastime_notes = ARRAY_SIZE(song_xmastime);
