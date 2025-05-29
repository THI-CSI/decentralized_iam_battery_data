#include "common.h"
#include "init_thread.h"
#include "init_thread_entry.h"
#include "common_utils.h"
#include "rtc_init.h"
#include "mbedtls/pk.h"
#include "mbedtls/ecp.h"

/* CustomInit entry function */
/* pvParameters contains TaskHandle_t */
void init_thread_entry(void *pvParameters)
{
    FSP_PARAMETER_NOT_USED (pvParameters);
    // Key Pair generation
    generate_signing_key_pair();
    // Initialize RTC
    initialize_rtc();
    // Initializing finished - vTaskDelete
    vTaskDelete(NULL);
}

void generate_signing_key_pair()
{
    psa_key_handle_t signing_key_handle = RESET_VALUE;
    psa_status_t status = (psa_status_t)RESET_VALUE;
    if (PSA_SUCCESS == psa_open_key(SIGNING_KEY_ID, &signing_key_handle))
    {
        status = psa_close_key(signing_key_handle);
        CHECK_PSA_SUCCESS(status, "\r\n** psa_close_key API FAILED ** \r\n");
    } else
    {
        int mbed_ret_val = RESET_VALUE;
        mbedtls_platform_context ctx = {RESET_VALUE};
        psa_key_attributes_t signing_key_attributes = PSA_KEY_ATTRIBUTES_INIT;

        // Setup the platform; initialize the SCE
        mbed_ret_val = mbedtls_platform_setup(&ctx);
        if (RESET_VALUE != mbed_ret_val)
        {
            APP_ERR_PRINT("\r\n** mbedtls_platform_setup API FAILED ** \r\n");
            APP_ERR_TRAP(mbed_ret_val);
        }
        // Initialize crypto library
        status = psa_crypto_init();
        if (PSA_SUCCESS != status)
        {
            APP_ERR_PRINT("\r\n** psa_crypto_init API FAILED ** \r\n");
            /* De-initialize the platform.*/
            mbedtls_platform_teardown(&ctx);
            APP_ERR_TRAP(status);
        }
        // Initialize littlefs
        if (FSP_SUCCESS != littlefs_init())
        {
            APP_ERR_PRINT("\r\n** littlefs operation failed. ** \r\n");
        }
        // Set Key uses flags, key_algorithm, key_type, key_bits, key_lifetime, key_id
        psa_set_key_usage_flags(&signing_key_attributes, PSA_KEY_USAGE_SIGN_HASH | PSA_KEY_USAGE_SIGN_MESSAGE);
        psa_set_key_algorithm(&signing_key_attributes, PSA_ALG_ECDSA(PSA_ALG_SHA_256));
        psa_set_key_type(&signing_key_attributes, PSA_KEY_TYPE_ECC_KEY_PAIR_WRAPPED(PSA_ECC_FAMILY_SECP_R1));
        psa_set_key_bits(&signing_key_attributes, SIGNING_KEY_256_BIT_LENGTH);
        psa_set_key_lifetime(&signing_key_attributes, PSA_KEY_LIFETIME_PERSISTENT);
        psa_set_key_id(&signing_key_attributes, SIGNING_KEY_ID);

        status = psa_generate_key(&signing_key_attributes, &signing_key_handle);
        CHECK_PSA_SUCCESS(status, "\r\n** psa_generate_key API FAILED ** \r\n");
        status = psa_close_key(signing_key_handle);
        CHECK_PSA_SUCCESS(status, "\r\n** psa_close_key API FAILED ** \r\n");
        mbedtls_psa_crypto_free();
        mbedtls_platform_teardown(&ctx);
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
