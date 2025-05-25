#ifndef INITIA_THREAD_H_
#define INITIA_THREAD_H_

#define SIGNING_KEY_256_BIT_LENGTH (256U)
#define SIGNING_KEY_ID ((psa_key_id_t) 6)

#define CHECK_PSA_SUCCESS(status, msg) \
    if (PSA_SUCCESS != (status))       \
    {                                  \
        APP_ERR_PRINT(msg);            \
    }

void generate_signing_key_pair(void);
void initialize_rtc(void);
fsp_err_t littlefs_init(void);
void deinit_littlefs(void);

#endif /* INITIA_THREAD_H_ */
