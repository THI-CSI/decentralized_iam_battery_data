package handlers

import (
	"blockchain/internal/api/web/server/models"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

// VerifyVp handles POST /api/v1/vps/verify
func (s *MyServer) VerifyVp(ctx echo.Context) error {
	var requestBody models.VerifyVpJSONRequestBody
	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVpVerifySchema); err != nil {
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	err := s.VPService.VerifyVP(ctx.Request().Context(), &requestBody)
	if err != nil {
		log.Printf("Error verifying the VP: %s", err)
		return ctx.JSON(http.StatusInternalServerError, models.ResponseErrorSchema{Message: err.Error()})
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VP verified"})
}
