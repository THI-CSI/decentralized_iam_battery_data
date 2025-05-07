#ifndef BMS_FREERTOS_DNS_GLOBALS
#define BMS_FREERTOS_DNS_GLOBALS

#include <FreeRTOS_DNS_Globals.h>
//#include "../ra-lib/ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/include/FreeRTOS_DNS_Globals.h"

#if ( ipconfigBYTE_ORDER == pdFREERTOS_LITTLE_ENDIAN )
    #define dnsDNS_PORT             0xB414U     /**< Little endian: Port used for DNS. */
#else
    #define dnsDNS_PORT             0x14B4U     /**< Big endian: Port used for DNS. */

#endif /* ipconfigBYTE_ORDER */

#endif /* BMS_FREERTOS_DNS_GLOBALS */