package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"log/slog"

	"github.com/gofiber/fiber/v2"
)

// CreateDid handles the creation of a new Decentralized Identifier (DID).
// It accepts a public key in the request body and returns a newly created DID.
//
// @Summary Create a DID
// @Description Create a DID with a public key
// @Tags Did
// @Accept json
// @Produce json
// @Param did body domain.CreateDid true "DID Request"
// @Success 201 {object} domain.Did
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/did [post]
func CreateDid(service services.DidService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		createDto, err := utils.ParseAndValidateStruct[domain.CreateDid](c)
		if err != nil {
			return err
		}

		slog.Info("CreateDid was called", "info", createDto)

		result, err := service.CreateDid(c.UserContext(), createDto)
		if err != nil {
			return err
		}

		return utils.WriteResponse(c, fiber.StatusCreated, result)
	}
}

// GrantAccessRight grants specific access rights to a DID.
// It receives the target DID and role from the request body.
//
// @Summary Grant access rights
// @Description Grant access rights to another DID
// @Tags Did
// @Accept json
// @Produce json
// @Param did body domain.GrantAccessRights true "Grant Access Request"
// @Success 200
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/grant [put]
func GrantAccessRight(service services.DidService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		grantDto, err := utils.ParseAndValidateStruct[domain.GrantAccessRights](c)
		if err != nil {
			return err
		}

		slog.Info("GrantAccessRight was called", "info", grantDto)

		if err := service.GrantAccessRight(c.UserContext(), grantDto); err != nil {
			return err
		}

		return c.SendStatus(fiber.StatusOK)
	}
}

// GetAccessRightsForDid retrieves all access rights associated with a given DID.
//
// @Summary Get access rights for DID
// @Description Get all access rights for a specified DID
// @Tags Did
// @Accept json
// @Produce json
// @Param did path string true "DID Identifier"
// @Success 200 {object} domain.AccessRightsResponse
// @Failure 400 {object} domain.ErrorResponseHTTP
// @Failure 500 {object} domain.ErrorResponseHTTP
// @Router /api/v1/grants/{did} [get]
func GetAccessRightsForDid(service services.DidService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		didId := c.Params("did")
		if didId == "" {
			return fiber.NewError(fiber.StatusBadRequest, "Did params not found")
		}

		slog.Info("GetAccessRightsForDid was called", "info", didId)

		result, err := service.GetAccessRightsForDid(c.UserContext(), didId)
		if err != nil {
			return err
		}

		return utils.WriteResponse(c, fiber.StatusOK, domain.AccessRightsResponse{AccessRights: result})
	}
}
