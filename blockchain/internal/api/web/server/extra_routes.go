package server

import (
	"github.com/labstack/echo/v4"
	"net/http"
	"path/filepath"
)

// RegisterExtraRoutes registers routes that are not part of the OpenAPI spec
// but provide additional functionality like status checks, Swagger UI, or static files.
func RegisterExtraRoutes(e *echo.Echo) {
	// Status route
	e.GET("/api/v1/status", func(c echo.Context) error {
		return c.String(http.StatusOK, "ok")
	})

	// Swagger documentation route
	// You need to ensure 'blockchain/docs/swagger' is correctly generating
	// the swagger.json/swagger.yaml files in your build process.
	e.GET("/swagger", func(c echo.Context) error {
		filePath := filepath.Clean("./docs/openapi.html") // Safer path joining
		return c.File(filePath)
	})

	// Serve static schema html files
	// Adjust the path "./docs/schema/html/" to your actual static files directory
	e.GET("/docs/schema/:file", func(c echo.Context) error {
		fileName := c.Param("file")
		filePath := filepath.Join("./docs/schema/html/", fileName) // Safer path joining
		return c.File(filePath)
	})

	// OPTIONAL: If you want to serve the entire docs/schema/html directory as static assets
	// e.Static("/docs/schema", "docs/schema/html")
}
