#ifndef INITIA_THREAD_H_
#define INITIA_THREAD_H_

#define SIGNING_KEY_256_BIT_LENGTH (256U)
#define ECC_256_PUB_MAX_BUFFER_SIZE (70U)
#define ECC_256_PUB_DER_MAX_BUFFER_SIZE (128U)
#define SIGNING_KEY_ID ((psa_key_id_t) 6)
#define FLASH_HP_DF_BLOCK_SIZE (64)
#define FLASH_HP_DF_BLOCK_0 (0x08000000U) /*   64 B:  0x40100000 - 0x4010003F */
#define FLASH_HP_DF_BLOCK_1 (0x40100040U) /*   64 B:  0x40100040 - 0x4010007F */
#define BLOCK_NUM (1)

#define CHECK_PSA_SUCCESS(status, msg) \
    if (PSA_SUCCESS != (status))       \
    {                                  \
        APP_ERR_PRINT(msg);            \
    }

#define CHECK_FSP_SUCCESS(status, msg) \
    if (PSA_SUCCESS != (status))       \
    {                                  \
        APP_ERR_PRINT(msg);            \
        return status;                 \
    }

void send_and_generate_signing_key_pair(void);
void der_encoding_init(uint8_t *sign_pub_key, size_t sign_pub_key_length, unsigned char **sign_pub_key_der, size_t *sign_pub_key_der_length);
void ethernet_send_init(char *endpoint, size_t endpoint_length, unsigned char* sign_public_key_der_base64, size_t sign_public_key_der_base64_length);
void write_did_to_data_flash(char *did, size_t did_length);
fsp_err_t flash_hp_data_flash_operations(char *did, size_t did_length);
void flash_hp_deinit(void);
void initialize_rtc(void);
fsp_err_t littlefs_init(void);
void deinit_littlefs(void);

#endif /* INITIA_THREAD_H_ */
