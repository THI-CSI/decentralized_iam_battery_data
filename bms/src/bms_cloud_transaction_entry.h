#ifndef BMS_CLOUD_H_
#define BMS_CLOUD_H_

#define WAIT_TIME (500U)
#define MAX_MODFIED_DATA_BUFFER (500U)
#define ECC_256_PUB_MAX_BUFFER_SIZE (70U)
#define ENDPOINT_MAX_BUFFER_SIZE (200U)
#define ECC_256_BIT_LENGTH (256U)
#define ECC_256_PUB_DER_MAX_BUFFER_SIZE (128U)
#define ECC_256_PUB_RAW_LENGTH (65U)
#define AES_KEY_BITS (256U)
#define SALT_LENGTH (32U)
#define NONCE_LENGTH (12U)
#define AAD_LENGTH (12U)
#define DID_LENGTH (29U)
#define TIMESTAMP_LENGTH (19U)
#define SIGNING_KEY_ID ((psa_key_id_t) 6)

#define CHECK_PSA_SUCCESS(status, msg) \
    if (PSA_SUCCESS != (status))       \
    {                                  \
        APP_ERR_PRINT(msg);            \
        return status;                 \
    }

#define CHECK_PSA_SUCCESS_DERIVATION(status, msg, op) \
    if (PSA_SUCCESS != (status))                      \
    {                                                 \
        APP_ERR_PRINT(msg);                           \
        psa_key_derivation_abort((op));               \
        return status;                                \
    }

#define CHECK_JSON_STATUS(object, json_item) \
    if (NULL == object) {                    \
        cJSON_Delete(json_item);             \
    }

typedef struct {
    char *endpoint;
    size_t endpoint_length;
    uint8_t public_key[ECC_256_PUB_RAW_LENGTH];
    uint8_t *public_key_der_encoded;
    size_t public_key_der_encoded_length;
} did_document;

typedef struct {
    uint8_t *battery_data;
    size_t battery_data_length;
    did_document **did_documents;
    psa_key_handle_t aes_key_handle;
    uint8_t *der_encoded_signing_pub_key;
    size_t der_encoded_signing_pub_key_length;
} encryption_context;

typedef struct {
    uint8_t *battery_data_encrypted; /* aad: nonce */
    size_t encrypted_data_length;
    uint8_t aad[AAD_LENGTH]; /* == nonce */
    uint8_t salt[SALT_LENGTH];
    uint8_t *der_encoded_ephermal_key;
    size_t der_encoded_ephermal_key_length;
    uint8_t timestamp_bytes[TIMESTAMP_LENGTH];
} message_context;

typedef struct {
    uint8_t *signed_message_bytes;
    size_t signed_message_bytes_length;
} final_message_struct;

uint8_t fetch_did_documents(encryption_context *encryption_ctx);
void simulate_battery_data_query(encryption_context *encryption_ctx);
int get_number_of_full_battery_cycles(void);
double get_energy_throughput(void);
double get_time_extreme_high_temperature(void);
void prepare_message_ctx(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx, final_message_struct *final_message);
psa_status_t crypto_operations(uint8_t recipient_counter, encryption_context *encryption_ctx, message_context *message_ctx, final_message_struct *final_message);
psa_status_t generate_ephermal_key_pair(message_context *message_ctx, psa_key_handle_t *ephermal_key_handle);
psa_status_t derive_encryption_key(message_context *message_ctx, encryption_context *encryption_ctx, uint8_t recipient_counter, psa_key_handle_t ephermal_key_handle);
void der_encoding(uint8_t *ecc_pub_key, size_t ecc_pub_key_length, uint8_t **der_encoded_key_buffer, size_t *der_encoded_key_buffer_length);
void der_decoding(uint8_t *ecc_pub_key_der, size_t ecc_pub_key_der_length, uint8_t *raw_key_buffer);
psa_status_t encrypt_battery_data(encryption_context *encryption_ctx, message_context *message_ctx);
psa_status_t generate_signed_json_message(message_context *message_ctx, final_message_struct *final_message);
void create_message_string(message_context *message_ctx, uint8_t **concatenated_message_bytes, size_t *concatenated_message_bytes_length, cJSON *message_json);
psa_status_t ecc_hashing_operation(uint8_t *concatenated_message_bytes, size_t concatenated_message_bytes_length, uint8_t *concatenated_message_bytes_hash, size_t *concatenated_message_bytes_hash_length);
void generate_final_signed_json_message(cJSON* json_message, uint8_t *signature, size_t signature_length, final_message_struct *final_message);
void ethernet_send(char *endpoint, size_t endpoint_length, final_message_struct *final_message);
void handle_error(psa_status_t status, char * err_str);

#endif /* BMS_CLOUD_H_ */
