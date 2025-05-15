package utils

import (
	"blockchain/internal/api/web/server/domain"
	"errors"
	"regexp"
	"strings"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
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

func IsDidValid(did string) bool {
	if !strings.HasPrefix(did, "did:batterypass:") {
		return false
	}
	matched, _ := regexp.MatchString(`^did:[a-z0-9]+:[A-Za-z0-9._-]+$`, did)
	return matched
}
