#ifndef __QF_PORT
#define __QF_PORT

#include <zephyr.h>

#include "qep_port.h"

#ifdef CONFIG_QPC_AO_SUPPORT


#define QF_EQUEUE_TYPE QEQueue
#define QF_THREAD_TYPE _thread_t

#define QF_MAX_ACTIVE 32U

#define QF_INT_DISABLE()
#define QF_INT_ENABLE()

#define QF_CRIT_ENTRY(dummy)    
#define QF_CRIT_EXIT(dummy)

#include <kernel/thread.h>

#include "qequeue.h"
#include "qmpool.h"
#include "qf.h"

#ifdef QP_IMPL

#define QACTIVE_EQUEUE_WAIT_(me_)               \
    while((me_)->eQueue.frontEvt == (QEvt *)0){ \
        QF_CRIT_X_();                           \
        QF_CRIT_E_();                          \
    }                       

#define QACTIVE_EQUEUE_SIGNAL_(me_) do {    \
    QF_CRIT_X_();                           \
    QF_CRIT_E_();                           \
} while (false)

#define QF_EPOOL_TYPE_ QMPool
#define QF_EPOOL_INIT_(p_, poolSto_, poolSize_, evtSize_) \
    (QMPool_init(&(p_), (poolSto_), (poolSize_), (evtSize_)))
#define QF_EPOOL_EVENT_SIZE_(p_) ((uint_fast16_t)(p_).blockSize)
#define QF_EPOOL_GET_(p_, e_, m_, qs_id_) \
    ((e_) = (QEvt*)QMPool_get(&(p_), (m_), (qs_id_)))
#define QF_EPOOL_PUT_(p_, e_, qs_id_) \
    (QMPool_put(&(p_), (e_), (qs_id_)))


#endif // QP_IMPL

#endif //CONFIG_QPC_AO_SUPPORT
#endif