/**
 * @defgroup module_qpc_tests QPC Tests
 * @ingroup all_tests
 * @{
 * @file
 * @brief Test suite: Hierarchical QHsm
 * @}
 *
 */
#include <zephyr.h>
#include <ztest.h>

#include <qep_port.h>
#include <qassert.h>

#ifndef CONFIG_QPC_NO_QASSERT
Q_DEFINE_THIS_MODULE("test_hierarchical")
#endif

typedef struct MyHsm
{
    QHsm super;
} MyHsm_t;

enum MyHsmSignals
{
    ACTIVATE_SIG = Q_USER_SIG,
    DEACTIVATE_SIG,
    TOGGLE_SIG,
    MAX_SIG
};

static MyHsm_t dut;
static QState MyHsm_active(MyHsm_t *me, QEvt const *e);
static QState MyHsm_active_collecting(MyHsm_t *me, QEvt const *e);
static QState MyHsm_active_storing(MyHsm_t *me, QEvt const *e);

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

    case Q_INIT_SIG:
    {
        printk("init active\n");
        status = Q_TRAN(&MyHsm_active_collecting);
        break;
    }

    case DEACTIVATE_SIG:
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

static QState MyHsm_active_collecting(MyHsm_t *me, QEvt const *e)
{
    QState status;

    switch (e->sig)
    {
    case Q_ENTRY_SIG:
    {
        printk("enter active.collecting\n");
        status = Q_HANDLED();
        break;
    }
    case Q_EXIT_SIG:
    {
        printk("leaving active.collecting\n");
        status = Q_HANDLED();
        break;
    }

    case TOGGLE_SIG:
    {
        status = Q_TRAN(&MyHsm_active_storing);
        break;
    }

    default:
    {
        status = Q_SUPER(&MyHsm_active);
        break;
    }
    }
    return status;
}

static QState MyHsm_active_storing(MyHsm_t *me, QEvt const *e)
{
    QState status;

    switch (e->sig)
    {
    case Q_ENTRY_SIG:
    {
        printk("enter active.storing\n");
        status = Q_HANDLED();
        break;
    }
    case Q_EXIT_SIG:
    {
        printk("leaving active.storing\n");
        status = Q_HANDLED();
        break;
    }

    case TOGGLE_SIG:
    {
        status = Q_TRAN(&MyHsm_active_collecting);
        break;
    }

    default:
    {
        status = Q_SUPER(&MyHsm_active);
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

static void *suite_setup()
{
    printk("setup suite\n");
    return NULL;
}

static void suite_before_each_test()
{
    QHsm *const Q_dut = (QHsm *)&dut;

    printk("reset state machine object\n");
    MyHsm_ctor();
    QHSM_INIT(Q_dut, NULL, NULL);
}

ZTEST_SUITE(qpc_hierarchical, NULL, suite_setup, suite_before_each_test, NULL, NULL);

/**
 * @brief Test QHsm init functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qpc_hierarchical, test_when_init_then_active_collecting)
{
    QHsm *const Q_dut = (QHsm *)&dut;

    zassert_true(QHsm_state(Q_dut) == Q_STATE_CAST(MyHsm_active_collecting), "active.collecting state not reached");
}

/**
 * @brief Test QHsm child to child state transition
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qpc_hierarchical, test_when_active_then_toggle_between_substates)
{
    QEvt e;
    QHsm *const Q_dut = (QHsm *)&dut;

    e.sig = TOGGLE_SIG;

    QHSM_DISPATCH(Q_dut, &e, NULL);
    zassert_true(QHsm_state(Q_dut) == Q_STATE_CAST(MyHsm_active_storing), "active.storing state not reached");

    QHSM_DISPATCH(Q_dut, &e, NULL);
    zassert_true(QHsm_state(Q_dut) == Q_STATE_CAST(MyHsm_active_collecting), "active.collecting state not reached");
}


/**
 * @brief Test QHsm leave any child state functionality
 *
 * @ingroup module_qpc_tests QPC Tests
 *
 *
 */
ZTEST(qpc_hierarchical, test_when_active_and_deactivate_then_inactive)
{
    QEvt e;
    QHsm *const Q_dut = (QHsm *)&dut;

    e.sig = DEACTIVATE_SIG;

    QHSM_DISPATCH(Q_dut, &e, NULL);

    zassert_true(QHsm_state(Q_dut) == Q_STATE_CAST(MyHsm_inactive), "inactive state not reached");
}
