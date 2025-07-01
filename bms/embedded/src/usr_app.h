/***********************************************************************************************************************
 * File Name    : usr_app.h
 * Description  : Contains macros, data structures and functions used  in the Application
 ***********************************************************************************************************************/
/***********************************************************************************************************************
* Copyright (c) 2020 - 2024 Renesas Electronics Corporation and/or its affiliates
*
* SPDX-License-Identifier: BSD-3-Clause
***********************************************************************************************************************/

#ifndef USR_APP_H_
#define USR_APP_H_

#include <stdint.h>
#include <stddef.h>

#define USR_PING_COUNT (100)

#define BLOCKCHAIN_ENDPOINT "10.89.0.2"
#define NETWORK_RETRIES 20

#define SUCCESS (0)
#define PRINT_UP_MSG_DISABLE (0x01)
#define PRINT_DOWN_MSG_DISABLE (0x02)
#define PRINT_NWK_USR_MSG_DISABLE (0x04)


#define ETHERNET_LINK_DOWN (0x01)
#define ETHERNET_LINK_UP (0x00)
#define IP_LINK_DOWN (0x02)
#define IP_LINK_UP (0x00)

int vTCPSend(const char* pcIPAddress, uint16_t pcPort, char *pcBufferToTransmit, const size_t xTotalLengthToSend, char*); 
int vTCPSendWithRetries(const char* pcIPAddress, uint16_t pcPort, char *pcBufferToTransmit, const size_t xTotalLengthToSend, char* pcBufferToReceive, int retries);

uint32_t ulApplicationGetNextSequenceNumber( uint32_t ulSourceAddress,
                                             uint16_t usSourcePort,
                                             uint32_t ulDestinationAddress,
                                             uint16_t usDestinationPort );
uint32_t isNetworkUp(void);
BaseType_t vSendPing( const char *pcIPAddress);
void print_ipconfig(void);
int dnsQuerryFunc(char *domain_name, char *ip_address);

typedef struct st_ping_data
{
    uint32_t sent;     // Ping Request
    uint32_t received; // Ping Response
    uint32_t lost;     // Ping failure
} ping_data_t;

#endif /* USR_APP_H_ */
