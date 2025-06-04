package handlers

import (
	"blockchain/internal/api/web/server/models"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

func (s *MyServer) GetBlockTransactions(ctx echo.Context, blockID int) error {
	result, err := s.TransactionService.GetTransactions(ctx.Request().Context(), blockID)
	if err != nil {
		log.Printf("Bad Request: %v", err)
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseTransactionsSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}
