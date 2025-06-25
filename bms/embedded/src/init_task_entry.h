#ifndef INIT_TASK_ENTRY_H
#define INIT_TASK_ENTRY_H

#define SIGNING_KEY_256_BIT_LENGTH (256U)
#define ECC_256_PUB_MAX_BUFFER_SIZE (70U)
#define ECC_256_PUB_DER_MAX_BUFFER_SIZE (128U)
#define SIGNING_KEY_ID ((psa_key_id_t) 6)

#define CHECK_PSA_SUCCESS(status, msg) \
    if (PSA_SUCCESS != (status))       \
    {                                  \
        APP_ERR_PRINT(msg);            \
    }

void send_and_generate_signing_key_pair(void);
void der_encoding_init(uint8_t *sign_pub_key, size_t sign_pub_key_length, unsigned char **sign_pub_key_der, size_t *sign_pub_key_der_length);
void ethernet_send_init(char *endpoint, size_t endpoint_length, unsigned char* sign_public_key_der_base64, size_t sign_public_key_der_base64_length);
void initialize_rtc(void);
fsp_err_t littlefs_init(void);
void deinit_littlefs(void);

#endif // INIT_TASK_ENTRY_H
