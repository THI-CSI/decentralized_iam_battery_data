package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"log/slog"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

// GetBlocks returns all blocks of the blockchain
//
//	@Summary		Get all blocks
//	@Description	Get all blocks of the blockchain
//	@Tags			Blocks
//	@Accept			json
//	@Produce		json
//	@Success		200	{object}	domain.BlockchainResponse
//	@Failure		400	{object}	domain.ErrorResponseHTTP
//	@Failure		500	{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/blocks [get]
func GetBlocks(service services.BlockService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		slog.Info("GetBlocks was called")

		result, err := service.GetBlocks(c.UserContext())
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}

// GetBlock returns a single block of the blockchain specified by the id
//
//	@Summary		Get a block by id
//	@Description	Get a block of the blockchain by id
//	@Tags			Blocks
//	@Accept			json
//	@Produce		json
//	@Param			blockId	path		int	true	"Block ID"
//	@Success		200		{object}	domain.BlockResponse
//	@Failure		400		{object}	domain.ErrorResponseHTTP
//	@Failure		500		{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/blocks/{blockId} [get]
func GetBlock(service services.BlockService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		blockId, err := strconv.Atoi(c.Params("blockId"))
		if err != nil {
			return domain.BadRequestError("BlockId must be a number")
		}
		slog.Info("GetBlock was called", blockId)

		result, err := service.GetBlock(c.UserContext(), blockId)
		if err != nil {
			return domain.NotFoundError(err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}
