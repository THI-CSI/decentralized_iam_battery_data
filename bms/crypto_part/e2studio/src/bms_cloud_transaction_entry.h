#ifndef BMS_CLOUD_H_
#define BMS_CLOUD_H_

#define ECC_256_BIT_LENGTH (256U)
#define REC_PUB_LENGTH (65U)
#define ECC_256_PUB_SIZE (65U)
#define ECC_256_PUB_DER_MAX_SIZE (300U)
// #define ECC_PSA_KEY_SKIP (1U) // skip the PSA ECC key padding to get the key
#define TAG_LENGTH ((size_t)16U)
#define SIGNING_KEY_ID ((psa_key_id_t) 6)
#define DERIVED_AES_KEY_ID ((psa_key_id_t) 6)
#define AES_KEY_BITS (256U)
#define SALT_LENGTH (32U)
#define NONCE_LENGTH (12U)
#define AAD_LENGTH (12U)
#define INFO_LENGTH (20U)
#define DID_LENGTH (32U)
#define WAIT_TIME (500U)

#define CHECK_PSA_SUCCESS(status, msg) \
    if (PSA_SUCCESS != (status))       \
    {                                  \
        APP_ERR_PRINT(msg);            \
        return status;                 \
    }

#define CHECK_PSA_SUCCESS_DERIVATION(status, msg, op) \
    if (PSA_SUCCESS != (status))                 \
    {                                            \
        APP_ERR_PRINT(msg);                      \
        psa_key_derivation_abort((op));         \
        return status;                           \
    }

#ifdef USE_IPV6
    typedef int ip_type;
#else
    typedef char ip_type;
#endif /* USE_IPV6 */

typedef struct {
    ip_type ip[16];
    int did;
    uint8_t *public_key;
    size_t public_key_length;
} did_document;

typedef struct {
    uint8_t *battery_data_json;
    size_t battery_data_length;
    did_document **did_documents;
    psa_key_handle_t aes_key_handle;
} encryption_context;

typedef struct {
    uint8_t *battery_data_encrypted; /* aad: nonce */
    size_t encrypted_data_length;
    uint8_t aad[AAD_LENGTH]; /* == nonce */
    uint8_t salt[SALT_LENGTH];
    uint8_t did[DID_LENGTH];
    uint8_t *der_encoded_ephermal_key;
    size_t der_encoded_ephermal_key_length;
} message_context;

uint8_t fetch_did_documents(encryption_context *encryption_ctx);
void simulate_battery_data_query(encryption_context *encryption_ctx);
void prepare_message_ctx(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx);
psa_status_t crypto_operations(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx);
psa_status_t generate_ephermal_key_pair(message_context *message_ctx, psa_key_handle_t *ephermal_key_handle);
psa_status_t derive_encryption_key(message_context *message_ctx, encryption_context *encryption_ctx, uint8_t recipient_counter, psa_key_handle_t ephermal_key_handle);
psa_status_t encrypt_battery_data(encryption_context *encryption_ctx, message_context *message_ctx);
psa_status_t generate_signed_json_message(message_context *message_ctx);
unsigned char* create_message_string(message_context *message_ctx, size_t *concatenated_message_string_length);
psa_status_t ecc_hashing_operation(unsigned char *payload, uint8_t payload_length, uint8_t * payload_hash, size_t * payload_hash_len);
void ethernet_send(ip_type *ip_addr, message_context *message_ctx);
void handle_error(psa_status_t status, char * err_str);
fsp_err_t littlefs_init(void);
void deinit_littlefs(void);

#endif /* BMS_CLOUD_H_ */
