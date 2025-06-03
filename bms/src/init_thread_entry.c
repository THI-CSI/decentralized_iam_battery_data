#include "common.h"
#include "init_thread.h"
#include "init_thread_entry.h"
#include "common_utils.h"
#include "rtc_init.h"
#include "mbedtls/pk.h"
#include "mbedtls/ecp.h"
#include "mbedtls/base64.h"

/* CustomInit entry function */
/* pvParameters contains TaskHandle_t */
void init_thread_entry(void *pvParameters)
{
    FSP_PARAMETER_NOT_USED (pvParameters);
    // Key Pair generation
    send_and_generate_signing_key_pair();
    // Initialize RTC
    initialize_rtc();
    // Initializing finished - vTaskDelete
    vTaskDelete(NULL);
}

/*******************************************************************************************************************//**
 *  @brief       Generate bms_signing_key_pair and register with blockchain.
 *  @param[IN]   None
 *  @retval      None
 **********************************************************************************************************************/
void send_and_generate_signing_key_pair()
{
    psa_key_handle_t signing_key_handle = RESET_VALUE;
    psa_status_t status = (psa_status_t)RESET_VALUE;
    int mbed_ret_val = RESET_VALUE;
    mbedtls_platform_context ctx_mbedtls = {RESET_VALUE};
    // Setup the platform; initialize the SCE
    mbed_ret_val = mbedtls_platform_setup(&ctx_mbedtls);
    if (RESET_VALUE != mbed_ret_val)
    {
        APP_ERR_PRINT("\r\n** mbedtls_platform_setup API FAILED ** \r\n");
        APP_ERR_TRAP(mbed_ret_val);
    }
    // Initialize littlefs
    if (FSP_SUCCESS != littlefs_init())
    {
        APP_ERR_PRINT("\r\n** littlefs operation failed. ** \r\n");
    }
    // Initialize crypto library
    status = psa_crypto_init();
    if (PSA_SUCCESS != status)
    {
        APP_ERR_PRINT("\r\n** psa_crypto_init API FAILED ** \r\n");
        /* De-initialize the platform.*/
        mbedtls_platform_teardown(&ctx_mbedtls);
        APP_ERR_TRAP(status);
    }
	status = psa_open_key(SIGNING_KEY_ID, &signing_key_handle);
	if (PSA_SUCCESS == status)
    {
        status = psa_close_key(signing_key_handle);
        CHECK_PSA_SUCCESS(status, "\r\n** psa_close_key API FAILED ** \r\n");
    } else
    {
        psa_key_attributes_t signing_key_attributes = PSA_KEY_ATTRIBUTES_INIT;
        // Set Key uses flags, key_algorithm, key_type, key_bits, key_lifetime, key_id
        psa_set_key_usage_flags(&signing_key_attributes, PSA_KEY_USAGE_SIGN_HASH | PSA_KEY_USAGE_SIGN_MESSAGE);
        psa_set_key_algorithm(&signing_key_attributes, PSA_ALG_ECDSA(PSA_ALG_SHA_256));
        psa_set_key_type(&signing_key_attributes, PSA_KEY_TYPE_ECC_KEY_PAIR_WRAPPED(PSA_ECC_FAMILY_SECP_R1));
        psa_set_key_bits(&signing_key_attributes, SIGNING_KEY_256_BIT_LENGTH);
        psa_set_key_lifetime(&signing_key_attributes, PSA_KEY_LIFETIME_PERSISTENT);
        psa_set_key_id(&signing_key_attributes, SIGNING_KEY_ID);

        // Generate ECC P256R1 Key pair
        status = psa_generate_key(&signing_key_attributes, &signing_key_handle);
        CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_key API FAILED ** \r\n");
        
        // Register public key in blockchain
        uint8_t sign_pub_key[ECC_256_PUB_MAX_BUFFER_SIZE] = {RESET_VALUE};
        size_t sign_pub_key_length = RESET_VALUE;
        unsigned char *sign_pub_key_der;
        size_t sign_pub_key_der_length;
        // DER encoding
        status = psa_export_public_key(signing_key_handle, sign_pub_key, ECC_256_PUB_MAX_BUFFER_SIZE, &sign_pub_key_length);
        CHECK_PSA_SUCCESS(status, "\r\n** psa_export_public_key API FAILED ** \r\n");
        der_encoding_init(sign_pub_key, sign_pub_key_length, &sign_pub_key_der, &sign_pub_key_der_length);
        // Base64 encoding
        size_t sign_pub_key_der_base64_size = (size_t) ((sign_pub_key_der_length + 2) / 3.0) * 4 + 1;
        size_t sign_pub_key_der_base64_bytes_written = RESET_VALUE;
        unsigned char sign_pub_key_der_base64[sign_pub_key_der_base64_size];
        mbedtls_base64_encode(sign_pub_key_der_base64, sign_pub_key_der_base64_size, &sign_pub_key_der_base64_bytes_written,
                              sign_pub_key_der, sign_pub_key_der_length);
        ethernet_send_init("http://blockchain-endpoint", strlen("http://blockchain-endpoint"), sign_pub_key_der_base64, sign_pub_key_der_base64_bytes_written);
         
        // Free memory
        vPortFree(sign_pub_key_der);
        status = psa_close_key(signing_key_handle);
        CHECK_PSA_SUCCESS(status, "\r\n** psa_close_key API FAILED ** \r\n");
    }
    mbedtls_psa_crypto_free();
    mbedtls_platform_teardown(&ctx_mbedtls);
}

void der_encoding_init(uint8_t *sign_pub_key, size_t sign_pub_key_length, unsigned char **sign_pub_key_der, size_t *sign_pub_key_der_length)
{
    unsigned char sign_pub_key_der_encoded[ECC_256_PUB_DER_MAX_BUFFER_SIZE] = {RESET_VALUE};
    unsigned char *sign_pub_key_der_write_ptr = sign_pub_key_der_encoded + sizeof(sign_pub_key_der_encoded);
    
    mbedtls_pk_context ctx_pk;
    mbedtls_pk_init(&ctx_pk);
    mbedtls_ecp_keypair *ecp = mbedtls_calloc(1, sizeof(mbedtls_ecp_keypair)); // pvPortCalloc?
    mbedtls_ecp_keypair_init(ecp);
    mbedtls_ecp_group_load(&ecp->grp, MBEDTLS_ECP_DP_SECP256R1);
    mbedtls_ecp_point_read_binary(&ecp->grp, &ecp->Q, sign_pub_key, sign_pub_key_length);
    mbedtls_mpi_init(&ecp->d);
    mbedtls_pk_setup(&ctx_pk, mbedtls_pk_info_from_type(MBEDTLS_PK_ECKEY));
    ctx_pk.pk_ctx = ecp;
    
    *sign_pub_key_der_length = (size_t)mbedtls_pk_write_pubkey_der(&ctx_pk, sign_pub_key_der_encoded, sizeof(sign_pub_key_der_encoded));
    *sign_pub_key_der = (uint8_t *)pvPortCalloc(*sign_pub_key_der_length, sizeof(char));
    memcpy(*sign_pub_key_der, (uint8_t *)(sign_pub_key_der_write_ptr - *sign_pub_key_der_length), *sign_pub_key_der_length);
    
    mbedtls_ecp_keypair_free(ecp);
    mbedtls_pk_free(&ctx_pk);
}

void ethernet_send_init(char *endpoint, size_t endpoint_length, unsigned char* sign_public_key_der_base64, size_t sign_public_key_der_base64_length)
{
    size_t xBytesSentEndpoint = RESET_VALUE;
    size_t xBytesSentMessage = RESET_VALUE;
    xBytesSentEndpoint = xMessageBufferSend(crypto_net_message_buffer, (void *)endpoint, endpoint_length, pdMS_TO_TICKS(1000));
    do {
        xBytesSentMessage = xMessageBufferSend(crypto_net_message_buffer, (void *)sign_public_key_der_base64, sign_public_key_der_base64_length,
                                               pdMS_TO_TICKS(1000));
    } while (xBytesSentMessage > 0);
}

/*******************************************************************************************************************//**
 *  @brief       Initialize the RTC.
 *  @param[IN]   None
 *  @retval      None
 **********************************************************************************************************************/
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

/*******************************************************************************************************************//**
 *  @brief       Initialize Littlefs operation.
 *  @param[IN]   None
 *  @retval      FSP_SUCCESS or any other possible error code
 **********************************************************************************************************************/
fsp_err_t littlefs_init(void)
{
    fsp_err_t          err                       = FSP_SUCCESS;
    int                lfs_err                   = RESET_VALUE;

    err = RM_LITTLEFS_FLASH_Open(&g_rm_littlefs0_ctrl, &g_rm_littlefs0_cfg);
    if(FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\n** RM_LITTLEFS_FLASH_Open API FAILED ** \r\n");
        return err;
    }
    lfs_err = lfs_format(&g_rm_littlefs0_lfs, &g_rm_littlefs0_lfs_cfg);
    if(RESET_VALUE != lfs_err)
    {
        APP_ERR_PRINT("\r\n** lfs_format API FAILED ** \r\n");
        deinit_littlefs();
        return (fsp_err_t)lfs_err;
    }
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
    if(FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\n** RM_LITTLEFS_FLASH_Close API FAILED ** \r\n");
    }
}
