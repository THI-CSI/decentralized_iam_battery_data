#include "usr_app.h"
#include "net_task.h"
#include "net_task_skeleton.h"
#include "common_utils.h"

/* @Matthias */
/* // Flash VCs (BMS - Cloud)
__attribute__((section(".data_flash")))
const char vc_cloud_1 [] = "xy";
.
.
.
__attribute__((section(".data_flash")))
const int number_of_vcs = x; */

/*******************************************************************************************************************//**
* @brief      This is the User Thread for the EP.
* @param[in]  Thread specific parameters
* @retval     None
**********************************************************************************************************************/
void net_task_entry(void *pvParameters)
{
    FSP_PARAMETER_NOT_USED (pvParameters);
    BaseType_t status = pdFALSE;
    TickType_t Semphr_wait_ticks = pdMS_TO_TICKS(500);

    // FreeRTOS IP Initialization: This init initializes the IP stack
    status = FreeRTOS_IPInit(ucIPAddress, ucNetMask, ucGatewayAddress, ucDNSServerAddress, ucMACAddress);
    if(pdFALSE == status)
    {
        APP_ERR_PRINT("FreeRTOS_IPInit Failed");
        APP_ERR_TRAP(status);
    }

    if (SUCCESS == isNetworkUp()) {
        sending_and_receiving_functionality();
        for (;;)
        {
            xSemaphoreTake(crypto_net_sem, portMAX_DELAY); // waits ~ 50 days
            for (uint8_t i = 0; i < number_of_vcs; i++)
            {
                char did_document[1024] = {RESET_VALUE};
                size_t did_document_length = RESET_VALUE;
                // Request DID-Documents for VCs
                /* @Matthias */
                vTaskDelay(pdMS_TO_TICKS(2000));
                xMessageBufferSend(net_crypto_message_buffer, (void *)did_document, did_document_length, pdMS_TO_TICKS(1000));
            }
            for (uint8_t i = 0; i < number_of_vcs; i++)
            {
                sending_and_receiving_functionality();
            }
        }
	}
}

void sending_and_receiving_functionality()
{
	char gp_remote_ip_address[MAX_IPV4_SIZE] = {RESET_VALUE};
    char endpoint_dns[MAX_ENDPOINT_DNS_SIZE] = {RESET_VALUE};
    const char ack = 'A';
    int endpoint_reachable = RESET_VALUE; // 1 = reachable; 0 = not reachable
    size_t endpoint_dns_length = RESET_VALUE;
    do {
        endpoint_dns_length = xMessageBufferReceive(crypto_net_message_buffer, (void *)endpoint_dns, MAX_ENDPOINT_DNS_SIZE, pdMS_TO_TICKS(500));
    } while (endpoint_dns_length == 0);
    dnsQuerryFunc(endpoint_dns, gp_remote_ip_address);
    for (int i = 0; i < 4; i++) {
        if (!vSendPing(gp_remote_ip_address)) { endpoint_reachable = 1; }
        vTaskDelay(100);
    }
    if (endpoint_reachable)
    {
    	xMessageBufferSend(net_crypto_message_buffer, (void *)&ack, ACK_LENGTH, pdMS_TO_TICKS(1000));
        char cReceivedString[600] = {RESET_VALUE};
        size_t xReceivedBytes = RESET_VALUE;
        do {
            xReceivedBytes = xMessageBufferReceive(crypto_net_message_buffer, (void *)cReceivedString, sizeof(cReceivedString), pdMS_TO_TICKS(1000));
        } while (xReceivedBytes == 0);
		// Logic to send signing public key to OEM client or
        // dynamic battery data message to cloud endpoint 
		/* @Matthias */
    }
}
