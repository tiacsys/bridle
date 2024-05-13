/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef __SONGS_H__
#define __SONGS_H__

#include "notes.h"
#include <zephyr/init.h>

enum song_choice {
	beep,
	folksong,
	xmastime,
	funkytown,
	mario,
	golioth,
	tiacsys,
};

extern const size_t song_beep_notes;
extern const struct note_duration song_beep[];

extern const size_t song_folksong_notes;
extern const struct note_duration song_folksong[];

extern const size_t song_xmastime_notes;
extern const struct note_duration song_xmastime[];

extern const size_t song_funkytown_notes;
extern const struct note_duration song_funkytown[];

extern const size_t song_mario_notes;
extern const struct note_duration song_mario[];

extern const size_t song_golioth_notes;
extern const struct note_duration song_golioth[];

extern const size_t song_tiacsys_notes;
extern const struct note_duration song_tiacsys[];

#endif /* __SONGS_H__ */
