package handlers

import (
	"blockchain/internal/api/web/server/models"
	"bytes"
	"github.com/labstack/echo/v4"
	"io"
	"log"
	"net/http"
)

// GetAllDids handles GET /api/v1/dids
func (s *MyServer) GetAllDids(ctx echo.Context) error {
	result, err := s.DidService.GetDIDs(ctx.Request().Context())
	if err != nil {
		log.Printf("Bad Request: %v", err)
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
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
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	if err := s.validateOutgoingResponse(ctx, *result, s.responseDidSchema); err != nil {
		return err
	}

	return ctx.JSON(http.StatusOK, result)
}

// CreateOrModifyDid handles POST /api/v1/dids/createormodify
func (s *MyServer) CreateOrModifyDid(ctx echo.Context) error {
	rawBody, err := io.ReadAll(ctx.Request().Body)
	ctx.Request().Body = io.NopCloser(bytes.NewBuffer(rawBody))
	if err != nil {
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: "Failed to read the raw request body"})
	}
	ctx.Request().Body = io.NopCloser(bytes.NewBuffer(rawBody))

	var requestBody models.CreateOrModifyDidJSONRequestBody
	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestDidCreateormodifySchema); err != nil {
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	err = s.verifyProof(rawBody, requestBody, requestBody.Proof.Jws, requestBody.Payload.VerificationMethod.Controller)
	if err != nil {
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	err = s.DidService.CreateOrModifyDID(ctx.Request().Context(), &requestBody.Payload)
	if err != nil {
		log.Printf("Error creating or modifying DID: %s", err)
		return ctx.JSON(http.StatusInternalServerError, models.ResponseErrorSchema{Message: err.Error()})
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "DID created"})
}

// RevokeDid handles POST /api/v1/dids/revoke
func (s *MyServer) RevokeDid(ctx echo.Context) error {
	rawBody, err := io.ReadAll(ctx.Request().Body)
	ctx.Request().Body = io.NopCloser(bytes.NewBuffer(rawBody))
	if err != nil {
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: "Failed to read the raw request body"})
	}
	ctx.Request().Body = io.NopCloser(bytes.NewBuffer(rawBody))

	var requestBody models.RevokeDidJSONRequestBody
	if err := s.validateIncomingRequest(ctx, &requestBody, s.requestDidCreateormodifySchema); err != nil {
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	err = s.verifyProof(rawBody, requestBody, requestBody.Proof.Jws, requestBody.Payload)
	if err != nil {
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})
	}

	err = s.DidService.RevokeDid(ctx.Request().Context(), requestBody.Payload)
	if err != nil {
		log.Printf("Error revoking DID: %s", err)
		return ctx.JSON(http.StatusInternalServerError, models.ResponseErrorSchema{Message: err.Error()})
	}

	return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "DID revoked"})
}
