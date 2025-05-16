package domain

import (
	"errors"
	"fmt"
	"log"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
)

// ErrorResponseHTTP defines the structure for HTTP error responses.
// It contains a single field "message" to convey the error description.
type ErrorResponseHTTP struct {
	// Message contains the human-readable error message.
	Message string `json:"message"`
}

// ParserError returns a new Fiber error with status 400 (Bad Request)
// and a formatted message indicating a parser error.
// Typically used when request body parsing fails (e.g., invalid JSON).
func ParserError(err error) *fiber.Error {
	return fiber.NewError(fiber.StatusBadRequest, fmt.Sprintf("Parser error: %v", err.Error()))
}

// ValidationError returns a new Fiber error with status 400 (Bad Request)
// and a message describing validation failures.
// Used when input payload validation using the validator package fails.
func ValidationError(error validator.ValidationErrors) *fiber.Error {
	return fiber.NewError(fiber.StatusBadRequest, fmt.Sprintf("invalid payload: %v", error.Error()))
}

// CreatedError returns a 201 status code with fiber
func CreatedError(err string) *fiber.Error {
	return fiber.NewError(fiber.StatusCreated)
}

// BadRequestError returns a 400 status code with fiber
func BadRequestError(err string) *fiber.Error {
	return fiber.NewError(fiber.StatusBadRequest, err)
}

// NotFoundError returns a 404 status code with fiber
func NotFoundError(err string) *fiber.Error {
	return fiber.NewError(fiber.StatusNotFound, err)
}

// CustomErrorHandler is a centralized error handler for Fiber.
// It handles both Fiber-specific errors and generic application errors,
// and returns structured JSON responses accordingly.
func CustomErrorHandler(c *fiber.Ctx, err error) error {
	// Try to cast the error to a Fiber error
	var fiberErr *fiber.Error
	if errors.As(err, &fiberErr) {
		// Log Fiber-specific error details (optional, for debugging)
		log.Printf("Fiber error: %v", fiberErr)

		// Return a custom response for Fiber errors
		return c.Status(fiberErr.Code).JSON(fiber.Map{
			"message": fiberErr.Message,
		})
	}

	// Log and handle unexpected or non-Fiber errors
	log.Printf("Internal server error: %v", err)

	// Return a generic 500 Internal Server Error response
	return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
		"message": "Internal Server Error",
	})
}
