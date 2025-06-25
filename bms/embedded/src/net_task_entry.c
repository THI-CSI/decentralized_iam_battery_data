#include <net_task_entry.h>
#include "cJSON.h"
#include "usr_app.h"
#include "net_task.h"
#include "common_utils.h"
#include "cJson.h"

/* @Matthias */
// Flash VCs (BMS - Cloud)
__attribute__((section(".data_flash")))
const char vc_cloud_1[] = "{  \"@context\": [    \"https://www.w3.org/2018/credentials/v1\",    \"http://localhost:8443/docs/vc.bmsProduction.schema.html\"  ],  \"id\": \"urn:uuid:982c43ee-3d16-419a-a2f4-5c61710f428c\",  \"type\": [    \"VerifiableCredential\",    \"BMSProduction\"  ],  \"issuer\": \"did:batterypass:bms.sn-544b51e7\",  \"holder\": \"did:batterypass:oem.sn-audi\",  \"issuanceDate\": \"2025-06-10T12:01:00Z\",  \"expirationDate\": \"2026-06-10T12:01:00Z\",  \"credentialSubject\": {    \"id\": \"did:batterypass:oem.sn-audi\",    \"type\": \"BMSProduction\",    \"bmsDid\": \"did:batterypass:bms.sn-544b51e7\",    \"timestamp\": \"2025-06-10T12:01:00Z\",    \"lotNumber\": \"LOT-775533\"  },  \"proof\": {    \"type\": \"EcdsaSecp256r1Signature2019\",    \"created\": \"2025-06-10T12:01:03Z\",    \"verificationMethod\": \"did:batterypass:bms.sn-544b51e7#key-1\",    \"proofPurpose\": \"authentication\",    \"jws\": \"eyJhbGciOiJFUzI1NiJ9.eyJAY29udGV4dCI6IFsiaHR0cHM6Ly93d3cudzMub3JnLzIwMTgvY3JlZGVudGlhbHMvdjEiLCAiaHR0cDovL2xvY2FsaG9zdDo4NDQzL2RvY3MvdmMuYm1zUHJvZHVjdGlvbi5zY2hlbWEuaHRtbCJdLCAiaWQiOiAidXJuOnV1aWQ6OTgyYzQzZWUtM2QxNi00MTlhLWEyZjQtNWM2MTcxMGY0MjhjIiwgInR5cGUiOiBbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwgIkJNU1Byb2R1Y3Rpb24iXSwgImlzc3VlciI6ICJkaWQ6YmF0dGVyeXBhc3M6Ym1zLnNuLTU0NGI1MWU3IiwgImhvbGRlciI6ICJkaWQ6YmF0dGVyeXBhc3M6b2VtLnNuLWF1ZGkiLCAiaXNzdWFuY2VEYXRlIjogIjIwMjUtMDYtMTBUMTI6MDE6MDBaIiwgImV4cGlyYXRpb25EYXRlIjogIjIwMjYtMDYtMTBUMTI6MDE6MDBaIiwgImNyZWRlbnRpYWxTdWJqZWN0IjogeyJpZCI6ICJkaWQ6YmF0dGVyeXBhc3M6b2VtLnNuLWF1ZGkiLCAidHlwZSI6ICJCTVNQcm9kdWN0aW9uIiwgImJtc0RpZCI6ICJkaWQ6YmF0dGVyeXBhc3M6Ym1zLnNuLTU0NGI1MWU3IiwgInRpbWVzdGFtcCI6ICIyMDI1LTA2LTEwVDEyOjAxOjAwWiIsICJsb3ROdW1iZXIiOiAiTE9ULTc3NTUzMyJ9LCAicHJvb2YiOiB7InR5cGUiOiAiRWNkc2FTZWNwMjU2cjFTaWduYXR1cmUyMDE5IiwgImNyZWF0ZWQiOiAiMjAyNS0wNi0xMFQxMjowMTowM1oiLCAidmVyaWZpY2F0aW9uTWV0aG9kIjogImRpZDpiYXR0ZXJ5cGFzczpibXMuc24tNTQ0YjUxZTcja2V5LTEiLCAicHJvb2ZQdXJwb3NlIjogImF1dGhlbnRpY2F0aW9uIiwgImp3cyI6ICIifX0.FGuVZ-NqZ6VfHc-FSfqLzwkNAyFl8ncWkQ5-z0NvuUf5aIMAwS67pE1bpBqmlUAx3cb7Xwn1KzM0BMtQxowioQ\"  }}";
__attribute__((section(".data_flash")))
const int number_of_vcs = 1;

/**
*	Static IP config, since no DHCP is being used
*/

static  uint8_t ucMACAddress[ 6 ]       = {0x00, 0x11, 0x22, 0x33, 0x44, 0x55};
static  uint8_t ucIPAddress[ 4 ]        = {192, 168, 0, 52};
static  uint8_t ucNetMask[ 4 ]          = {255, 255, 255, 0};
static  uint8_t ucGatewayAddress[ 4 ]   = {192, 168, 0, 3};
static  uint8_t ucDNSServerAddress[ 4 ] = {192, 168, 0, 2};


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
	const cJSON* parsed_vc_cloud_1 = cJSON_Parse(vc_cloud_1);
    // FreeRTOS IP Initialization: This init initializes the IP stack
    status = FreeRTOS_IPInit(ucIPAddress, ucNetMask, ucGatewayAddress, ucDNSServerAddress, ucMACAddress);
    if(pdFALSE == status)
    {
        APP_ERR_PRINT("FreeRTOS_IPInit Failed");
        APP_ERR_TRAP(status);
    }
	while (1) {
		if (SUCCESS == isNetworkUp()) {
			for (uint8_t i = 0; i < number_of_vcs; i++)
			{
				sending_and_receiving_functionality(parsed_vc_cloud_1);
			}
			sending_and_receiving_functionality(parsed_vc_cloud_1);
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
}

void sending_and_receiving_functionality(const cJSON* vc)
{
    //char endpoint_dns[MAX_ENDPOINT_DNS_SIZE] = {RESET_VALUE};
	char endpoint_dns[] = "test-server.lan";
    const char ack = 'A';
    int endpoint_reachable = RESET_VALUE; // 1 = reachable; 0 = not reachable
    size_t endpoint_dns_length = RESET_VALUE;
    do {
        endpoint_dns_length = xMessageBufferReceive(crypto_net_message_buffer, (void *)endpoint_dns, MAX_ENDPOINT_DNS_SIZE, pdMS_TO_TICKS(500));
    } while (endpoint_dns_length == 0);
	char gp_remote_ip_address[] = "255.255.255.255";

    dnsQuerryFunc("test-server.lan", gp_remote_ip_address);
    for (int i = 0; i < 4; i++) {
        if (!vSendPing(gp_remote_ip_address)) { endpoint_reachable = 1; }
        vTaskDelay(100);
    }
	endpoint_reachable = vTCPSend("10.89.0.2", 8000, "GET /batterypass/ HTTP/1.1\r\nHost: 10.89.0.2:8000\r\nUser-Agent: BMS/8.14.1\r\nAccept: */*\r\n\r\n", 79);
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

/*******************************************************************************************************************//**
 * @brief      Sends Raw TCP data 
 * @param[in]  pcIPAddress Destination IP Address
 * @param[in]  pcPort Destination Port
 * @param[in]  pcBufferToTransmit to send
 * @param[in]  xTotalLengthToSend buffer length to send
 * @retval     Status
 **********************************************************************************************************************/

int vTCPSend(const char* pcIPAddress, uint16_t pcPort, char *pcBufferToTransmit, const size_t xTotalLengthToSend ) 
{
    struct freertos_sockaddr xRemoteAddress;
    BaseType_t xAlreadyTransmitted = 0, xBytesSent = 0;

    xRemoteAddress.sin_port = FreeRTOS_htons( pcPort );
    xRemoteAddress.sin_address.ulIP_IPv4 = FreeRTOS_inet_addr(pcIPAddress);
    xRemoteAddress.sin_family = FREERTOS_AF_INET4;

    Socket_t xSocket = FreeRTOS_socket(FREERTOS_AF_INET4, FREERTOS_SOCK_STREAM, FREERTOS_IPPROTO_TCP);
    configASSERT( xSocket != FREERTOS_INVALID_SOCKET );
/* Connect to the remote socket.  The socket has not previously been bound to
    a local port number so will get automatically bound to a local port inside
    the FreeRTOS_connect() function. */

    if( FreeRTOS_connect( xSocket, &xRemoteAddress, sizeof( xRemoteAddress ) ) == 0 )
    {
        /* Keep sending until the entire buffer has been sent. */
        while( xAlreadyTransmitted < xTotalLengthToSend )
        {
            BaseType_t xAvlSpace = 0;
            BaseType_t xBytesToSend = 0;
            uint8_t *pucTCPZeroCopyStrmBuffer;
            /* This RTOS task is going to send using the zero copy interface.  The
                data being sent is therefore written directly into the TCP TX stream
                buffer that is passed into, rather than copied into, the FreeRTOS_send()
                function. */


            /* Obtain the pointer to the current head of sockets TX stream buffer 
                using FreeRTOS_get_tx_head */

            pucTCPZeroCopyStrmBuffer = FreeRTOS_get_tx_head( xSocket, &xAvlSpace );


            if(pucTCPZeroCopyStrmBuffer)
            {
                /* Check if there is enough space in the stream buffer to place 
                    the entire data. */
                if((xTotalLengthToSend - xAlreadyTransmitted) > xAvlSpace)
                {
                    xBytesToSend = xAvlSpace;
                    APP_PRINT("Not enough Space to send the data");
                }
                else
                {
                    xBytesToSend = (xTotalLengthToSend - xAlreadyTransmitted);
                }
                memcpy( pucTCPZeroCopyStrmBuffer, 
                        ( void * ) (( (uint8_t *) pcBufferToTransmit ) + xAlreadyTransmitted),  
                        xBytesToSend);
            }
            else
            {
                /* Error - break out of the loop for graceful socket close. */
                break;
            }
            /* Call the FreeRTOS_send with buffer as NULL indicating to the stack
                that its a zero copy */
            xBytesSent = FreeRTOS_send( /* The socket being sent to. */
                                        xSocket,
                                        /* The data being sent. */
                                        NULL,
                                        /* The remaining length of data to send. */
                                        xBytesToSend,
                                        /* ulFlags. */
                                        0 );
            if( xBytesSent >= 0 )
            {
                /* Data was sent successfully. */
                xAlreadyTransmitted += xBytesSent;
            }
            else
            {
                /* Error - break out of the loop for graceful socket close. */
                break;
            }
        }
    }

    /* Wait for the socket to disconnect gracefully (indicated by FreeRTOS_recv()
    returning a -pdFREERTOS_ERRNO_EINVAL error) before closing the socket. */
	int len = 1;
    while( (len = FreeRTOS_recv( xSocket, pcBufferToTransmit, 500, 0 )) >= 0 )
    {
        /* Wait for shutdown to complete.  If a receive block time is used then
        this delay will not be necessary as FreeRTOS_recv() will place the RTOS task
        into the Blocked state anyway. */

		vTaskDelay(1000);
        /* Note - real applications should implement a timeout here, not just
        loop forever. */

    }
  	APP_PRINT("Response: %s\n", pcBufferToTransmit);
	/* Initiate graceful shutdown. */
    FreeRTOS_shutdown( xSocket, FREERTOS_SHUT_RDWR );
    /* The socket has shut down and is safe to close. */
    FreeRTOS_closesocket( xSocket );
    return 0;
}

/*******************************************************************************************************************//**
* @brief      Send ICMP Ping request  based on the user input IP Address.
* @param[in]  IP address to Ping
* @retval     Sequence Number
**********************************************************************************************************************/
BaseType_t vSendPing( const char *pcIPAddress)
{
	uint32_t ulIPAddress = RESET_VALUE;

    /*
     * The pcIPAddress parameter holds the destination IP address as a string in
     * decimal dot notation (for example, “192.168.0.200”). Convert the string into
     * the required 32-bit format.
     */
    ulIPAddress = FreeRTOS_inet_addr(pcIPAddress);

    /*
     * Send a ping request containing 8 data bytes.  Wait (in the Blocked state) a
     * maximum of 100ms for a network buffer into which the generated ping request
     * can be written and sent.
     */
    return(FreeRTOS_SendPingRequest(ulIPAddress, 8, 100 / portTICK_PERIOD_MS));
}

/*******************************************************************************************************************//**
 * @brief      DNS Query for the requested Domain name.  Uses the FreeRTOS Client API  FreeRTOS_gethostbyname
 *             to get the IP address for the domain name
 * @param[in]  Domain name
 * @retval     Status
 **********************************************************************************************************************/
int dnsQuerryFunc(char *domain, char *ip_address)
{
    uint32_t ulIPAddress = RESET_VALUE;

    /* Lookup the IP address of the FreeRTOS.org website. */
    ulIPAddress = FreeRTOS_gethostbyname((char*)domain);
    if( ulIPAddress != 0 )
    {
        /* Convert the IP address to a string. */
        FreeRTOS_inet_ntoa( ulIPAddress, ( char * ) ip_address);

		/* Print out the IP address obtained from the DNS lookup. */
        APP_PRINT ("\r\nDNS Lookup for %s is      : %s  \r\n", domain, ip_address);
		return 0;
    }
    else
    {
        APP_PRINT ("\r\nDNS Lookup failed for %s \r\n", domain);
		return 1;
	}
	return 1;
}

void print_ipconfig() {
	    APP_PRINT("\r\nEthernet adapter for Renesas RA6M5:\r\n");

    APP_PRINT("\tDescription . . . . . . . . . . . : Renesas RA6M5 Ethernet\r\n");
    APP_PRINT("\tPhysical Address. . . . . . . . . : %02x-%02x-%02x-%02x-%02x-%02x\r\n",
            ucMACAddress[0],ucMACAddress[1],ucMACAddress[2],ucMACAddress[3],ucMACAddress[4],ucMACAddress[5]);
    APP_PRINT("\tDHCP Enabled. . . . . . . . . . . : No\r\n");
    APP_PRINT("\tIPv4 Address. . . . . . . . . . . : %d.%d.%d.%d\r\n",ucIPAddress[0],ucIPAddress[1],ucIPAddress[2],ucIPAddress[3]);
    APP_PRINT("\tSubnet Mask . . . . . . . . . . . : %d.%d.%d.%d\r\n",ucNetMask[0],ucNetMask[1],ucNetMask[2],ucNetMask[3]);
    APP_PRINT("\tDefault Gateway . . . . . . . . . : %d.%d.%d.%d\r\n",ucGatewayAddress[0],ucGatewayAddress[1],ucGatewayAddress[2],ucGatewayAddress[3]);
    APP_PRINT("\tDNS Servers . . . . . . . . . . . : %d.%d.%d.%d\r\n",ucDNSServerAddress[0],ucDNSServerAddress[1],ucDNSServerAddress[2],ucDNSServerAddress[3]);
}

/*******************************************************************************************************************//**
 * @brief      This Function checks the Network status (Both Ethernet and IP Layer). If the Network is down
 *             the Application will not send any data on the network.
 * @param[in]  None
 * @retval     Network Status
 **********************************************************************************************************************/
uint32_t isNetworkUp(void)
{
    fsp_err_t  eth_link_status = FSP_ERR_NOT_OPEN;
    BaseType_t networkUp = pdFALSE;
    uint32_t network_status = (IP_LINK_UP | ETHERNET_LINK_UP);

    networkUp = FreeRTOS_IsNetworkUp();
    eth_link_status = R_ETHER_LinkProcess(g_ether0.p_ctrl);

    if((FSP_SUCCESS == eth_link_status) && (pdTRUE == networkUp))
    {
        return network_status;
    }
    else
    {
        if(FSP_SUCCESS != eth_link_status)
        {
            network_status |= ETHERNET_LINK_DOWN;
        }
        else if(FSP_SUCCESS == eth_link_status)
        {
            network_status |= ETHERNET_LINK_UP;
        }

        if(pdTRUE != networkUp)
        {
             network_status |= IP_LINK_DOWN;
        }
        else if(pdTRUE == networkUp)
        {
             network_status |= IP_LINK_UP;
        }
        return network_status;
    }
}

/*******************************************************************************************************************//**
* @brief      User Hook for the Ping Reply. vApplicationPingReplyHook() is called by the TCP/IP
*             stack when the stack receives a ping reply.
* @param[in]  Ping reply status and Identifier
* @retval     None
**********************************************************************************************************************/
void vApplicationPingReplyHook( ePingReplyStatus_t eStatus, uint16_t usIdentifier )
{
    (void)  usIdentifier;
	return;
    // switch( eStatus )
    // {
    //     /* A valid ping reply has been received */
    //     case eSuccess    :
    //         ping_data.received++;
    //         break;
    //         /* A reply was received but it was not valid. */
    //     case eInvalidData :
    //     default:
    //         ping_data.lost++;
    //         break;
    // }
}