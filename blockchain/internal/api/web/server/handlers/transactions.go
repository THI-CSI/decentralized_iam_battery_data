package handlers

import (
	"blockchain/internal/api/web/server/models"
	"github.com/labstack/echo/v4"
	"net/http"
)

func (s *MyServer) GetBlockTransactions(ctx echo.Context, blockID int) error {
	result, err := s.TransactionService.GetTransactions(ctx.Request().Context(), blockID)
	if err != nil {
		// You might want to distinguish between 400 and 500 errors based on the 'err' value
		// For simplicity, here we're returning 400 for any service error.
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	return ctx.JSON(http.StatusOK, result)
}
