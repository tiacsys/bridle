/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2022 Golioth, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "buzzer.h"

#include <zephyr/kernel.h>
#include <zephyr/init.h>

/* Logging */
#include <zephyr/logging/log.h>
LOG_MODULE_DECLARE(buzzersh, CONFIG_BUZZER_SHELL_LOG_LEVEL);

/* Buzzer thread structs */
static k_tid_t buzzer_tid;
static struct k_thread buzzer_thread;
static struct buzzer_instance *buzzer_instance;
K_THREAD_STACK_DEFINE(buzzer_stack, 1024);
K_SEM_DEFINE(buzzer_initialized_sem, 0, 1);	// wait until buzzer is ready

#define BUZZER_MAX_FREQ 2500
#define BUZZER_MIN_FREQ 10

/* extern */ void buzzer_entry(void *p0, void *p1, void *p2)
{
	buzzer_instance = (struct buzzer_instance *)(p0);

	/* block until buzzer is available */
	k_sem_take(&buzzer_initialized_sem, K_FOREVER);

	while (1)
	{
		const struct pwm_dt_spec *pwm = &(buzzer_instance->dt_spec);
		const struct note_duration *replay;	// the song with ...
		size_t notes;	// ... number of notes in replay

		switch (buzzer_instance->song)
		{
		case beep:
			LOG_DBG("beep");
			replay = song_beep;
			notes = song_beep_notes;
			break;

		case folksong:
			LOG_DBG("folksong");
			replay = song_folksong;
			notes = song_folksong_notes;
			break;

		case xmastime:
			LOG_DBG("xmastime");
			replay = song_xmastime;
			notes = song_xmastime_notes;
			break;

		case funkytown:
			LOG_DBG("funkytown");
			replay = song_funkytown;
			notes = song_funkytown_notes;
			break;

		case mario:
			LOG_DBG("mario");
			replay = song_mario;
			notes = song_mario_notes;
			break;

		case golioth:
			LOG_DBG("golioth");
			replay = song_golioth;
			notes = song_golioth_notes;
			break;

		case tiacsys:
			LOG_DBG("tiacsys");
			replay = song_tiacsys;
			notes = song_tiacsys_notes;
			break;

		default:
			LOG_WRN("Warning: invalid song selection");
			replay = NULL;
			notes = 0;
			break;
		}

		/* if song, then ... */
		if (replay && notes)
		{
			/* ... replay the song */
			for (int i = 0; i < notes; i++)
			{
				int note = replay[i].note;
				int duration = replay[i].duration;

				if (note < BUZZER_MIN_FREQ)
				{
					/* 'pause' on frequency notes */
					pwm_set_pulse_dt(pwm, 0);
					k_msleep(duration);
				}
				else
				{
					pwm_set_dt(pwm, PWM_HZ(note),
							PWM_HZ(note) / 2);
					k_msleep(duration);
				}
			}
		}

		/* turn buzzer off (pulse duty to 0) */
		pwm_set_pulse_dt(pwm, 0);

		/* sleep thread again until awoken externally */
		k_sleep(K_FOREVER);
	}
}

int app_buzzer_init(struct buzzer_instance *buzzer)
{
	if (!device_is_ready(buzzer->dt_spec.dev))
	{
		return -ENODEV;
	}

	buzzer_tid = k_thread_create(&buzzer_thread,
			buzzer_stack, K_THREAD_STACK_SIZEOF(buzzer_stack),
			buzzer_entry, buzzer, NULL, NULL,
			K_LOWEST_APPLICATION_THREAD_PRIO, 0, K_SECONDS(2));
	k_sem_give(&buzzer_initialized_sem);
	return 0;
}

void app_buzzer_play_song(enum song_choice song)
{
	if (buzzer_instance) buzzer_instance->song = song;
	k_wakeup(buzzer_tid);
}
