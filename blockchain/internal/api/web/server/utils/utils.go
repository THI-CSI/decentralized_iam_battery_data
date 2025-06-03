package utils

import (
	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"regexp"
)

// Validate is a shared instance of the validator used for struct validation.
// It uses tags (e.g., `validate:"required"`) defined in struct fields.
var Validate = validator.New()

// WriteResponse sets the content type to JSON and writes a structured response with a given status code.
// This helps standardize response formatting throughout the application.
func WriteResponse(c *fiber.Ctx, statusCode int, obj any) error {
	c.Set("Content-Type", "application/json")
	return c.Status(statusCode).JSON(obj)
}

// IsDidValid Checks if the DID starts with "did:batterypass:" and conforms to the specified format.
func IsDidValid(did string) bool {
	matched, _ := regexp.MatchString(`^did:batterypass:(eu|oem|cloud|bms|service)\\.[a-zA-Z0-9.\\-]+$`, did)
	return matched
}

// IsUrnValid Validates if the input string is a valid URN according to the UUID pattern.
func IsUrnValid(urn string) bool {
	matched, _ := regexp.MatchString(`^urn:uuid:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$`, urn)
	return matched
}
