package server

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/handlers"
	"blockchain/internal/api/web/server/services"

	_ "blockchain/docs/swagger" // Required for Swagger documentation

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/swagger"
)

// NewServer initializes and returns a configured Fiber application.
func New() *fiber.App {
	app := fiber.New(fiber.Config{
		ServerHeader: "blockchain",
		AppName:      "blockchain",
		ErrorHandler: domain.CustomErrorHandler,
	})

	app.Use(logger.New(logger.Config{
		Format:     "${cyan}[${time}] ${white}${pid} ${red}${status} ${blue}[${method}] ${white}${path}\n",
		TimeFormat: "02-Jan-2006",
		TimeZone:   "UTC",
	}))

	// Swagger documentation route
	app.Get("/swagger/*", swagger.HandlerDefault)

	apiRoutes := app.Group("/api")

	apiRoutes.Get("/status", func(c *fiber.Ctx) error {
		return c.SendString("ok")
	})

	// Instantiate the DID service
	didService := services.NewDidService()

	// Register all handlers related to did
	apiRoutes.Post("/v1/did", handlers.CreateDid(didService))
	apiRoutes.Put("/v1/grant", handlers.GrantAccessRight(didService))
	apiRoutes.Get("/v1/grants/:did", handlers.GetAccessRightsForDid(didService))

	return app
}
