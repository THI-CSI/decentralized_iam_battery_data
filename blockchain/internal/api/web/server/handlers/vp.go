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

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVpVerifySchema); err != nil {
		return err
	}
	if err := s.VCService.VerifyRequestCreate(&requestBody.VerifiableCredential); err != nil {
		return err
	}
	err := s.VPService.VerifyVP(ctx.Request().Context(), &requestBody)
	if err != nil {
		log.Printf("Error verifying the VP: %s", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VP verified"})
}
