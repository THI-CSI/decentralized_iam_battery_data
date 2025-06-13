package handlers

import (
	"blockchain/internal/api/web/server/models"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
)

// GetAllDids handles GET /api/v1/dids
func (s *MyServer) GetAllDids(ctx echo.Context) error {
	result, err := s.DidService.GetDIDs(ctx.Request().Context())

	if err != nil {
		log.Printf("Bad Request: %v", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseDidsSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}

// GetDidById handles GET /api/v1/dids/{did}
func (s *MyServer) GetDidById(ctx echo.Context, did string) error {
	result, err := s.DidService.GetDID(ctx.Request().Context(), did)
	if err != nil {
		log.Printf("Bad Request: %v", err)
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseDidSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}

// CreateOrModifyDid handles POST /api/v1/dids/createormodify
func (s *MyServer) CreateOrModifyDid(ctx echo.Context) error {
	var requestBody models.CreateOrModifyDidJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestDidCreateormodifySchema); err != nil {
		return err
	}

	err := s.DidService.VerifyRequestCreateOrModify(requestBody)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	err = s.DidService.CreateOrModifyDID(ctx.Request().Context(), &requestBody.Payload)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, models.ResponseErrorSchema{Message: err.Error()})
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "DID created/modified"})
}

// RevokeDid handles POST /api/v1/dids/revoke
func (s *MyServer) RevokeDid(ctx echo.Context) error {
	var requestBody models.RevokeDidJSONRequestBody

	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestDidRevokeSchema); err != nil {
		return err
	}

	err := s.DidService.VerifyRequestRevoke(requestBody)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err = s.DidService.RevokeDid(ctx.Request().Context(), requestBody.Payload)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "DID revoked"})
}
