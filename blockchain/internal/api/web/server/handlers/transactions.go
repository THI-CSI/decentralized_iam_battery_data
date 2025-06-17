package handlers

import (
	"github.com/labstack/echo/v4"
	"net/http"
)

func (s *MyServer) GetBlockTransactions(ctx echo.Context, blockID int) error {
	result, err := s.TransactionService.GetTransactions(ctx.Request().Context(), blockID)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseTransactionsSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}
