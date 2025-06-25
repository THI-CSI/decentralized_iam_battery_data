#include "common.h"
#include "common_utils.h"
#include "bms_cloud_transaction.h"
#include "bms_cloud_transaction_entry.h"
#include "portable.h"
#include "mbedtls/pk.h"
#include "mbedtls/ecp.h"
#include "mbedtls/base64.h"
#include "rtc_init.h"

// DID
__attribute__((section(".data_flash")))
const char did[30] = "did:example:123456789abcdefgh";

/* BMS2Cloud entry function */
/* pvParameters contains TaskHandle_t */
void bms_cloud_transaction_entry(void *pvParameters)
{
    FSP_PARAMETER_NOT_USED (pvParameters);
    // The rate at which the task waits on the Semaphore availability.
    TickType_t Semphr_wait_ticks = pdMS_TO_TICKS(WAIT_TIME);
    for (;;)
    {
        if (pdPASS == xSemaphoreTake(bms_cloud_sem, Semphr_wait_ticks))
        {
            // Initialize encryption_context on heap
            encryption_context *encryption_ctx = (encryption_context *)pvPortCalloc(1, sizeof(encryption_context));
            // Request DID-docs and initialize encryption_ctx->did_documents
            uint8_t number_of_endpoints = fetch_did_documents(encryption_ctx);
            // Query dynamic battery data
            simulate_battery_data_query(encryption_ctx);
            // Send message_ctx
            for (uint8_t i = 0; i < number_of_endpoints; i++)
            {
            	// Initialize context_structs on heap
            	message_context  *message_ctx = (message_context *)pvPortCalloc(1, sizeof(message_context));
                final_message_struct *final_message = (final_message_struct *)pvPortCalloc(1, sizeof(final_message_struct));
                // Initialize message_ctx
                prepare_final_message_ctx(i, encryption_ctx, message_ctx, final_message);
                // Send message_ctx to did_document[i]->endpoint
                ethernet_send(encryption_ctx->did_documents[i]->endpoint, encryption_ctx->did_documents[i]->endpoint_length, final_message);
                // Free resources
                free_contexts(i, encryption_ctx, message_ctx, final_message);
            }
            // Free encryption_context
            vPortFree(encryption_ctx->battery_data);
            vPortFree(encryption_ctx->did_documents);
            vPortFree(encryption_ctx);
        }
    }
}

/*******************************************************************************************************************//**
 * @brief        Retrieves DID documents of cloud endpoints via the network task and extracts relevant data into 
                 DID document structures.
 * @param[out]   encryption_ctx     Buffer to store the extracted encryption context structure.
 * @retval       None
 **********************************************************************************************************************/
uint8_t fetch_did_documents(encryption_context *encryption_ctx)
{
    uint8_t number_of_endpoints = 1; // = amount of stored VCs
    encryption_ctx->did_documents = (did_document **)pvPortCalloc(number_of_endpoints, sizeof(did_document *));
    xSemaphoreGive(crypto_net_sem);
    for (uint8_t i = 0; i < number_of_endpoints; i++)
    {
        encryption_ctx->did_documents[i] = (did_document *)pvPortCalloc(1, sizeof(did_document));
        encryption_ctx->did_documents[i]->endpoint = (char *)pvPortCalloc(ENDPOINT_MAX_BUFFER_SIZE, sizeof(char));
        encryption_ctx->did_documents[i]->public_key_der_encoded = (uint8_t *)pvPortCalloc(ECC_256_PUB_DER_MAX_BUFFER_SIZE, sizeof(uint8_t));
        size_t xReceivedBytes = RESET_VALUE;
        char cReceivedString[1024];
        memset(cReceivedString, RESET_VALUE, sizeof(cReceivedString));
        do
        {
            xReceivedBytes = xMessageBufferReceive(net_crypto_message_buffer, (void *)cReceivedString, sizeof(cReceivedString), pdMS_TO_TICKS(1000));
        } while(xReceivedBytes == 0);
        cJSON *root = cJSON_ParseWithLength(cReceivedString, xReceivedBytes);
        cJSON *vm = cJSON_GetObjectItem(root, "verificationMethod");
        cJSON *pubkey = cJSON_GetObjectItem(vm, "publicKeyMultibase");
        const char *public_key_base_64 = pubkey->valuestring;
        size_t public_key_base_64_length = strlen(public_key_base_64);
        mbedtls_base64_decode(encryption_ctx->did_documents[i]->public_key_der_encoded, ECC_256_PUB_DER_MAX_BUFFER_SIZE, &encryption_ctx->did_documents[i]->public_key_der_encoded_length,
							 (unsigned char *)public_key_base_64, public_key_base_64_length);
        der_decoding(encryption_ctx->did_documents[i]->public_key_der_encoded, encryption_ctx->did_documents[i]->public_key_der_encoded_length, encryption_ctx->did_documents[i]->public_key);
        cJSON *service_array = cJSON_GetObjectItem(root, "service");
        cJSON *first_service = cJSON_GetArrayItem(service_array, 0);
        cJSON *endpoint = cJSON_GetObjectItem(first_service, "serviceEndpoint");
        const char *endpoint_ptr = endpoint->valuestring;
        memcpy(encryption_ctx->did_documents[i]->endpoint, endpoint_ptr, strlen(endpoint->valuestring));
        encryption_ctx->did_documents[i]->endpoint_length = strlen(endpoint->valuestring);
        cJSON_Delete(root);
    }
    return number_of_endpoints;
}

/*******************************************************************************************************************//**
 * @brief        Simulates a dynamic battery data query and stores the results in a list of JSON paths.
 * @param[out]   encryption_ctx     Buffer containing the encryption context structure.
 * @retval       None
 **********************************************************************************************************************/
void simulate_battery_data_query(encryption_context *encryption_ctx)
{
    char *battery_data_string = (char *)pvPortCalloc(MAX_MODFIED_DATA_BUFFER, sizeof(char));
    int number_of_full_battery_cycles = get_number_of_full_battery_cycles();
    sprintf(battery_data_string, "performance.batteryCondition.numberOfFullCycles.numberOfFullCyclesValue: %d", number_of_full_battery_cycles);
    encryption_ctx->battery_data_length = strlen(battery_data_string);
    encryption_ctx->battery_data = (uint8_t *)pvPortCalloc(encryption_ctx->battery_data_length, sizeof(uint8_t));
    memcpy(encryption_ctx->battery_data, battery_data_string, encryption_ctx->battery_data_length);
    // Free memory
    vPortFree(battery_data_string);
}

int get_number_of_full_battery_cycles(void)
{
    int number_of_full_battery_cycles = 200;
    return number_of_full_battery_cycles;
}

/*******************************************************************************************************************//**
 * @brief        Prepares the final_message structure to be passed to the network task.
 * @param[in]    recipient_counter      Index of the DID document for which the message is being created.
 * @param[in]    encryption_ctx         Buffer containing the encryption context structure.
 * @param[in]    message_ctx            Buffer containing the message context structure.
 * @param[out]   final_message_struct   Buffer to store the prepared final_message structure.
 * @retval       None
 **********************************************************************************************************************/
void prepare_final_message_ctx(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx, final_message_struct *final_message)
{
   psa_status_t status = (psa_status_t)RESET_VALUE;
   status = crypto_operations(recipient_counter, encryption_ctx, message_ctx, final_message);
   if (PSA_SUCCESS != status)
   {
       // HPKE operation failed. Perform cleanup and trap error.
       handle_error(status, "\r\n** Crypto-Operation FAILED ** \r\n");
   }
}

psa_status_t crypto_operations(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx, final_message_struct *final_message)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_key_handle_t ephemeral_key_handle = (psa_key_handle_t)RESET_VALUE;
    // Generate ephemeral-keypair & export public part in DER-Format
    status = generate_ephemeral_key_pair(message_ctx, &ephemeral_key_handle);
    CHECK_PSA_SUCCESS(status, "");
    // Derive encryption key - DHCP | HKDF(SHA2-256)
    status = derive_encryption_key(message_ctx, encryption_ctx, recipient_counter, ephemeral_key_handle);
    CHECK_PSA_SUCCESS(status, "");
    // Encrypt battery data - AES-GCM 256
    status = encrypt_battery_data(encryption_ctx, message_ctx);
    CHECK_PSA_SUCCESS(status, "");
    // Generate signed JSON-message
    status = generate_signed_json_message(message_ctx, final_message);
    CHECK_PSA_SUCCESS(status, "");

    return status;
}

 /*******************************************************************************************************************//**
 * @brief        Generates an ephemeral key pair for shared secret generation.
 * @param[out]   message_ctx            Buffer containing the encryption context structure.
 * @param[out]   ephemeral_key_handle   Buffer containing the ephemeral key handle.
 * @retval       PSA_SUCCESS or other error codes indicating the result of the operation.
 **********************************************************************************************************************/
psa_status_t generate_ephemeral_key_pair(message_context *message_ctx, psa_key_handle_t *ephemeral_key_handle)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_key_attributes_t ecc_attributes = PSA_KEY_ATTRIBUTES_INIT;
    uint8_t ecc_pub_key[ECC_256_PUB_MAX_BUFFER_SIZE] = {RESET_VALUE};
    size_t ecc_pub_key_length = RESET_VALUE;

    // Set Key uses flags, key_algorithm, key_type, key_bits, key_lifetime
    psa_set_key_usage_flags(&ecc_attributes, PSA_KEY_USAGE_DERIVE);
    psa_set_key_algorithm(&ecc_attributes, PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(PSA_ALG_SHA_256)));
    psa_set_key_type(&ecc_attributes, PSA_KEY_TYPE_ECC_KEY_PAIR_WRAPPED(PSA_ECC_FAMILY_SECP_R1));
    psa_set_key_bits(&ecc_attributes, ECC_256_BIT_LENGTH);
    psa_set_key_lifetime(&ecc_attributes, PSA_KEY_LIFETIME_VOLATILE);

    // Generate ECC P256R1 Key pair
    status = psa_generate_key(&ecc_attributes, ephemeral_key_handle);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_key API FAILED ** \r\n")

    // Export public key
    status = psa_export_public_key(*ephemeral_key_handle, ecc_pub_key, ECC_256_PUB_MAX_BUFFER_SIZE, &ecc_pub_key_length);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_export_public_key API FAILED ** \r\n");

    // DER-encoding of public key
    der_encoding(ecc_pub_key, ecc_pub_key_length, &message_ctx->der_encoded_ephemeral_key, &message_ctx->der_encoded_ephemeral_key_length);

    return status;
}

/*******************************************************************************************************************//**
 * @brief        DER encodes a public key.
 * @param[in]    ecc_pub_key                    Buffer containing the public key.
 * @param[in]    ecc_pub_key_length             Length of the public key in bytes.
 * @param[out]   der_encoded_key_buffer         Buffer to store the DER-encoded public key.
 * @param[out]   der_encoded_key_buffer_length  Length of the DER-encoded public key in bytes.
 * @retval       None
 **********************************************************************************************************************/
void der_encoding(uint8_t *ecc_pub_key, size_t ecc_pub_key_length, uint8_t **der_encoded_key_buffer, size_t *der_encoded_key_buffer_length)
{
    unsigned char ecc_pub_key_der_encoded[ECC_256_PUB_DER_MAX_BUFFER_SIZE] = {RESET_VALUE};
    unsigned char *ecc_pub_key_der_write_ptr = ecc_pub_key_der_encoded + sizeof(ecc_pub_key_der_encoded);
    size_t ecc_pub_key_length_der_encoded = RESET_VALUE;

    mbedtls_pk_context ctx_pk;
    mbedtls_pk_init(&ctx_pk);
    mbedtls_ecp_keypair *ecp = mbedtls_calloc(1, sizeof(mbedtls_ecp_keypair)); // pvPortCalloc?
    mbedtls_ecp_keypair_init(ecp);
    mbedtls_ecp_group_load(&ecp->grp, MBEDTLS_ECP_DP_SECP256R1);
    mbedtls_ecp_point_read_binary(&ecp->grp, &ecp->Q, ecc_pub_key, ecc_pub_key_length);
    mbedtls_mpi_init(&ecp->d);
    mbedtls_pk_setup(&ctx_pk, mbedtls_pk_info_from_type(MBEDTLS_PK_ECKEY));
    ctx_pk.pk_ctx = ecp;

    ecc_pub_key_length_der_encoded = (size_t)mbedtls_pk_write_pubkey_der(&ctx_pk, ecc_pub_key_der_encoded, sizeof(ecc_pub_key_der_encoded));
    *der_encoded_key_buffer = (uint8_t *)pvPortCalloc(ecc_pub_key_length_der_encoded, sizeof(uint8_t));
    memcpy(*der_encoded_key_buffer, (uint8_t *)(ecc_pub_key_der_write_ptr - ecc_pub_key_length_der_encoded), ecc_pub_key_length_der_encoded);
    *der_encoded_key_buffer_length = ecc_pub_key_length_der_encoded;

    mbedtls_ecp_keypair_free(ecp);
    mbedtls_pk_free(&ctx_pk);
}

/*******************************************************************************************************************//**
 * @brief        DER decodes a public key.
 * @param[in]    ecc_pub_key_der            Buffer containing the DER-encoded public key.
 * @param[in]    ecc_pub_key_der_length     Length of the DER-encoded public key in bytes.
 * @param[out]   raw_key_buffer             Buffer to store the decoded raw public key.
 * @retval       None
 **********************************************************************************************************************/
void der_decoding(uint8_t *ecc_pub_key_der, size_t ecc_pub_key_der_length, uint8_t *raw_key_buffer)
{
    mbedtls_pk_context ctx_pk;
    mbedtls_pk_init(&ctx_pk);
    mbedtls_pk_parse_public_key(&ctx_pk, (unsigned char *)ecc_pub_key_der, ecc_pub_key_der_length);
    if (mbedtls_pk_can_do(&ctx_pk, MBEDTLS_PK_ECKEY))
    {
        mbedtls_ecp_keypair *ecp = mbedtls_pk_ec(ctx_pk);
        unsigned char x_coord[32] = {RESET_VALUE};
        unsigned char y_coord[32] = {RESET_VALUE};
        mbedtls_mpi_write_binary(&ecp->Q.X, x_coord, sizeof(x_coord));
        mbedtls_mpi_write_binary(&ecp->Q.Y, y_coord, sizeof(y_coord));
        raw_key_buffer[0] = 0x04;
        memcpy(&raw_key_buffer[1], x_coord, 32);
        memcpy(&raw_key_buffer[33], y_coord, 32);
    }

    mbedtls_pk_free(&ctx_pk);
}

/*******************************************************************************************************************//**
 * @brief        Generates a shared secret using ECDH and derives a symmetric key from it using HKDF (SHA-256).
 * @param[out]   message_ctx            Buffer containing the encryption context structure.
 * @param[in,out] encryption_ctx        Buffer containing the encryption context structure.
 * @param[in]    recipient_counter      Index of the DID document for which the key is derived.
 * @param[in]    ephemeral_key_handle   Buffer containing the ephemeral key handle.
 * @retval       PSA_SUCCESS or other error codes indicating the result of the operation.
 **********************************************************************************************************************/  
psa_status_t derive_encryption_key(message_context *message_ctx, encryption_context *encryption_ctx, uint8_t recipient_counter, psa_key_handle_t ephemeral_key_handle)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_key_derivation_operation_t derivation_operation = PSA_KEY_DERIVATION_OPERATION_INIT;
    psa_key_attributes_t aes_attributes = PSA_KEY_ATTRIBUTES_INIT;
    did_document *did_doc = encryption_ctx->did_documents[recipient_counter];
    size_t info_length = message_ctx->der_encoded_ephemeral_key_length + did_doc->public_key_der_encoded_length;
    uint8_t info[info_length];
    memcpy(info, message_ctx->der_encoded_ephemeral_key, message_ctx->der_encoded_ephemeral_key_length);
    memcpy(info + message_ctx->der_encoded_ephemeral_key_length, did_doc->public_key_der_encoded, did_doc->public_key_der_encoded_length);

    // Set Key uses flags, key_algorithm, key_type, key_bits, key_lifetime
    psa_set_key_usage_flags(&aes_attributes, PSA_KEY_USAGE_ENCRYPT);
    psa_set_key_algorithm(&aes_attributes, PSA_ALG_GCM);
    psa_set_key_type(&aes_attributes, PSA_KEY_TYPE_AES);
    psa_set_key_bits(&aes_attributes, AES_KEY_BITS);
    psa_set_key_lifetime(&aes_attributes, PSA_KEY_LIFETIME_VOLATILE);

    // Generate random Salt value
    status = psa_generate_random(message_ctx->salt, SALT_LENGTH);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_random API FAILED ** \r\n");

    // Shared-Secret agreement and aes-key derivation
    status = psa_key_derivation_setup(&derivation_operation, PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(PSA_ALG_SHA_256)));
    CHECK_PSA_SUCCESS(status, "\r\n** psa_key_derivation_setup API FAILED ** \r\n");
    status = psa_key_derivation_set_capacity(&derivation_operation, AES_KEY_BITS);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_key_derivation_set_capacity API FAILED ** \r\n");
    status = psa_key_derivation_input_bytes(&derivation_operation, PSA_KEY_DERIVATION_INPUT_SALT, message_ctx->salt, SALT_LENGTH);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_input_bytes API FAILED ** \r\n", &derivation_operation);
    status = psa_key_derivation_key_agreement(&derivation_operation, PSA_KEY_DERIVATION_INPUT_SECRET, ephemeral_key_handle, did_doc->public_key, ECC_256_PUB_RAW_LENGTH);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_input_key_agreement API FAILED ** \r\n", &derivation_operation);
    status = psa_key_derivation_input_bytes(&derivation_operation, PSA_KEY_DERIVATION_INPUT_INFO, info, info_length);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_input_bytes API FAILED ** \r\n", &derivation_operation);
    status = psa_key_derivation_output_key(&aes_attributes, &derivation_operation, &encryption_ctx->aes_key_handle);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_output_key API FAILED ** \r\n", &derivation_operation);

    // Abort derivation_operation and destroy ephemeral_key_pair
    psa_key_derivation_abort(&derivation_operation);
    status = psa_destroy_key(ephemeral_key_handle);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_destroy_key API FAILED ** \r\n");

    return status;
}

/*******************************************************************************************************************//**
 * @brief        Encrypts dynamic battery data using AES-GCM 256.
 * @param[in]    encryption_ctx      Buffer containing the encryption context structure.
 * @param[out]   message_ctx         Buffer containing the message context structure.
 * @retval       PSA_SUCCESS or other error codes indicating the result of the encryption.
 **********************************************************************************************************************/
psa_status_t encrypt_battery_data(encryption_context *encryption_ctx, message_context *message_ctx)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    uint8_t nonce[NONCE_LENGTH] = {RESET_VALUE};
    size_t encrypted_data_size = RESET_VALUE;

    // Generate IV (96 bits), calculate encrypted_data_size and allocate heap for encrypted data
    status = psa_generate_random(nonce, NONCE_LENGTH);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_random API FAILED ** \r\n");
    encrypted_data_size = PSA_AEAD_ENCRYPT_OUTPUT_SIZE(PSA_KEY_TYPE_AES, PSA_ALG_GCM, encryption_ctx->battery_data_length);
    message_ctx->battery_data_encrypted = (uint8_t *)pvPortCalloc(encrypted_data_size, sizeof(uint8_t));
    if (NULL == message_ctx->battery_data_encrypted)
    {
        APP_ERR_PRINT("\r\n** Out Of Memory. ** \r\n");
        return FSP_ERR_OUT_OF_MEMORY;
    }
    memcpy(message_ctx->aad, nonce, NONCE_LENGTH);

    // AES-GCM 256 encryption
    status = psa_aead_encrypt(encryption_ctx->aes_key_handle, PSA_ALG_GCM, nonce, NONCE_LENGTH, message_ctx->aad, AAD_LENGTH, encryption_ctx->battery_data,
                              encryption_ctx->battery_data_length, message_ctx->battery_data_encrypted, encrypted_data_size, &message_ctx->encrypted_data_length);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_aead_encrypt API FAILED ** \r\n");
    status = psa_destroy_key(encryption_ctx->aes_key_handle);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_destroy_key API FAILED ** \r\n");

    return status;
}

/*******************************************************************************************************************//**
 * @brief        Signs the message using ECDSA (SHA-256) and prepares the final_message structure.
 * @param[in]    message_ctx     Buffer containing the message context structure.
 * @param[out]   final_message   Buffer to store the prepared final_message structure.
 * @retval       PSA_SUCCESS or other error codes indicating the result of the operation.
 **********************************************************************************************************************/
psa_status_t generate_signed_json_message(message_context *message_ctx, final_message_struct *final_message)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_key_handle_t signing_key_handle = (psa_key_handle_t)RESET_VALUE;
    uint8_t *concatenated_message_bytes = NULL;
    size_t concatenated_message_bytes_length = RESET_VALUE;
    uint8_t concatenated_message_bytes_hash[PSA_HASH_MAX_SIZE] = {RESET_VALUE};
    size_t concatenated_message_bytes_hash_length = RESET_VALUE;
    uint8_t signature[PSA_SIGNATURE_MAX_SIZE] = {RESET_VALUE};
    size_t signature_length = RESET_VALUE;
    cJSON *json_message = cJSON_CreateObject();

    // Sign hash of message_ctx
    status = psa_open_key(SIGNING_KEY_ID, &signing_key_handle);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_close_key API FAILED ** \r\n");
    create_message_string(message_ctx, &concatenated_message_bytes, &concatenated_message_bytes_length, json_message);
    status = ecc_hashing_operation(concatenated_message_bytes, concatenated_message_bytes_length, concatenated_message_bytes_hash, &concatenated_message_bytes_hash_length);
    CHECK_PSA_SUCCESS(status, "\r\n** ecc_hashing_operation failed. ** \r\n");
    status = psa_sign_hash(signing_key_handle, PSA_ALG_ECDSA(PSA_ALG_SHA_256), concatenated_message_bytes_hash, concatenated_message_bytes_hash_length, signature, PSA_SIGNATURE_MAX_SIZE, &signature_length);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_sign_hash API FAILED ** \r\n");
    status = psa_close_key(signing_key_handle);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_close_key API FAILED ** \r\n");
    // Generate final signed JSON-Message
    generate_final_signed_json_message(json_message, signature, signature_length, final_message);

    return status;
}

/*******************************************************************************************************************//**
 * @brief        Base64-encodes values from the message_context, generates the JSON message, and produces the 
                 concatenated message bytes to hash.
 * @param[in]    message_ctx                         Buffer containing the message context structure.
 * @param[out]   concatenated_message_bytes          Buffer to store the concatenated message bytes.
 * @param[out]   concatenated_message_bytes_length   Length of the concatenated message in bytes.
 * @param[out]   message_json                        Buffer containing the JSON representation of the message.
 * @retval       None
 **********************************************************************************************************************/
void create_message_string(message_context *message_ctx, uint8_t **concatenated_message_bytes, size_t *concatenated_message_bytes_length, cJSON *message_json)
{
    CHECK_JSON_STATUS(message_json, message_json);

    // Base64 encoding of ciphertext and adding to message_json
    size_t ciphertext_base64_size = (size_t) ((message_ctx->encrypted_data_length + 2) / 3.0) * 4 + 1;
    size_t ciphertext_base64_bytes_written = RESET_VALUE;
    unsigned char ciphertext_base64[ciphertext_base64_size];
    mbedtls_base64_encode(ciphertext_base64, ciphertext_base64_size, &ciphertext_base64_bytes_written,
                          (unsigned char *)message_ctx->battery_data_encrypted, message_ctx->encrypted_data_length);
    ciphertext_base64[ciphertext_base64_bytes_written] = '\0';
    cJSON_AddStringToObject(message_json, "ciphertext", (char *)ciphertext_base64);

    // Base64 encoding of AAD and adding to message_json
    size_t aad_base64_size = (size_t) ((AAD_LENGTH +2) / 3) * 4 + 1;
    size_t aad_base64_bytes_written = RESET_VALUE;
    unsigned char aad_base64[aad_base64_size];
    mbedtls_base64_encode(aad_base64, aad_base64_size, &aad_base64_bytes_written, (unsigned char *)message_ctx->aad, AAD_LENGTH);
    aad_base64[aad_base64_bytes_written] = '\0';
    cJSON_AddStringToObject(message_json, "aad", (char *)aad_base64);

    // Base64 encoding of salt and adding to message_json
    size_t salt_base64_size = (size_t) ((SALT_LENGTH + 2) / 3) * 4 + 1;
    size_t salt_base64_bytes_written = RESET_VALUE;
    unsigned char salt_base64[salt_base64_size];
    mbedtls_base64_encode(salt_base64, salt_base64_size, &salt_base64_bytes_written, (unsigned char *)message_ctx->salt, SALT_LENGTH);
    salt_base64[salt_base64_bytes_written] = '\0';
    cJSON_AddStringToObject(message_json, "salt", (char *)salt_base64);

    // Base64 encoding of did and adding to message_json
    size_t did_base64_size = (size_t) ((DID_LENGTH + 2) / 3) * 4 + 1;
    size_t did_base64_bytes_written = RESET_VALUE;
    unsigned char did_base64[did_base64_size];
    mbedtls_base64_encode(did_base64, did_base64_size, &did_base64_bytes_written, (unsigned char *)did, DID_LENGTH);
    did_base64[did_base64_bytes_written] = '\0';
    cJSON_AddStringToObject(message_json, "did", (char *)did_base64);

    // Base64 encoding of ephemeral_public_key_der and adding to message_json
    size_t ephemeral_public_key_der_base64_size = (size_t) ((message_ctx->der_encoded_ephemeral_key_length + 2) / 3) * 4 + 1;
    size_t ephemeral_publick_key_der_base64_bytes_written = RESET_VALUE;
    unsigned char ephemeral_public_key_der_base64[ephemeral_public_key_der_base64_size];
    mbedtls_base64_encode(ephemeral_public_key_der_base64, ephemeral_public_key_der_base64_size, &ephemeral_publick_key_der_base64_bytes_written,
                             (unsigned char *)message_ctx->der_encoded_ephemeral_key, message_ctx->der_encoded_ephemeral_key_length);
    ephemeral_public_key_der_base64[ephemeral_publick_key_der_base64_bytes_written] = '\0';
    cJSON_AddStringToObject(message_json, "eph_pub", (char *)ephemeral_public_key_der_base64);

    // Get timestamp, base64 encoding of timestamp and adding to message_json
    get_rtc_calendar_time(message_ctx->timestamp_bytes);
    size_t timestamp_base64_size = (size_t) ((TIMESTAMP_LENGTH + 2) / 3) * 4 + 1;
    size_t timestamp_bytes_written = RESET_VALUE;
    unsigned char timestamp_base64[timestamp_base64_size];
    mbedtls_base64_encode(timestamp_base64, timestamp_base64_size, &timestamp_bytes_written, (unsigned char *)message_ctx->timestamp_bytes, TIMESTAMP_LENGTH);
    timestamp_base64[timestamp_bytes_written] = '\0';
    cJSON_AddStringToObject(message_json, "timestamp", (char *)timestamp_base64);

    // Create concatenated message string to sign
    char *concatenated_message_string = cJSON_PrintUnformatted(message_json);
    *concatenated_message_bytes_length = strlen(concatenated_message_string);
    *concatenated_message_bytes = (uint8_t *)pvPortCalloc(*concatenated_message_bytes_length, sizeof(uint8_t));
    memcpy(*concatenated_message_bytes, concatenated_message_string, *concatenated_message_bytes_length);
}

/*******************************************************************************************************************//**
 * @brief        Performs SHA-256 hashing on the given message bytes for ECC operations.
 * @param[in]    concatenated_message_bytes                 Buffer containing the message bytes to hash.
 * @param[in]    concatenated_message_bytes_length          Length of the message in bytes.
 * @param[out]   concatenated_message_bytes_hash            Buffer to store the resulting hash.
 * @param[out]   concatenated_message_bytes_hash_length     Length of the hash in bytes.
 * @retval       PSA_SUCCESS or other error codes indicating the result of the hashing operation.
 **********************************************************************************************************************/
psa_status_t ecc_hashing_operation(uint8_t *concatenated_message_bytes, size_t concatenated_message_bytes_length, uint8_t *concatenated_message_bytes_hash, size_t *concatenated_message_bytes_hash_length)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_hash_operation_t hash_operation = {RESET_VALUE};
    status = psa_hash_setup(&hash_operation, PSA_ALG_SHA_256);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_hash_setup API FAILED ** \r\n");
    status = psa_hash_update(&hash_operation, concatenated_message_bytes, concatenated_message_bytes_length);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_hash_update API FAILED ** \r\n");
    status = psa_hash_finish(&hash_operation, concatenated_message_bytes_hash, PSA_HASH_MAX_SIZE, concatenated_message_bytes_hash_length);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_hash_finish API FAILED ** \r\n");
    // Free memory
    vPortFree(concatenated_message_bytes);

    return status;
}

/*******************************************************************************************************************//**
 * @brief        Populates the final_message structure by adding the Base64-encoded signature.
 * @param[in]    message_json         Buffer containing the JSON representation of the message.
 * @param[in]    signature            Buffer containing the message hash signature.
 * @param[in]    signature_length     Length of the signature in bytes.
 * @param[out]   final_message        Buffer to store the populated final_message structure.
 * @retval       None
 **********************************************************************************************************************/
void generate_final_signed_json_message(cJSON* json_message, uint8_t *signature, size_t signature_length, final_message_struct *final_message)
{
    // Base64 encoding of signature and adding to message_json
    size_t signatur_base64_size = (size_t) ((signature_length + 2) / 3) * 4 + 1;
    size_t signature_base64_bytes_written = RESET_VALUE;
    unsigned char signature_base64[signatur_base64_size];
    mbedtls_base64_encode(signature_base64, signatur_base64_size, &signature_base64_bytes_written, (unsigned char *)signature, signature_length);
    signature_base64[signature_base64_bytes_written] = '\0';
    cJSON_AddStringToObject(json_message, "signature", (char *)signature_base64);

    // Initlialize final message struct
    char *final_message_string = cJSON_PrintUnformatted(json_message);
    final_message->signed_message_bytes_length = strlen(final_message_string);
    final_message->signed_message_bytes = (uint8_t *)pvPortCalloc(final_message->signed_message_bytes_length, sizeof(uint8_t));
    memcpy(final_message->signed_message_bytes, final_message_string, final_message->signed_message_bytes_length);
    cJSON_Delete(json_message);
}

/*******************************************************************************************************************//**
 * @brief        Sends the message bytes as input to the network task.
 * @param[in]    endpoint           Buffer containing the cloud endpoint to which the data will be sent.
 * @param[in]    endpoint_length    Length of the endpoint in bytes.
 * @param[in]    final_message      Buffer containing the final_message structure to be sent.
 * @retval       None
 **********************************************************************************************************************/
void ethernet_send(char *endpoint, size_t endpoint_length, final_message_struct *final_message)
{
    xMessageBufferSend(crypto_net_message_buffer, (void *)endpoint, endpoint_length, pdMS_TO_TICKS(1000));
    char ack = {RESET_VALUE};
    size_t ackBytes = RESET_VALUE;
    do {
        ackBytes = xMessageBufferReceive(net_crypto_message_buffer, (void *)&ack, sizeof(ack), pdMS_TO_TICKS(1000));
    } while (ackBytes == 0);
    xMessageBufferSend(crypto_net_message_buffer, (void *)final_message->signed_message_bytes, final_message->signed_message_bytes_length,
                                               pdMS_TO_TICKS(1000));
}

/*******************************************************************************************************************//**
 * @brief        Frees resources from memory.
 * @param[in]    recipient_counter      Index of the DID document.
 * @param[in]    encryption_ctx         Buffer containing the encryption context structure.
 * @param[in]    message_ctx            Buffer containing the message context structure.
 * @param[in]    final_message_struct   Buffer containing the final_message structure.
 * @retval       None
 **********************************************************************************************************************/
void free_contexts(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context  *message_ctx, final_message_struct *final_message)
{
    // Free encryption_context
    vPortFree(encryption_ctx->did_documents[recipient_counter]->endpoint);
    vPortFree(encryption_ctx->did_documents[recipient_counter]->public_key_der_encoded);
    vPortFree(encryption_ctx->did_documents[recipient_counter]);
    encryption_ctx->aes_key_handle = (psa_key_handle_t)RESET_VALUE;
    
    // Free message_context
    vPortFree(message_ctx->battery_data_encrypted);
    vPortFree(message_ctx->der_encoded_ephemeral_key);
    vPortFree(message_ctx);
    
    // Free final_message_struct
    vPortFree(final_message->signed_message_bytes);
    vPortFree(final_message);
}

/*******************************************************************************************************************//**
 *  @brief       De-initialize the platform, print and trap error.
 *  @param[IN]   status    error status
 *  @param[IN]   err_str   error string
 *  @retval      None
 **********************************************************************************************************************/
void handle_error(psa_status_t status, char *err_str)
{
    /*mbedtls_psa_crypto_free();
    // De-initialize the platform.
    mbedtls_platform_teardown(&ctx_mbedtls);*/
    APP_ERR_PRINT(err_str);
    APP_ERR_TRAP(status);
}


