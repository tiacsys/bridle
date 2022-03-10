/**
* @file
* @brief QEP/C port for GCC
* @ingroup qep port
* @cond
******************************************************************************
* taken from qpc/ports/arm-cm/qv/gnu/qep_port.h* 
******************************************************************************
* @endcond
*/
#ifndef QEP_PORT_H
#define QEP_PORT_H

/*! no-return function specifier (GCC-ARM compiler) */
#define Q_NORETURN   __attribute__ ((noreturn)) void

#include <stdint.h>  /* Exact-width types. WG14/N843 C99 Standard */
#include <stdbool.h> /* Boolean type.      WG14/N843 C99 Standard */

#include "qep.h"     /* QEP platform-independent public interface */

#endif /* QEP_PORT_H */