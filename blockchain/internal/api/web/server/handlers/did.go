package handlers

import (
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	"log/slog"

	"github.com/gofiber/fiber/v2"
)

// GetDIDs retrieves all DIDs from the blockchain
//
// @Summary Get all DIDs
// @Description Get all DIDs from the blockchain
// @Tags Did
// @Accept json
// @Produce json
// @Success 200 {object} []domain.Did
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/dids [get]
func GetDIDs(service services.DidService, chain *core.Blockchain) fiber.Handler {
	return func(c *fiber.Ctx) error {
		slog.Info("GetDIDs was called", "info")

		result, err := service.GetDIDs(c.UserContext(), chain)
		if err != nil {
			return err
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}
