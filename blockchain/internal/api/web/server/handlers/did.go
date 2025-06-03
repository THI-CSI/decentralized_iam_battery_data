package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"github.com/gofiber/fiber/v2"
	"github.com/labstack/echo/v4"
	"log/slog"
	"net/http"
	"net/url"
)

// GetDIDs retrieves all DIDs from the blockchain
//
//	@Summary		Get all DIDs
//	@Description	Get all DIDs from the blockchain
//	@Tags			DIDs
//	@Accept			json
//	@Produce		json
//	@Success		200	{object}	[]core.Did
//	@Failure		400	{object}	domain.ErrorResponseHTTP
//	@Failure		500	{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/dids [get]
func GetDIDs(service services.DidService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		slog.Info("GetDIDs was called", "info")
		result, err := service.GetDIDs(c.UserContext())
		if err != nil {
			return err
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}

// GetAllDids handles GET /api/v1/dids
func (s *Server) GetAllDids(ctx echo.Context) error {
	// TODO: return all DIDs
	return ctx.JSON(http.StatusOK, []string{})
}

// GetDID retrieves a DID from the blockchain
//
//	@Summary		Get a single DID
//	@Description	Get a DID from the blockchain
//	@Tags			DIDs
//	@Accept			json
//	@Produce		json
//	@Param			did	path		string	true	"DID"
//	@Success		200	{object}	core.Did
//	@Failure		400	{object}	domain.ErrorResponseHTTP
//	@Failure		500	{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/dids/{did} [get]
func GetDID(service services.DidService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		did := c.Params("did")
		did, err := url.QueryUnescape(did)
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, err.Error())
		}
		if !utils.IsDidValid(did) {
			return domain.BadRequestError("Invalid Did")
		}

		slog.Info("GetDID was called", did)

		result, err := service.GetDID(c.UserContext(), did)
		if err != nil {
			return fiber.NewError(fiber.StatusNotFound, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusOK, result)
	}
}

// GetDidById handles GET /api/v1/dids/{did}
func (s *Server) GetDidById(ctx echo.Context, did string) error {
	// TODO: fetch DID by ID
	return ctx.JSON(http.StatusOK, map[string]string{"did": did})
}

// CreateDID creates a DID on the blockchain
//
//	@Summary		Create a new DID
//	@Description	Create a new DID on the blockchain
//	@Tags			DIDs
//	@Accept			json
//	@Produce		json
//	@Param			did body		domain.CreateDid	true	"DID"
//	@Success		201		{object}	core.Did
//	@Failure		400		{object}	domain.ErrorResponseHTTP
//	@Failure		500		{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/dids [post]
func CreateDID(service services.DidService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		createDid, err := utils.ParseAndValidateStruct[domain.CreateDid](c)
		if err != nil {
			return domain.BadRequestError("Invalid Did")
		}

		slog.Info("CreateDID was called", createDid)

		result, err := service.CreateDID(c.UserContext(), createDid)
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, err.Error())
		}

		return utils.WriteResponse(c, fiber.StatusCreated, result)
	}
}

// CreateOrModifyDid handles POST /api/v1/dids/createormodify
func (s *Server) CreateOrModifyDid(ctx echo.Context) error {
	// TODO: parse input and create/modify DID
	return ctx.JSON(http.StatusCreated, map[string]string{"message": "DID created or modified"})
}

// RevokeDid revokes a DID on the blockchain and creates a new transaction
//
//	@Summary		Revokes a DID
//	@Description	Revokes a DID on the blockchain and creates a new transaction
//	@Tags			DIDs
//	@Accept			json
//	@Produce		json
//	@Param			did	path	string	true	"DID"
//	@Success		200
//	@Failure		400	{object}	domain.ErrorResponseHTTP
//	@Failure		500	{object}	domain.ErrorResponseHTTP
//	@Router			/api/v1/dids/{did} [delete]
func RevokeDid(service services.DidService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		did := c.Params("did")
		did, err := url.QueryUnescape(did)
		if err != nil {
			return fiber.NewError(fiber.StatusBadRequest, err.Error())
		}
		if !utils.IsDidValid(did) {
			return domain.BadRequestError("Invalid Did")
		}

		slog.Info("RevokeDid was called", did)

		if err := service.RevokeDid(c.UserContext(), did); err != nil {
			return err
		}

		return c.SendStatus(fiber.StatusOK)
	}
}

// RevokeDid handles POST /api/v1/dids/revoke
func (s *Server) RevokeDid(ctx echo.Context) error {
	// TODO: parse input and revoke DID
	return ctx.JSON(http.StatusOK, map[string]string{"message": "DID revoked"})
}
