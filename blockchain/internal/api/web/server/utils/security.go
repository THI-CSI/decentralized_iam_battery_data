package utils

import (
	"blockchain/internal/api/web/server/domain"
	"crypto/ed25519"
	"encoding/base64"
	"errors"
	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"github.com/multiformats/go-multibase"
	"regexp"
	"strings"
)

// ParseAndValidateStruct parses the request body into a generic type T,
// then validates it using the validator library.
// Returns a pointer to the parsed object, or a Fiber-compatible error if parsing or validation fails.
func ParseAndValidateStruct[T any](c *fiber.Ctx) (*T, error) {
	c.Accepts("application/json")

	var payload T

	// Attempt to parse the JSON request body into the payload struct
	if err := c.BodyParser(&payload); err != nil {
		return nil, domain.ParserError(err)
	}

	// Validate the parsed struct against any `validate:"..."` tags
	if err := Validate.Struct(payload); err != nil {
		var validationErr validator.ValidationErrors
		errors.As(err, &validationErr)
		return nil, domain.ValidationError(validationErr)
	}

	return &payload, nil
}

// IsDidValid Checks if the DID starts with "did:batterypass:" and conforms to the specified format.
func IsDidValid(did string) bool {
	if !strings.HasPrefix(did, "did:batterypass:") {
		return false
	}
	matched, _ := regexp.MatchString(`^did:[a-z0-9]+:[A-Za-z0-9._-]+$`, did)
	return matched
}

// IsUrnValid Validates if the input string is a valid URN according to the UUID pattern.
func IsUrnValid(urn string) bool {
	matched, _ := regexp.MatchString(`^urn:uuid:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$`, urn)
	return matched
}

// VerifySignature verifies an Ed25519 signature using a public key in multibase format.
// The public key must have a multicodec prefix of 0xED (Ed25519).
func VerifySignature(data []byte, signatureB64, publicKeyMultibase string) error {
	// Decode the multibase-encoded public key
	_, decoded, err := multibase.Decode(publicKeyMultibase)
	if err != nil {
		return errors.New("invalid multibase-encoded public key")
	}

	// Ensure the multicodec prefix is 0xED for Ed25519
	if len(decoded) < 1 || decoded[0] != 0xED {
		return errors.New("missing or invalid Ed25519 multicodec prefix")
	}

	// Extract the actual public key bytes
	pubKeyBytes := decoded[1:]
	if len(pubKeyBytes) != ed25519.PublicKeySize {
		return errors.New("invalid public key length after decoding")
	}
	pubKey := ed25519.PublicKey(pubKeyBytes)

	// Decode the base64-encoded signature
	sigBytes, err := base64.StdEncoding.DecodeString(signatureB64)
	if err != nil {
		return errors.New("invalid base64 signature")
	}
	if len(sigBytes) != ed25519.SignatureSize {
		return errors.New("invalid signature length")
	}

	// Verify the signature
	if !ed25519.Verify(pubKey, data, sigBytes) {
		return errors.New("signature verification failed")
	}

	return nil
}
