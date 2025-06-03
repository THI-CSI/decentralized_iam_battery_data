package utils

import (
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
