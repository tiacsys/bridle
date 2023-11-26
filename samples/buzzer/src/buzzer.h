/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2022 Golioth, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef __BUZZER_H__
#define __BUZZER_H__

#include "songs.h"

#include <zephyr/devicetree.h>
#include <zephyr/drivers/pwm.h>

struct buzzer_instance
{
	const struct pwm_dt_spec dt_spec;
	enum song_choice song;
};

int app_buzzer_init(struct buzzer_instance *buzzer);
void app_buzzer_play_song(enum song_choice song);

#endif /* __BUZZER_H__ */
