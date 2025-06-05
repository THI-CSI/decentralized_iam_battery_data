package utils

import (
	"encoding/json"
	"errors"
	"github.com/go-playground/validator/v10"
	"regexp"
)

// Validate is a shared instance of the validator used for struct validation.
// It uses tags (e.g., `validate:"required"`) defined in struct fields.
var Validate = validator.New()

// IsDidValid Checks if the DID conforms to the specified format.
func IsDidValid(did string) bool {
	matched, _ := regexp.MatchString(`^did:batterypass:[a-zA-Z0-9.\-]+$`, did)
	return matched
}

// IsUrnValid Validates if the input string is a valid URN according to the UUID pattern.
func IsUrnValid(urn string) bool {
	matched, _ := regexp.MatchString(`^urn:uuid:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$`, urn)
	return matched
}

// PayloadProjection projects the raw payload data from the rawBody
func PayloadProjection(rawBody []byte, requestBody interface{}) ([]byte, error) {
	if err := json.Unmarshal(rawBody, &requestBody); err != nil {
		return nil, err
	}

	var tempMap map[string]json.RawMessage
	if err := json.Unmarshal(rawBody, &tempMap); err != nil {
		return nil, errors.New("Failed to parse raw body for payload extraction")
	}

	rawPayloadBytes, err := tempMap["payload"]
	if err {
		return nil, errors.New("Request body missing 'payload' field")
	}

	return rawPayloadBytes, nil
}
