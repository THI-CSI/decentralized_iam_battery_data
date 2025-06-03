package handlers

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/services"
	"blockchain/internal/api/web/server/utils"
	"fmt"
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
func (s *MyServer) GetAllDids(ctx echo.Context) error {
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
func (s *MyServer) GetDidById(ctx echo.Context, did string) error {
	unescapedDid, err := url.QueryUnescape(did)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, fmt.Sprintf("Invalid DID format: %s", err.Error()))
	}

	if !utils.IsDidValid(unescapedDid) {
		return echo.NewHTTPError(http.StatusBadRequest, domain.BadRequestError("Invalid DID").Error())
	}

	slog.Info("GetDidById was called", "did", unescapedDid)

	result, err := s.DidService.GetDID(ctx.Request().Context(), unescapedDid)
	if err != nil {
		return echo.NewHTTPError(http.StatusNotFound, err.Error())
	}

	return ctx.JSON(http.StatusOK, result)
}

// CreateOrModifyDid handles POST /api/v1/dids/createormodify
func (s *MyServer) CreateOrModifyDid(ctx echo.Context) error {
	var requestBody models.CreateOrModifyDidJSONRequestBody

	// Use c.Bind() to unmarshal the request body into the struct.
	// Echo automatically handles different content models (like JSON, XML, form data)
	// based on the Content-Type header. For JSON, it uses encoding/json internally.
	if err := ctx.Bind(&requestBody); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, fmt.Sprintf("Failed to decode request: %v", err))
	}

	// Now you have the unmarshaled data in requestBody
	fmt.Printf("Received DID Payload ID: %s\n", requestBody.Payload.Id)
	fmt.Printf("Received Proof Created Time: %s\n", requestBody.Proof.Created)
	fmt.Printf("Received Proof JWS: %s\n", requestBody.Proof.Jws)

	// You can then process the data
	// ...

	return ctx.JSON(http.StatusOK, map[string]string{"message": "DID created or modified successfully"})
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
func (s *MyServer) RevokeDid(ctx echo.Context) error {
	// TODO: parse input and revoke DID
	return ctx.JSON(http.StatusOK, map[string]string{"message": "DID revoked"})
}
