#include <zephyr.h>
#include <sys/__assert.h>

#include <qpc.h>

#ifndef CONFIG_QPC_NO_ASSERT

/*..........................................................................*/
Q_NORETURN Q_onAssert(char_t const *const module, int_t const loc)
{

    __ASSERT(false, "QPC assertion raised in %s on line %d", module, loc);

    // execution will not reach this point, yet to satisfy the Q_NORETURN signature
    // make it explicit that this function never returns
    for (;;)
    {
    }
}

#endif