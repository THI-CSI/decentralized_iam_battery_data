package handlers

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/utils"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

// VerifyVpCloud handles POST /api/v1/vps/verify/cloud
func (s *MyServer) VerifyVpCloud(ctx echo.Context) error {
	var requestBody models.VerifyVpCloudJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	// Check input against jsonschema
	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVpVerifySchemaCloud); err != nil {
		return err
	}
	// Check VP signature and VC Hash and verify that dids in VC and VP match
	if err := s.VPService.VerifyVPForCloud(ctx.Request().Context(), &requestBody); err != nil {
		log.Printf("Error verifying the VP: %s", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	// Check VC signature
	if err := utils.VerifyRequestCreateCloud(&requestBody.VerifiableCredential[0]); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	// DID states are checked during signature confirmations
	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VP verified"})
}

// VerifyVpBms handles POST /api/v1/vps/verify/bms
func (s *MyServer) VerifyVpBms(ctx echo.Context) error {
	var requestBody models.VerifyVpBmsJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	// Check input against jsonschema
	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVpVerifySchemaBms); err != nil {
		return err
	}
	// Check VP signature and VC Hash and verify that dids in VC and VP match
	if err := s.VPService.VerifyVPForBms(ctx.Request().Context(), &requestBody); err != nil {
		log.Printf("Error verifying the VP: %s", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	// Check VC signature
	if err := utils.VerifyRequestCreateBms(&requestBody.VerifiableCredential[0]); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	// DID states are checked during signature confirmations
	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VP verified"})
}

// VerifyVpServices handles POST /api/v1/vps/verify/services
func (s *MyServer) VerifyVpServices(ctx echo.Context) error {
	var requestBody models.VerifyVpServicesJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	// Check input against jsonschema
	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVpVerifySchemaServices); err != nil {
		return err
	}
	// Check VP signature and VC Hash and verify that dids in VC and VP match
	if err := s.VPService.VerifyVPForServices(ctx.Request().Context(), &requestBody); err != nil {
		log.Printf("Error verifying the VP: %s", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	// Check VC signature
	if err := utils.VerifyRequestCreateServices(&requestBody.VerifiableCredential[0]); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	// DID states are checked during signature confirmations
	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VP verified"})
}
