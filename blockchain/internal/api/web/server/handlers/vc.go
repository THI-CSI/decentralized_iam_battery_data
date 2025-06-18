package handlers

import (
	"blockchain/internal/api/web/server/models"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

// GetAllVCs handles GET /api/v1/vcs
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

// GetVcById handles GET /api/v1/vcs/{vcUri}
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

// CreateVcRecord handles POST /api/v1/vcs/create
func (s *MyServer) CreateVcRecordForCloud(ctx echo.Context) error {
	var requestBody models.CreateVcRecordCloudJSONRequestBody

	log.Println("inside create vc record")

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestVcCreateSchemaCloudInstance); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	log.Println("verify request create")
	err := s.VCService.VerifyRequestCreate(&requestBody)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	log.Println("create vc record")
	err = s.VCService.CreateVCRecord(ctx.Request().Context(), &requestBody)
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
