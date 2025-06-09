#include "usr_app.h"
#include "net_task_skeleton.h"

// Flash VCs (BMS - Cloud)
__attribute__((section(".data_flash")))
const char vc_cloud_1 [] = "{\"@context\":[\"https://www.w3.org/2018/credentials/v1\",\"http://localhost:8443/docs/vc.schema.html\"],\"id\":\"urn:uuid:cc4e69d7-b7f7-4155-ac8b-5af63df4472a\",\"type\":[\"VerifiableCredential\",\"ServiceAccess\"],\"issuer\":\"did:batterypass:bms.sn-987654321\",\"holder\":\"did:batterypass:service.tuv-sued-42\",\"issuanceDate\":\"2025-07-04T07:45:00Z\",\"expirationDate\":\"2027-07-04T07:45:00Z\",\"credentialSubject\":{\"id\":\"did:batterypass:service.tuv-sued-42\",\"type\":\"ServiceAccess\",\"bmsDid\":\"did:batterypass:bms.sn-987654321\",\"accessLevel\":[\"read\"],\"validFrom\":\"2025-07-04T07:45:00Z\",\"validUntil\":\"2027-07-04T07:45:00Z\"},\"proof\":{\"type\":\"EcdsaSecp256r1Signature2019\",\"created\":\"2025-07-04T07:45:05Z\",\"verificationMethod\":\"did:batterypass:bms.sn-987654321#device-key\",\"proofPurpose\":\"assertionMethod\",\"jws\":\"eyJhbGciOiJFUzI1NiJ9..BASE64_SIG\"}}";

__attribute__((section(".data_flash")))
const int number_of_vcs = 1;

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
        sending_and_receiving_functionality(1);
        for (;;)
        {
            for (uint8_t i = 0; i < number_of_vcs; i++)
            {
                ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
                char did_docment[1024] = {RESET_VALUE};
                size_t did_document_length = RESET_VALUE;
                // Request DID-Documents for VCs 
                /* @Matthias */
                xMessageBufferSend(net_crypto_message_buffer, (void *)did_document, did_document_length, pdMS_TO_TICKS(1000)); 
            }
            for (uint8_t i = 0; i < number_of_vcs; i++)
            {
                sending_and_receiving_functionality(0);
            }
        }
    }
}

void sending_and_receiving_functionality(int retrieve_did)
{
    char gp_remote_ip_address[MAX_IPV4_SIZE] = {RESET_VALUE};
    char endpoint_dns[MAX_ENDPOINT_DNS_SIZE] = {RESET_VALUE};
    int endpoint_reachable = RESET_VALUE; // 1 = reachable; 0 = not reachable
    size_t endpoint_dns_length = RESET_VALUE;
    do {
        endpoint_dns_length = xMessageBufferReceive(crypto_net_message_buffer, (void *)endpoint_dns, MAX_ENDPOINT_DNS_SIZE, pdMS_TO_TICKS(1000));
    } while (endpoint_dns_length == 0);
    dnsQuerryFunc(endpoint_dns, gp_remote_ip_address);
    for (int i = 0; i < 4; i++) {
        if (!vSendPing(gp_remote_ip_address)) { endpoint_reachable = 1; }
        vTaskDelay(100);
    }
    if (endpoint_reachable) 
    {
        xTaskNotifyGive(init_thread);
        char cReceivedString[2048] = {RESET_VALUE};
        size_t xReceivedBytes = RESET_VALUE;
        do {
            xReceivedBytes = xMessageBufferReceive(crypto_net_message_buffer, (void *)cReceivedString, sizeof(cReceivedString), pdMS_TO_TICKS(1000));
        } while (xReceivedBytes == 0);
        if (retrieve_did) 
        {
            // Logic to retrieve did from client
            char did[DID_LENGTH] = {RESET_VALUE};
            /* @Matthias */

            xMessageBufferSend(net_crypto_message_buffer, (void *)did, DID_LENGTH, pdMS_TO_TICKS(1000));
        } else 
        {
            // Logic to send dynamic battery data message to cloud endpoint
            /* @Matthias */
        }
    }
}
