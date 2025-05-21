package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"log/slog"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

// GetTransactions returns all transactions of a block
//
//	@Summary		Get all transactions of a block
//	@Description	Get all transactions of a block
//	@Tags			Blocks
//	@Accept			json
//	@Produce		json
//	@Param			blockId	path		int	true	"Block ID"
//	@Success		200		{object} 	domain.TransactionResponse
//	@Failure		400		{object}	domain.ErrorResponseHTTP
//	@Failure		500		{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/blocks/{blockId}/transactions [get]
func GetTransactions(service services.TransactionService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		blockId, err := strconv.Atoi(c.Params("blockId"))
		if err != nil {
			return domain.BadRequestError("BlockId must a number")
		}
		slog.Info("GetTransactions was called", blockId)

		result, err := service.GetTransactions(c.UserContext(), blockId)
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}
