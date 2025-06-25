#ifndef NET_TASK_ENTRY_H
#define NET_TASK_ENTRY_H

extern const int number_of_vcs;

#define MAX_IPV4_SIZE 17
#define MAX_ENDPOINT_DNS_SIZE 100
#define DID_LENGTH 29
#define ACK_LENGTH 1

#include "FreeRTOS_IP.h"
#include "FreeRTOS_IP_Private.h"
#include "FreeRTOS_Sockets.h"
#include "common_utils.h"
#include "usr_app.h"
#include <stdint.h>
#include <string.h>
#include "cJSON.h"


void sending_and_receiving_functionality(const cJSON* vc);
void print_ipconfig();

#endif // NET_TASK_ENTRY_H

