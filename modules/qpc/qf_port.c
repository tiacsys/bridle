#define QP_IMPL

#include <sys/__assert.h>

#include "qf_port.h"
#include "qf_pkg.h"
#include "qassert.h"

//Q_DEFINE_THIS_MODULE("qf_port")

void QF_init(void){
    /*empty for Zephyr*/
}

void QActive_start_(QActive * const me, uint_fast8_t prio,
                    QEvt const * * const qSto, uint_fast16_t const qLen,
                    void * const stkSto, uint_fast16_t const stkSize,
                    void const * const par)
{
__ASSERT(false, "not implemented");
}