#include "r_usb_basic.h"
#include "r_usb_basic_api.h"
#include "usb_thread.h"

/* USB Thread entry function */
/* pvParameters contains TaskHandle_t */

#define BUFFER_SIZE  64
static uint8_t rx_buf[BUFFER_SIZE];
static uint8_t tx_buf[BUFFER_SIZE];
volatile bool usb_read_complete = false;
volatile bool usb_write_complete = false;
extern bsp_leds_t g_bsp_leds;

#define USB_EP_PACKET_SIZE                        (512U)
#define OFF                                       (0U)
#define ON                                        (1U)

#define BLUE                                      (BSP_LED_LED1)
#define GREEN                                     (BSP_LED_LED2)
#define RED                                       (BSP_LED_LED3)
#define TURN_RED_ON                               R_IOPORT_PinWrite(&g_ioport_ctrl, g_bsp_leds.p_leds[RED], ON); \
		                                          R_IOPORT_PinWrite(&g_ioport_ctrl, g_bsp_leds.p_leds[GREEN], OFF);\
		                                          R_IOPORT_PinWrite(&g_ioport_ctrl, g_bsp_leds.p_leds[BLUE], OFF);


void usb_thread_entry(void * pvParameters)
{
        fsp_err_t err;

    // Open USB peripheral in device mode
    err = R_USB_Open(&g_basic0_ctrl, &g_basic0_cfg);
    if (err != FSP_SUCCESS)
    {
        // Error handling: stop here
		TURN_RED_ON
        while(1);
    }
	
	usb_status_t status = {0};
    while (1)
    {
		err = R_USB_EventGet(&g_basic0_ctrl, &status);
        if (err == FSP_SUCCESS)
        {
            // Echo back received data (blocking)
            memcpy(tx_buf, rx_buf, BUFFER_SIZE);
            err = R_USB_Write(&g_basic0_ctrl, tx_buf, BUFFER_SIZE, USB_PIPE1);
			TURN_RED_ON
            if (err != FSP_SUCCESS)
            {
                
            }
        } else {
			TURN_RED_ON
		}

        // You may add delay here if needed (e.g. R_BSP_SoftwareDelay)
    }
}
