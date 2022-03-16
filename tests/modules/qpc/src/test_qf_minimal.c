/**
 * @defgroup module_qf_tests qf Tests
 * @ingroup all_tests
 * @{
 * @file
 * @brief Test suite: Minimal QHsm
 * @}
 *
 */
#include <zephyr.h>
#include <ztest.h>

#define QP_IMPL
#include <qf_port.h>
#include <qf_pkg.h>
#include <qassert.h>

#ifndef CONFIG_qf_NO_QASSERT
	Q_DEFINE_THIS_FILE
#endif

typedef struct MyAO
{
	QActive super;
	int my_state;
} MyAO_t;

static MyAO_t dut;
static QEvt const *dutQSto[10];

static QState MyAO_active(MyAO_t *me, QEvt const *e)
{
	QState status;

	switch (e->sig)
	{
	case Q_ENTRY_SIG:
	{
		printk("enter active\n");
		me->my_state++;
		status = Q_HANDLED();
		break;
	}
	case Q_EXIT_SIG:
	{
		printk("leaving active\n");
		status = Q_HANDLED();
		break;
	}

	case Q_INIT_SIG:
	{
		printk("init active\n");
		me->my_state++;
		status = Q_SUPER(&QHsm_top);
		break;
	}

	default:
	{
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
	QActive_ctor(&me->super, Q_STATE_CAST(&MyAO_initial));
	me->my_state = 0;
}

ZTEST_SUITE(qf_minimal, NULL, NULL, NULL, NULL, NULL);

/**
 * @brief Test AO ctor functionality
 *
 * @ingroup module_qf_tests qf Tests
 *
 *
 */
ZTEST(qf_minimal, test_can_construct_AO)
{
	MyAO_ctor();
	zassert_true(dut.my_state == 0, "state machine ctor not called");
}

/**
 * @brief Test AO event init functionality
 *
 * @ingroup module_qf_tests qf Tests
 *
 *
 */
ZTEST(qf_minimal, test_can_initialize_event_queue)
{
	QActive *Q_dut = (QActive *)&dut;
	QEQueue_init(&Q_dut->eQueue, dutQSto, Q_DIM(dutQSto));
	zassert_true(Q_dut->eQueue.ring == dutQSto, "event queue not properly initialized");
	zassert_true(Q_dut->eQueue.nFree==11, "queue size not correct");
}


/**
 * @brief Test AO init functionality
 *
 * @ingroup module_qf_tests qf Tests
 *
 *
 */
ZTEST(qf_minimal, test_can_initialize_hsm)
{
	QActive *Q_dut = (QActive *)&dut;
	MyAO_ctor();

	QHSM_INIT(&Q_dut->super, NULL, 0);
	zassert_true(QHsm_state(Q_dut) == Q_STATE_CAST(MyAO_active), "active state not reached");
}

/**
 * @brief Test AO init functionality
 *
 * @ingroup module_qf_tests qf Tests
 *
 *
 */
ZTEST(qf_minimal, test_can_post_event_to_queue)
{
	QActive *Q_dut = (QActive *)&dut;
	QEvt e;
	QEvt const* f;
	MyAO_ctor();
	QEQueue_init(&Q_dut->eQueue, dutQSto, Q_DIM(dutQSto));


	QHSM_INIT(&Q_dut->super, NULL, 0);
	QACTIVE_POST(Q_dut, &e, 0);
	f = QActive_get_(Q_dut);

	zassert_equal_ptr(&e, f, "not the same event");
}
