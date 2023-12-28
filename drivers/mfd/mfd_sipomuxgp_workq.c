/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mfd_sipomuxgp.h"

#include <zephyr/init.h>

struct k_work_q mfd_sipomuxgp_xfr_workq;
static K_KERNEL_STACK_DEFINE(mfd_sipomuxgp_xfr_workq_stack,
		MFD_SIPOMUXGP_NUM_INSTS * CONFIG_MFD_SIPOMUXGP_XFR_WORKQUEUE_STACK_SIZE);

static int mfd_sipomuxgp_xfr_workq_init(void)
{
	struct k_work_queue_config config = {
		.name = "mfd_sipomuxgp_xfr_workq",
		.no_yield = IS_ENABLED(CONFIG_MFD_SIPOMUXGP_XFR_WORKQUEUE_NO_YIELD),
	};

	k_work_queue_start(&mfd_sipomuxgp_xfr_workq,
			   mfd_sipomuxgp_xfr_workq_stack,
			   K_KERNEL_STACK_SIZEOF(mfd_sipomuxgp_xfr_workq_stack),
			   K_PRIO_COOP(CONFIG_MFD_SIPOMUXGP_XFR_WORKQUEUE_PRIORITY),
			   &config);
	return 0;
}

SYS_INIT(mfd_sipomuxgp_xfr_workq_init, POST_KERNEL, CONFIG_KERNEL_INIT_PRIORITY_DEFAULT);
