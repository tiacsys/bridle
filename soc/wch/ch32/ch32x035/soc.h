#ifndef SOC_H
#define SOC_H

#ifndef _ASMLANGUAGE
#include <ch32x035.h>
#include <ch32x035_adc.h>
#include <ch32x035_dma.h>
#include <ch32x035_gpio.h>
#include <ch32x035_pwr.h>
#include <ch32x035_rcc.h>
#include <ch32x035_usart.h>
#include <ch32x035_usbpd.h>

// bug with an extra extern "C"...
#ifndef __CH32X035_USB_H
#include <ch32x035_usb.h>
#ifdef __cplusplus
}
#endif
#endif

#endif

#include <soc_common.h>

#endif // SOC_H
