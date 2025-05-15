package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	"log/slog"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

// GetTransactions returns all transactions of a block
//
// @Summary Get all transactions of a block
// @Description Get all transactions of a block
// @Tags Blocks
// @Accept json
// @Produce json
// @Success 200 {object} domain.BlockResponse
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/blocks/{blockId}/transactions [get]
func GetTransactions(service services.TransactionService, chain *core.Blockchain) fiber.Handler {
	return func(c *fiber.Ctx) error {
		blockId, err := strconv.Atoi(c.Params("blockId"))
		if err != nil {
			return domain.BadRequestError("BlockId must a number")
		}
		slog.Info("GetTransactions was called", "info", blockId)

		result, err := service.GetTransactions(c.UserContext(), chain, blockId)
		if err != nil {
			return err
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}
