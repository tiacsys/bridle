/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "buzzer.h"

#include <zephyr/shell/shell.h>

/* Logging */
#include <zephyr/logging/log.h>
LOG_MODULE_DECLARE(buzzersh, CONFIG_BUZZER_SHELL_LOG_LEVEL);

#include <stdlib.h>

static int cmd_buzzer_info(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	shell_print(sh, "Warning: not yet implemented.");
	return 0;
}

static int cmd_buzzer_beep(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	app_buzzer_play_song(beep);
	LOG_DBG("song played: beep");
	return 0;
}

static int cmd_buzzer_folksong(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	app_buzzer_play_song(folksong);
	LOG_DBG("song played: folksong");
	return 0;
}

static int cmd_buzzer_xmastime(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	app_buzzer_play_song(xmastime);
	LOG_DBG("song played: xmastime");
	return 0;
}

static int cmd_buzzer_funkytown(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	app_buzzer_play_song(funkytown);
	LOG_DBG("song played: funkytown");
	return 0;
}

static int cmd_buzzer_mario(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	app_buzzer_play_song(mario);
	LOG_DBG("song played: mario");
	return 0;
}

static int cmd_buzzer_golioth(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	app_buzzer_play_song(golioth);
	LOG_DBG("song played: golioth");
	return 0;
}

static int cmd_buzzer_tiacsys(const struct shell *sh,
		size_t argc, char **argv, void *data)
{
	app_buzzer_play_song(tiacsys);
	LOG_DBG("song played: tiacsys");
	return 0;
}

SHELL_STATIC_SUBCMD_SET_CREATE(buzzer_play_sub,
	SHELL_CMD(folksong, NULL, "Play the 'folksong' song", cmd_buzzer_folksong),
	SHELL_CMD(xmastime, NULL, "Play the 'folksong' song", cmd_buzzer_xmastime),
	SHELL_CMD(funkytown, NULL, "Play the 'funkytown' song", cmd_buzzer_funkytown),
	SHELL_CMD(mario, NULL, "Play the 'mario' song", cmd_buzzer_mario),
	SHELL_CMD(golioth, NULL, "Play the 'golioth' song", cmd_buzzer_golioth),
	SHELL_CMD(tiacsys, NULL, "Play the 'tiacsys' song", cmd_buzzer_tiacsys),
	SHELL_SUBCMD_SET_END
);

SHELL_STATIC_SUBCMD_SET_CREATE(buzzer_sub,
	SHELL_CMD(info, NULL, "Get buzzer info", cmd_buzzer_info),
	SHELL_CMD(beep, NULL, "Use buzzer to beep", cmd_buzzer_beep),
	SHELL_CMD(play, &buzzer_play_sub, "Play one of predefined sounds", NULL),
	SHELL_SUBCMD_SET_END
);

SHELL_CMD_REGISTER(buzzer, &buzzer_sub, "Buzzer related commands", NULL);
