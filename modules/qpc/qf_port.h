#ifndef __QF_PORT
#define __QF_PORT

#include <zephyr.h>

#include "qep_port.h"

#ifdef CONFIG_QPC_AO_SUPPORT

#define QF_CRIT_ENTRY(dummy)    
#define QF_CRIT_EXIT(dummy)

#include "qv_port.h"
#include "qf.h"


#endif //CONFIG_QPC_AO_SUPPORT
#endif