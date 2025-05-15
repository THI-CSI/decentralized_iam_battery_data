package handlers

import (
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	"log/slog"

	"github.com/gofiber/fiber/v2"
)

// GetBlocks handles the creation of a new Decentralized Identifier (DID).
// It accepts a public key in the request body and returns a newly created DID.
//
// @Summary Get all blocks
// @Description Get all blocks of the blockchain
// @Tags Blocks
// @Accept json
// @Produce json
// @Success 200 {object} domain.Did
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/blocks [get]
func GetBlocks(service services.BlockService, chain *core.Blockchain) fiber.Handler {
	return func(c *fiber.Ctx) error {

		slog.Info("GetBlocks was called", "info")

		result, err := service.GetBlocks(c.UserContext(), chain)
		if err != nil {
			return err
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}
