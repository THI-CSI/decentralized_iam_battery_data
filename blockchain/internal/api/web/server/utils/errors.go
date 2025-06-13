package utils

import (
	"fmt"
	"github.com/labstack/echo/v4"
	"net/http"
	"runtime"
	"strings"
)

// Location Helper to get file and line where the error originated
func Location(depth int) string {
	_, file, line, ok := runtime.Caller(depth)
	if !ok {
		return "unknown"
	}
	parts := strings.Split(file, "/")
	file = parts[len(parts)-1] // just filename
	return fmt.Sprintf("%s:%d", file, line)
}

// CustomErrorHandler Custom error handler
func CustomErrorHandler(err error, c echo.Context) {
	code := http.StatusInternalServerError
	var msg string

	if he, ok := err.(*echo.HTTPError); ok {
		code = he.Code
		msg = fmt.Sprintf("%v", he.Message)
	} else {
		msg = err.Error()
	}

	logLocation := Location(5)
	c.Logger().Errorf("[%s] %s (code=%d)", logLocation, msg, code)

	if !c.Response().Committed {
		if code < 500 {
			c.JSON(code, echo.Map{"error": msg})
		} else {
			c.JSON(code, echo.Map{"error": http.StatusText(code)})
		}
	}
}
