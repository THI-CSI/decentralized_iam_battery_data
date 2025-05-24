#include "common.h"
#include "bms_cloud_transaction.h"
#include "bms_cloud_transaction_entry.h"
#include "common_utils.h"
#include "portable.h"
#include "mbedtls/pk.h"
#include "mbedtls/ecp.h"
#include "rtc_init.h"

// platform context structure
mbedtls_platform_context ctx = {RESET_VALUE};

/* BMS2Cloud entry function */
/* pvParameters contains TaskHandle_t */
void bms_cloud_transaction_entry(void *pvParameters)
{
    FSP_PARAMETER_NOT_USED (pvParameters);
    // The rate at which the task waits on the Semaphore availability.
    TickType_t Semphr_wait_ticks = pdMS_TO_TICKS (WAIT_TIME);
    // Initialize RTC
    initialize_rtc();

    for (;;)
    {
        if (pdPASS == xSemaphoreTake(bms_cloud_sem, Semphr_wait_ticks))
        {
            // Initialize context_structs on heap
            encryption_context *encryption_ctx = (encryption_context *)pvPortCalloc(1, sizeof(encryption_context));
            message_context  *message_ctx = (message_context *)pvPortCalloc(1, sizeof(message_context));
            // Request DID-docs and initialize encryption_ctx->did_documents
            uint8_t number_of_endpoints = fetch_did_documents(encryption_ctx);
            // Query dynamic battery data
            simulate_battery_data_query(encryption_ctx);
            // Send message_ctx
            for (uint8_t i = 0; i < number_of_endpoints; i++)
            {
                // Initialize message_ctx
                prepare_message_ctx(i, encryption_ctx, message_ctx);
                // Send message_ctx to did_document[i]->ip
                ethernet_send(encryption_ctx->did_documents[i]->ip, message_ctx);
            }
        }
    }
}

void initialize_rtc()
{
    fsp_err_t err = FSP_SUCCESS;
    err = rtc_init();
    if (FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\n ** RTC INIT FAILED ** \r\n");
        APP_ERR_TRAP(err);
    }
    err = set_rtc_calendar_time();
    if (FSP_SUCCESS != err)
    {
        rtc_deinit();
        APP_ERR_PRINT("\r\nRTC Calendar Time Set failed.\r\nClosing the driver. Restart the Application\r\n");
        APP_ERR_TRAP(err);
    }
    err = set_rtc_calendar_alarm();
    if (FSP_SUCCESS != err)
    {
       rtc_deinit();
       APP_ERR_PRINT("\r\nPeriodic interrupt rate setting failed.\r\nClosing the driver. Restart the Application\r\n");
       APP_ERR_TRAP(err);
    }
}

void prepare_message_ctx(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx)
{
   psa_status_t       status                    = (psa_status_t)RESET_VALUE;
   int                mbed_ret_val              = RESET_VALUE;
   // Setup the platform; initialize the SCE
   mbed_ret_val = mbedtls_platform_setup(&ctx);
   if (RESET_VALUE != mbed_ret_val)
   {
       APP_ERR_PRINT("\r\n** mbedtls_platform_setup API FAILED ** \r\n");
       APP_ERR_TRAP(mbed_ret_val);
   }
   // Initialize crypto-library
   status = psa_crypto_init();
   if (PSA_SUCCESS != status)
   {
       APP_ERR_PRINT("\r\n** psa_crypto_init API FAILED ** \r\n");
       // De-initialize the platform
       mbedtls_platform_teardown(&ctx);
       APP_ERR_TRAP(status);
   }
   status = crypto_operations(recipient_counter, encryption_ctx, message_ctx);
   if (PSA_SUCCESS != status)
   {
       // HPKE operation failed. Perform cleanup and trap error.
       handle_error(status, "\r\n** Crypto-Operation FAILED ** \r\n");
   }
   // De-initialize the platform
   mbedtls_psa_crypto_free();
   mbedtls_platform_teardown(&ctx);
}

psa_status_t crypto_operations(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_key_handle_t ephermal_key_handle = (psa_key_handle_t)RESET_VALUE;
    // Generate ephermal-keypair & export public part in DER-Format
    status = generate_ephermal_key_pair(message_ctx, &ephermal_key_handle);
    CHECK_PSA_SUCCESS(status, "");
    // Derive encryption key - DHCP | HKDF(SHA2-256)
    status = derive_encryption_key(message_ctx, encryption_ctx, recipient_counter, ephermal_key_handle);
    CHECK_PSA_SUCCESS(status, "");
    // Encrypt battery data - AES-GCM 256
    status = encrypt_battery_data(encryption_ctx, message_ctx);
    CHECK_PSA_SUCCESS(status, "");
    // Generate signed JSON-message

    return status;
}

psa_status_t generate_ephermal_key_pair(message_context *message_ctx, psa_key_handle_t *ephermal_key_handle)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_key_attributes_t ecc_attributes = PSA_KEY_ATTRIBUTES_INIT;
    uint8_t ecc_pub_key[ECC_256_PUB_SIZE] = {RESET_VALUE};
    size_t ecc_pub_key_length = RESET_VALUE;
    uint8_t ecc_pub_key_der_encoded[ECC_256_PUB_DER_MAX_SIZE] = {RESET_VALUE};
    uint8_t *ecc_pub_key_der_write_ptr = ecc_pub_key_der_encoded + sizeof(ecc_pub_key_der_encoded);
    size_t ecc_pub_key_length_der_encoded = RESET_VALUE;

    // Set Key uses flags, key_algorithm, key_type, key_bits, key_lifetime
    psa_set_key_usage_flags(&ecc_attributes, PSA_KEY_USAGE_DERIVE);
    psa_set_key_algorithm(&ecc_attributes, PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(PSA_ALG_SHA_256)));
    psa_set_key_type(&ecc_attributes, PSA_KEY_TYPE_ECC_KEY_PAIR_WRAPPED(PSA_ECC_FAMILY_SECP_R1));
    psa_set_key_bits(&ecc_attributes, ECC_256_BIT_LENGTH);
    psa_set_key_lifetime(&ecc_attributes, PSA_KEY_LIFETIME_VOLATILE);

    // Generate ECC P256R1 Key pair
    status = psa_generate_key(&ecc_attributes, ephermal_key_handle);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_key API FAILED ** \r\n")

    // Export public key
    status = psa_export_public_key(*ephermal_key_handle, ecc_pub_key, ECC_256_PUB_SIZE , &ecc_pub_key_length);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_export_public_key API FAILED ** \r\n");

    // DER-encoding of public key
    mbedtls_pk_context ctx_pk;
    mbedtls_pk_init(&ctx_pk);
    mbedtls_ecp_keypair *ecp = mbedtls_calloc(1, sizeof(mbedtls_ecp_keypair)); // pvPortCalloc?
    mbedtls_ecp_keypair_init(ecp);

    mbedtls_ecp_group_load(&ecp->grp, MBEDTLS_ECP_DP_SECP256R1);
    mbedtls_ecp_point_read_binary(&ecp->grp, &ecp->Q, ecc_pub_key, ecc_pub_key_length);
    mbedtls_mpi_init(&ecp->d);
    mbedtls_pk_setup(&ctx_pk, mbedtls_pk_info_from_type(MBEDTLS_PK_ECKEY));
    ctx_pk.pk_ctx = ecp;
    ecc_pub_key_length_der_encoded = mbedtls_pk_write_pubkey_der(&ctx_pk, ecc_pub_key_der_encoded, sizeof(ecc_pub_key_der_encoded));
    message_ctx->der_encoded_ephermal_key = (uint8_t *)pvPortCalloc(1, ecc_pub_key_length_der_encoded);
    memcpy(message_ctx->der_encoded_ephermal_key, ecc_pub_key_der_write_ptr - ecc_pub_key_length_der_encoded, ecc_pub_key_length_der_encoded);

    return status;
}

psa_status_t derive_encryption_key(message_context *message_ctx, encryption_context *encryption_ctx, uint8_t recipient_counter, psa_key_handle_t ephermal_key_handle)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    psa_key_derivation_operation_t derivation_operation = PSA_KEY_DERIVATION_OPERATION_INIT;
    psa_key_attributes_t aes_attributes = PSA_KEY_ATTRIBUTES_INIT;
    did_document *did_doc = encryption_ctx->did_documents[recipient_counter];

    // Set Key uses flags, key_algorithm, key_type, key_bits, key_lifetime
    // ! To-do: wrapped aes-key
    psa_set_key_usage_flags(&aes_attributes, PSA_KEY_USAGE_ENCRYPT | PSA_KEY_USAGE_DECRYPT);
    psa_set_key_algorithm(&aes_attributes, PSA_ALG_GCM);
    psa_set_key_type(&aes_attributes, PSA_KEY_TYPE_AES_WRAPPED);
    psa_set_key_bits(&aes_attributes, AES_KEY_BITS);
    psa_set_key_lifetime(&aes_attributes, PSA_KEY_LIFETIME_VOLATILE);

    // Generate random Salt value
    status = psa_generate_random(message_ctx->salt, SALT_LENGTH);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_random API FAILED ** \r\n");

    // Shared-Secret agreement and aes-key derivation
    status = psa_key_derivation_setup(&derivation_operation, PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(PSA_ALG_SHA_256)));
    CHECK_PSA_SUCCESS(status, "\r\n** psa_key_derivation_setup API FAILED ** \r\n");
    status = status = psa_key_derivation_set_capacity(&derivation_operation, AES_KEY_BITS);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_key_derivation_set_capacity API FAILED ** \r\n");
    status = psa_key_derivation_input_bytes(&derivation_operation, PSA_KEY_DERIVATION_INPUT_SALT, message_ctx->salt, SALT_LENGTH);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_input_bytes API FAILED ** \r\n", &derivation_operation);
    status = psa_key_derivation_key_agreement(&derivation_operation, PSA_KEY_DERIVATION_INPUT_SECRET, ephermal_key_handle, did_doc->public_key, did_doc->public_key_length);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_input_key_agreement API FAILED ** \r\n", &derivation_operation);
    status = psa_key_derivation_input_bytes(&derivation_operation, PSA_KEY_DERIVATION_INPUT_INFO, did_doc->public_key, did_doc->public_key_length);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_input_bytes API FAILED ** \r\n", &derivation_operation);
    status = psa_key_derivation_output_key(&aes_attributes, &derivation_operation, &encryption_ctx->aes_key_handle);
    CHECK_PSA_SUCCESS_DERIVATION(status, "\r\n** psa_key_derivation_output_key API FAILED ** \r\n", &derivation_operation);

    // Abort derivation_operation and destroy ephermal_key_pair
    psa_key_derivation_abort(&derivation_operation);
    status = psa_destroy_key(ephermal_key_handle);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_destroy_key API FAILED ** \r\n");

    return status;
}

psa_status_t encrypt_battery_data(encryption_context *encryption_ctx, message_context *message_ctx)
{
    psa_status_t status = (psa_status_t)RESET_VALUE;
    uint8_t nonce[NONCE_LENGTH] = {RESET_VALUE};
    size_t encrypted_data_size = RESET_VALUE;

    // Generate IV (96 bits), calculate encrypted_data_size and allocate heap for encrypted data
    status = psa_generate_random(nonce, NONCE_LENGTH);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_random API FAILED ** \r\n");
    encrypted_data_size = encryption_ctx->battery_data_length + TAG_LENGTH;
    message_ctx->battery_data_encrypted = (uint8_t *)pvPortCalloc(1, encrypted_data_size);
    if (NULL == message_ctx->battery_data_encrypted)
    {
        APP_ERR_PRINT("\r\n** Out Of Memory. ** \r\n");
        return FSP_ERR_OUT_OF_MEMORY;
    }
    memcpy(message_ctx->aad, nonce, NONCE_LENGTH);

    // AES-GCM 256 encryption
    status = psa_aead_encrypt(encryption_ctx->aes_key_handle, PSA_ALG_GCM, nonce, NONCE_LENGTH, message_ctx->aad, AAD_LENGTH, encryption_ctx->battery_data_json,
                              encryption_ctx->battery_data_length, message_ctx->battery_data_encrypted, encrypted_data_size, &message_ctx->encrypted_data_length);
    CHECK_PSA_SUCCESS(status, "\r\n** psa_aead_encrypt API FAILED ** \r\n");

    return status;
}

/*******************************************************************************************************************//**
 *  @brief       Initialize Littlefs operation.
 *  @param[IN]   None
 *  @retval      FSP_SUCCESS or any other possible error code
 **********************************************************************************************************************/
fsp_err_t littlefs_init(void)
{
    fsp_err_t          err                       = FSP_SUCCESS;
    int                lfs_err                   = RESET_VALUE;

    /* Open LittleFS Flash port.*/
    err = RM_LITTLEFS_FLASH_Open(&g_rm_littlefs0_ctrl, &g_rm_littlefs0_cfg);
    if(FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\n** RM_LITTLEFS_FLASH_Open API FAILED ** \r\n");
        return err;
    }

    /* Format the filesystem. */
    lfs_err = lfs_format(&g_rm_littlefs0_lfs, &g_rm_littlefs0_lfs_cfg);
    if(RESET_VALUE != lfs_err)
    {
        APP_ERR_PRINT("\r\n** lfs_format API FAILED ** \r\n");
        deinit_littlefs();
        return (fsp_err_t)lfs_err;
    }

    /* Mount the filesystem. */
    lfs_err = lfs_mount(&g_rm_littlefs0_lfs, &g_rm_littlefs0_lfs_cfg);
    if(RESET_VALUE != lfs_err)
    {
        APP_ERR_PRINT("\r\n** lfs_mount API FAILED ** \r\n");
        deinit_littlefs();
        return (fsp_err_t)lfs_err;
    }
    return err;
}

/*******************************************************************************************************************//**
 *  @brief       De-Initialize the Littlefs.
 *  @param[IN]   None
 *  @retval      None
 **********************************************************************************************************************/
void deinit_littlefs(void)
{
    fsp_err_t          err                       = FSP_SUCCESS;
    /*Closes the lower level driver */
    err = RM_LITTLEFS_FLASH_Close(&g_rm_littlefs0_ctrl);
    /* Handle error */
    if(FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\n** RM_LITTLEFS_FLASH_Close API FAILED ** \r\n");
    }
}

/*******************************************************************************************************************//**
 *  @brief       De-initialize the platform, print and trap error.
 *  @param[IN]   status    error status
 *  @param[IN]   err_str   error string
 *  @retval      None
 **********************************************************************************************************************/
void handle_error(psa_status_t status, char * err_str)
{
    mbedtls_psa_crypto_free();
    /* De-initialize the platform.*/
    mbedtls_platform_teardown(&ctx);
    APP_ERR_PRINT(err_str);
    APP_ERR_TRAP(status);
}


