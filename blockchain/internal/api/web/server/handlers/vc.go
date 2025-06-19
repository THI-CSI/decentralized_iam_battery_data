package handlers

import (
	"blockchain/internal/api/web/server/models"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

// GetAllVcRecords handles GET /api/v1/vcs
func (s *MyServer) GetAllVcRecords(ctx echo.Context) error {
	result, err := s.VCService.GetVCRecords(ctx.Request().Context())
	if err != nil {
		log.Printf("Bad Request: %v", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseVcsSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}

// GetVcRecordById handles GET /api/v1/vcs/{vcUri}
func (s *MyServer) GetVcRecordById(ctx echo.Context, did string) error {
	result, err := s.VCService.GetVCRecord(ctx.Request().Context(), did)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseVcSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}

// CreateVcRecordCloud handles POST /api/v1/vcs/create/cloud
func (s *MyServer) CreateVcRecordCloud(ctx echo.Context) error {
	var requestBody models.CreateVcRecordCloudJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVcCreateSchemaCloudInstance); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err := s.VCService.CreateVCRecordCloud(ctx.Request().Context(), &requestBody)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VC created"})
}

// CreateVcRecordBms handles POST /api/v1/vcs/create/bms
func (s *MyServer) CreateVcRecordBms(ctx echo.Context) error {
	var requestBody models.CreateVcRecordBmsJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVcCreateSchemaBmsProduced); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err := s.VCService.CreateVCRecordBms(ctx.Request().Context(), &requestBody)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VC created"})
}

// CreateVcRecordServices handles POST /api/v1/vcs/create/services
func (s *MyServer) CreateVcRecordServices(ctx echo.Context) error {
	var requestBody models.CreateVcRecordServicesJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVcCreateSchemaServiceAccess); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err := s.VCService.CreateVCRecordServices(ctx.Request().Context(), &requestBody)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VC created"})
}

// RevokeVcRecord handles POST /api/v1/vcs/revoke
func (s *MyServer) RevokeVcRecord(ctx echo.Context) error {
	var requestBody models.RevokeVcRecordJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVcRevokeSchema); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err := s.VCService.VerifyRequestRevoke(requestBody)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err = s.VCService.RevokeVCRecord(ctx.Request().Context(), requestBody.Payload)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "VC revoked"})
}
