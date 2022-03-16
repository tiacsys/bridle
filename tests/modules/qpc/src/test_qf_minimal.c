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

#include <qf_port.h>
#include <qassert.h>

#ifndef CONFIG_QPC_NO_QASSERT
//	Q_DEFINE_THIS_FILE
#endif


typedef struct MyAO
{
	QActive super;
	int my_state;
} MyAO_t;

static MyAO_t dut;

static QState MyAO_active(MyAO_t *me, QEvt const *e)
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

static QState MyAO_initial(MyAO_t *me, QEvt const *e)
{
	me->my_state++;
	return Q_TRAN(&MyAO_active);
}

static void MyAO_ctor(void)
{
	MyAO_t *me = &dut;
	QActive_ctor(&me->super, (QStateHandler)&MyAO_initial);
	me->my_state = 0;
}


ZTEST_SUITE(qf_minimal, NULL, NULL, NULL, NULL, NULL);

/**
 * @brief Test QHsm ctor functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qf_minimal, test_can_construct_AO)
{
	MyAO_ctor();	
	zassert_true(dut.my_state==0, "state machine ctor not called");

}

/**
 * @brief Test QHsm init functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qf_minimal, test_can_initialize_AO)
{
//	QHsm *const Q_dut = (QHsm *)&dut;

//	QHSM_INIT(Q_dut, NULL, NULL);
//	zassert_true(dut.my_state==3, "active state initialized and entered");

}

