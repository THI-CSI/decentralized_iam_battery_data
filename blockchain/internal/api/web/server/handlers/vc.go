package handlers

import (
	"blockchain/internal/api/web/server/models"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

// GetAllVCs handles GET /api/v1/vcs
func (s *MyServer) GetAllVCs(ctx echo.Context) error {
	result, err := s.VCService.GetVCRecords(ctx.Request().Context())
	if err != nil {
		log.Printf("Bad Request: %v", err)
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
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
		log.Printf("Bad Request: %v", err)
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseVcSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}

// CreateVcRecord handles POST /api/v1/vcs/create
func (s *MyServer) CreateVcRecord(ctx echo.Context) error {
	// TODO: implement once service logic is set
	return ctx.JSON(http.StatusCreated, map[string]string{"message": "VC created"})
}

// RevokeVcRecord handles POST /api/v1/vcs/revoke
func (s *MyServer) RevokeVcRecord(ctx echo.Context) error {
	// TODO: implement once service logic is set
	return ctx.JSON(http.StatusOK, map[string]string{"message": "VC revoked"})
}
