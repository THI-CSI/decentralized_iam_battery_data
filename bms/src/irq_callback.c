#include "common_utils.h"

/*******************************************************************************************************************//**
 *  @brief       Interrupt callback routine.
 *  @param[in]   p_args     Callback function parameter data.
 *  @retval      None
 **********************************************************************************************************************/
void irq_callback(rtc_callback_args_t *p_args)
{
    if(RTC_EVENT_ALARM_IRQ == p_args->event)
    {
        FSP_PARAMETER_NOT_USED(p_args);
        // Variable is set to true if priority of unblocked task is higher
        // than the task that was in running state when interrupt occurred
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        xSemaphoreGiveFromISR (bms_cloud_sem , &xHigherPriorityTaskWoken);
        portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
    }
    // other IRQ
}
