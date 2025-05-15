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
// @Summary Get a single DID
// @Description Get a DID from the blockchain
// @Tags VC
// @Accept json
// @Produce json
// @Success 200 {object} core.VCRecord
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/dids/{did}/vc/{urn} [get]
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
// @Tags VC
// @Accept json
// @Produce json
// @Success 201 {object} core.VCRecord
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/dids/{did}/vc [post]
func CreateVC(service services.VCService, chain *core.Blockchain) fiber.Handler {
	return func(c *fiber.Ctx) error {

		// TODO: Proof can not be an object (with type, created, verificationMethod, proofPurpose and jws) but just a string!
		vc, err := utils.ParseAndValidateStruct[coreTypes.Vc](c)
		if err != nil {
			slog.Warn("Invalid Verifiable Credential: %v\n", err)
			return domain.BadRequestError("Invalid Verifiable Credential")
		}

		slog.Info("CreateVC was called", vc)
		result, err := service.CreateVCRecord(c.UserContext(), chain, vc)
		if err != nil {
			return err
		}

		return utils.WriteResponse(c, fiber.StatusCreated, result)
	}
}
