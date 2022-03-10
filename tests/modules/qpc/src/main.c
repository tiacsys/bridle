/*
 * Copyright (c) 2021 TiaC Systems
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr.h>
#include <ztest.h>

#include <qep.h>


/**
 * @defgroup module_qpc_tests QPC Tests
 * @ingroup all_tests
 * @{
 * @}
 *
 */

typedef struct MyHsm
{
	QHsm super;
	int my_state;
} MyHsm_t;
MyHsm_t dut;

QState MyHsm_active(MyHsm_t *me, QEvt const *e)
{
	QState status;

    switch (e->sig) {
         case Q_ENTRY_SIG: {
             printk("enter active\n");
			 me->my_state++;
             status = Q_HANDLED();
             break;
         }
         case Q_EXIT_SIG: {
             printk("leaving active\n");
			 status = Q_HANDLED();
             break;
         }

		 case Q_INIT_SIG:{
			 printk("init active\n");
			 me->my_state++;
			 status = Q_SUPER(&QHsm_top);
			 break;
		 }

         default: {
			 printk("defer to super state\n");
             status = Q_SUPER(&QHsm_top);
             break;
         }
     }
	return status;
}

QState MyHsm_initial(MyHsm_t *me, QEvt const *e)
{
	return Q_TRAN(&MyHsm_active);
}

void MyHsm_ctor(void)
{
	MyHsm_t *me = &dut;
	QHsm_ctor(&me->super, (QStateHandler)&MyHsm_initial);
	me->my_state = 0;

}

/**
 * @brief Test QHsm functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
static void test_can_construct_Hsm(void)
{
	QHsm *const Q_dut = (QHsm *)&dut;
	MyHsm_ctor();	
	zassert_true(dut.my_state==0, "state machine ctor not called");

	QHsm_init_(Q_dut,NULL);
	zassert_true(dut.my_state==2, "active state initialized and entered");
}

void test_main(void)
{
	ztest_test_suite(common,
					 ztest_unit_test(test_can_construct_Hsm));

	ztest_run_test_suite(common);
}
