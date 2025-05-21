package server

import (
	_ "blockchain/docs/swagger" // Required for Swagger documentation
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/handlers"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/core"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/swagger"
)

// New initializes and returns a configured Fiber application.
func New(chain *core.Blockchain) *fiber.App {
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

	apiRoutes := app.Group("/api/v1/")

	apiRoutes.Get("/status", func(c *fiber.Ctx) error {
		return c.SendString("ok")
	})

	didService := services.NewDidService(chain)
	vcService := services.NewVCService(chain)
	blockService := services.NewBlockService(chain)
	transactionService := services.NewTransactionService(chain)

	// all blocks routes
	apiRoutes.Get("/blocks", handlers.GetBlocks(blockService))
	apiRoutes.Get("/blocks/:blockId", handlers.GetBlock(blockService))
	apiRoutes.Get("/blocks/:blockId/transactions", handlers.GetTransactions(transactionService))

	// all DIDs routes
	apiRoutes.Get("/dids", handlers.GetDIDs(didService))
	apiRoutes.Get("/dids/:did", handlers.GetDID(didService))
	apiRoutes.Post("/dids", handlers.CreateDID(didService))
	apiRoutes.Delete("/dids/:did", handlers.RevokeDid(didService))

	// all VC routes
	apiRoutes.Post("/dids/:did/vc", handlers.CreateVC(vcService, chain))
	apiRoutes.Get("/vc/:urn", handlers.GetVC(vcService))

	// serve static schema html files
	apiRoutes.Get("/docs/schema/:file", func(c *fiber.Ctx) error {
		file := c.Params("file")
		return c.SendFile("./docs/schema/html/" + file)
	})

	return app
}
