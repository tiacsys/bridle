/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "songs.h"

const note_t song_xmastime[] = {
	{.pitch = A6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = H6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = A6, .duration = (quarter + sixteenth)},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = G6, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = Fs6, .duration = quarter},
	{.pitch = G6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = A6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = H6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = A6, .duration = (quarter + sixteenth)},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = G6, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = Fs6, .duration = quarter},
	{.pitch = G6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = A6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = A6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = H6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = Cs7, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = D7, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = Cs7, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = H6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = A6, .duration = (half + quarter)},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = E6, .duration = (quarter + eighth)},
	{.pitch = Fs6, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = E6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = Fs6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = G6, .duration = (quarter + eighth)},
	{.pitch = A6, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = G6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = Fs6, .duration = (quarter + eighth)},
	{.pitch = G6, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = Fs6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = G6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = A6, .duration = (quarter + eighth)},
	{.pitch = H6, .duration = sixteenth},
	{.pitch = REST, .duration = sixteenth},
	{.pitch = A6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = D7, .duration = quarter},
	{.pitch = Cs7, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = H6, .duration = quarter},
	{.pitch = A6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = D7, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = H6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = A6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	{.pitch = G6, .duration = eighth},
	{.pitch = REST, .duration = eighth},
	/* bar */
	{.pitch = Fs6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	{.pitch = E6, .duration = quarter},
	{.pitch = REST, .duration = quarter},
	/* bar */
	{.pitch = D6, .duration = whole},
};
const size_t song_xmastime_notes = ARRAY_SIZE(song_xmastime);
