package utils

import (
	"blockchain/internal/core"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"github.com/go-playground/validator/v10"
	"github.com/lestrrat-go/jwx/v3/jwa"
	"github.com/lestrrat-go/jwx/v3/jws"
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

func VerfiyJWS(chain *core.Blockchain, token string, didKeyFragment string) ([]byte, error) {
	key, err := chain.GetPublicKey(didKeyFragment)
	if err != nil {
		return nil, err
	}

	verified, err := jws.Verify([]byte(token), jws.WithKey(jwa.RS256(), key))
	if err != nil {
		return nil, err
	}
	// TODO: Compare the signed content currently unused return of jws.Verify contains the content that was signed with key - we need to compare this against the payload that was sent
	// We will need to umarshal the return value into the respected generated type and then compare them. Which is why I prepared the individual functions in server/services
	return verified, nil
}
