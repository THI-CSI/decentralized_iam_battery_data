package handlers

import (
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

// GetAllBlocks handles GET /api/v1/blocks
func (s *MyServer) GetAllBlocks(ctx echo.Context) error {
	result, err := s.BlockService.GetBlocks(ctx.Request().Context())
	if err != nil {
		log.Printf("Bad Request: %v", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseBlocksSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}

// GetBlockById handles GET /api/v1/blocks/{blockId}
func (s *MyServer) GetBlockById(ctx echo.Context, blockId int) error {
	result, err := s.BlockService.GetBlock(ctx.Request().Context(), blockId)
	if err != nil {
		log.Printf("Bad Request: %v", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseBlockSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}
