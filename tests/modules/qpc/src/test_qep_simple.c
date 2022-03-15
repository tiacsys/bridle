/**
 * @defgroup module_qpc_tests QPC Tests
 * @ingroup all_tests
 * @{
 * @file
 * @brief Test suite: Simple QHsm
 * @}
 *
 */
#include <zephyr.h>
#include <ztest.h>

#include <qep_port.h>
#include <qassert.h>

#ifndef CONFIG_QPC_NO_QASSERT
Q_DEFINE_THIS_MODULE("test_simple")
#endif

typedef struct MyHsm
{
	QHsm super;
} MyHsm_t;

enum MyHsmSignals
{
	TOGGLE_SIG = Q_USER_SIG,
	MAX_SIG
};

static MyHsm_t dut;
static QState MyHsm_active(MyHsm_t *me, QEvt const *e);
static QState MyHsm_inactive(MyHsm_t *me, QEvt const *e);

static QState MyHsm_active(MyHsm_t *me, QEvt const *e)
{
	QState status;

	switch (e->sig)
	{
	case Q_ENTRY_SIG:
	{
		printk("enter active\n");
		status = Q_HANDLED();
		break;
	}
	case Q_EXIT_SIG:
	{
		printk("leaving active\n");
		status = Q_HANDLED();
		break;
	}

	case TOGGLE_SIG:
	{
		status = Q_TRAN(&MyHsm_inactive);
		break;
	}

	default:
	{
		status = Q_SUPER(&QHsm_top);
		break;
	}
	}
	return status;
}

static QState MyHsm_inactive(MyHsm_t *me, QEvt const *e)
{
	QState status;
	switch (e->sig)
	{
	case Q_ENTRY_SIG:
	{
		printk("enter inactive\n");
		status = Q_HANDLED();
		break;
	}
	case Q_EXIT_SIG:
	{
		printk("leaving inactive\n");
		status = Q_HANDLED();
		break;
	}

	case TOGGLE_SIG:
	{
		status = Q_TRAN(&MyHsm_active);
		break;
	}

	default:
	{
		status = Q_SUPER(&QHsm_top);
		break;
	}
	}
	return status;
}

static QState MyHsm_initial(MyHsm_t *me, QEvt const *e)
{
	return Q_TRAN(&MyHsm_active);
}

static void MyHsm_ctor()
{
	MyHsm_t *me = &dut;
	QHsm_ctor(&me->super, (QStateHandler)&MyHsm_initial);
}

static void suite_before_each_test()
{
	QHsm *const Q_dut = (QHsm *)&dut;

	printk("reset state machine object\n");
	MyHsm_ctor();
	QHSM_INIT(Q_dut, NULL, NULL);
}

ZTEST_SUITE(qpc_simple, NULL, NULL, suite_before_each_test, NULL, NULL);

/**
 * @brief Test QHsm init functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qpc_simple, test_when_active_and_event_then_inactive)
{
	QEvt e;
	QHsm *const Q_dut = (QHsm *)&dut;

	e.sig = TOGGLE_SIG;

	QHSM_DISPATCH(Q_dut, &e, NULL);
	zassert_true(QHsm_state(Q_dut) == Q_STATE_CAST(MyHsm_inactive), "inactive state not reached");
}

/**
 * @brief Test QHsm init functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qpc_simple, test_when_inactive_and_event_then_active)
{
	QEvt e;
	QHsm *const Q_dut = (QHsm *)&dut;

	e.sig = TOGGLE_SIG;

	QHSM_DISPATCH(Q_dut, &e, NULL);
	QHSM_DISPATCH(Q_dut, &e, NULL);
	zassert_true(QHsm_state(Q_dut) == Q_STATE_CAST(MyHsm_active), "active state not reached");
}
