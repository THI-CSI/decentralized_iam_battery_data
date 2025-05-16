package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"github.com/gofiber/fiber/v2"
	"log/slog"
)

// GetVC retrieves a VC from the blockchain
//
// @Summary Get a VC Record
// @Description Get a VC Record from the blockchain
// @Tags VCs
// @Accept json
// @Produce json
// @Param urn path string true "VC Record URN"
// @Success 200 {object} core.VCRecord
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/vc/{urn} [get]
func GetVC(service services.VCService, chain *core.Blockchain) fiber.Handler {
	return func(c *fiber.Ctx) error {
		urn := c.Params("urn")
		if !utils.IsUrnValid(urn) {
			return domain.BadRequestError("Invalid URN")
		}

		slog.Info("GetVC was called", urn)

		result, err := service.GetVCRecord(c.UserContext(), chain, urn)
		if err != nil {
			return fiber.NewError(fiber.StatusNotFound, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}

// CreateVC creates a VC on the blockchain
//
// @Summary Create a new VC
// @Description Create a new VC on the blockchain
// @Tags VCs
// @Accept json
// @Produce json
// @Param did path string true "DID"
// @Param recipe body core.Vc true "VC"
// @Success 201 {object} core.VCRecord
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/dids/{did}/vc [post]
func CreateVC(service services.VCService, chain *core.Blockchain) fiber.Handler {
	return func(c *fiber.Ctx) error {

		did := c.Params("did")
		didState := chain.VerifyDID(did)
		// TODO: Should be able to add VC if DID is pending
		if didState != core.DidValid {
			slog.Warn("Invalid DID: %v=%v\n", did, didState)
			return domain.BadRequestError("DID does not exist or is revoked")
		}

		vc, err := coreTypes.UnmarshalVc(c.BodyRaw())
		if err != nil {
			slog.Warn("Invalid Verifiable Credential: %v\n", err)
			return domain.BadRequestError("Invalid Verifiable Credential")
		}

		if vc.Issuer != did {
			slog.Warn("The Issuer of the VC is different to the specified DID: %v!=%v\n", vc.Issuer, did)
			return domain.BadRequestError("Invalid Verifiable Credential")
		}

		slog.Info("CreateVC was called", vc)
		result, err := service.CreateVCRecord(c.UserContext(), chain, &vc)
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusCreated, result)
	}
}
