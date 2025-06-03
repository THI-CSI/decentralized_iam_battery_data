package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	"github.com/gofiber/fiber/v2"
	"github.com/labstack/echo/v4"
	"log/slog"
	"net/http"
)

// GetVC retrieves a VC from the blockchain
//
//	@Summary		Get a VC Record
//	@Description	Get a VC Record from the blockchain
//	@Tags			VCs
//	@Accept			json
//	@Produce		json
//	@Param			urn	path		string	true	"VC Record URN"
//	@Success		200	{object}	core.VCRecord
//	@Failure		400	{object}	domain.ErrorResponseHTTP
//	@Failure		500	{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/vc/{urn} [get]
func GetVC(service services.VCService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		urn := c.Params("urn")
		if !utils.IsUrnValid(urn) {
			return domain.BadRequestError("Invalid URN")
		}

		slog.Info("GetVC was called", urn)

		result, err := service.GetVCRecord(c.UserContext(), urn)
		if err != nil {
			return fiber.NewError(fiber.StatusNotFound, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}

// CreateVC creates a VC on the blockchain
//
//	@Summary		Create a new VC
//	@Description	Create a new VC on the blockchain
//	@Tags			VCs
//	@Accept			json
//	@Produce		json
//	@Param			did		path		string	true	"DID"
//	@Param			vc body		domain.VCRequest true "VC"
//	@Success		201		{object}	core.VCRecord
//	@Failure		400		{object}	domain.ErrorResponseHTTP
//	@Failure		500		{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/dids/{did}/vc [post]
func CreateVC(service services.VCService, chain *core.Blockchain) fiber.Handler {
	return func(c *fiber.Ctx) error {

		did := c.Params("did")
		didState := chain.VerifyDID(did)
		// TODO: Should be able to add VC if DID is pending
		if didState != core.DidValid {
			slog.Warn("Invalid DID: %v=%v\n", did, didState)
			return domain.BadRequestError("DID does not exist or is revoked")
		}

		vc, err := utils.ParseAndValidateStruct[domain.VCRequest](c)
		if err != nil {
			slog.Warn("Invalid Verifiable Credential: %v\n", err)
			return domain.BadRequestError("Invalid Verifiable Credential")
		}

		slog.Info("CreateVC was called", vc)
		result, err := service.CreateVCRecord(c.UserContext(), vc)
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusCreated, result)
	}
}

// CreateVcRecord handles POST /api/v1/vc/create
func (s *Server) CreateVcRecord(ctx echo.Context) error {
	// TODO: parse and create VC
	return ctx.JSON(http.StatusCreated, map[string]string{"message": "VC created"})
}

// RevokeVcRecord handles POST /api/v1/vc/revoke
func (s *Server) RevokeVcRecord(ctx echo.Context) error {
	// TODO: parse and revoke VC
	return ctx.JSON(http.StatusOK, map[string]string{"message": "VC revoked"})
}

// VerifyVcRecord handles POST /api/v1/vc/verify
func (s *Server) VerifyVcRecord(ctx echo.Context) error {
	// TODO: parse and verify VC
	return ctx.JSON(http.StatusOK, map[string]bool{"valid": true})
}
