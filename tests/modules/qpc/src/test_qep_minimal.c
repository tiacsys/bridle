/**
 * @defgroup module_qpc_tests QPC Tests
 * @ingroup all_tests
 * @{
 * @file
 * @brief Test suite: Minimal QHsm
 * @}
 *
 */
#include <zephyr.h>
#include <ztest.h>

#include <qep_port.h>
#include <qassert.h>

#ifndef CONFIG_QPC_NO_QASSERT
	Q_DEFINE_THIS_FILE
#endif


typedef struct MyHsm
{
	QHsm super;
	int my_state;
} MyHsm_t;

static MyHsm_t dut;

static QState MyHsm_active(MyHsm_t *me, QEvt const *e)
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

static QState MyHsm_initial(MyHsm_t *me, QEvt const *e)
{
	me->my_state++;
	return Q_TRAN(&MyHsm_active);
}

static void MyHsm_ctor(void)
{
	MyHsm_t *me = &dut;
	QHsm_ctor(&me->super, (QStateHandler)&MyHsm_initial);
	me->my_state = 0;
}


ZTEST_SUITE(qpc_minimal, NULL, NULL, NULL, NULL, NULL);

/**
 * @brief Test QHsm ctor functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qpc_minimal, test_can_construct_Hsm)
{
	MyHsm_ctor();	
	zassert_true(dut.my_state==0, "state machine ctor not called");

}

/**
 * @brief Test QHsm init functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qpc_minimal, test_can_initialize_Hsm)
{
	QHsm *const Q_dut = (QHsm *)&dut;

	QHSM_INIT(Q_dut, NULL, NULL);
	zassert_true(dut.my_state==3, "active state initialized and entered");

}

