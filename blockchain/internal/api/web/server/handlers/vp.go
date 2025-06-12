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

	// Check input against jsonschema
	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVpVerifySchema); err != nil {
		return err
	}
	// Check VP signature and VC Hash and verify that dids in VC and VP match
	if err := s.VPService.VerifyVP(ctx.Request().Context(), &requestBody); err != nil {
		log.Printf("Error verifying the VP: %s", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	// Check VC signature
	if err := s.VCService.VerifyRequestCreate(&requestBody.VerifiableCredential[0]); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	// DID states are checked during signature confirmations

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VP verified"})
}
