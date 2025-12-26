#ifndef NET_TASK_ENTRY_H
#define NET_TASK_ENTRY_H

extern const int number_of_vcs;

#define MAX_IPV4_SIZE 17
#define MAX_ENDPOINT_DNS_SIZE 100
#define DID_LENGTH 29
#define ACK_LENGTH 1
#define BUFFER_LENGTH 2000

#ifndef BLOCKCHAIN_ENDPOINT
#define BLOCKCHAIN_ENDPOINT "10.89.0.2"
#endif

#ifndef BMS_DID
#define BMS_DID "did:batterypass:bms.sn-544b51e7"
#endif

#ifndef VC_LIST
#define VC_LIST {"{\"@context\":[\"https://www.w3.org/2018/credentials/v1\",\"http://localhost:8443/docs/vc.serviceAccess.schema.html\"],\"id\":\"urn:uuid:a1fd774e-5300-4171-b778-e53cedb64823\",\"type\":[\"VerifiableCredential\",\"CloudInstance\"],\"issuer\":\"did:batterypass:bms.sn-544b51e7\",\"holder\":\"did:batterypass:cloud.sn-central\",\"issuanceDate\":\"2025-06-17T16:17:43Z\",\"expirationDate\":\"2026-06-17T16:17:43Z\",\"credentialSubject\":{\"id\":\"did:batterypass:cloud.sn-cloud1\",\"type\":\"CloudInstance\",\"cloudDid\":\"did:batterypass:cloud.sn-cloud1\",\"timestamp\":\"2026-06-17T16:17:43Z\"},\"proof\":{\"type\":\"EcdsaSecp256r1Signature2019\",\"created\":\"2025-06-17T16:17:43Z\",\"verificationMethod\":\"did:batterypass:bms.sn-544b51e7#key-1\",\"proofPurpose\":\"authentication\",\"jws\":\"\"}}"}
#endif

#include "FreeRTOS_IP.h"
#include "FreeRTOS_IP_Private.h"
#include "FreeRTOS_Sockets.h"
#include "common_utils.h"
#include "usr_app.h"
#include <stdint.h>
#include <string.h>
#include "cJSON.h"
#include "core_json.h"



int sending_and_receiving_functionality( );
void print_ipconfig();



#endif // NET_TASK_ENTRY_H

