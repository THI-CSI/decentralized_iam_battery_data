package utils

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
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

// Generate256HashHex expects payload with json tags, marshalls it and then calculates a SHA-256 hash in hex format with that.
func Generate256HashHex(payload interface{}) (string, error) {
	jsonBytes, err := json.Marshal(payload)
	if err != nil {
		return "", err
	}
	hashBytes := sha256.Sum256(jsonBytes)
	return hex.EncodeToString(hashBytes[:]), nil
}
