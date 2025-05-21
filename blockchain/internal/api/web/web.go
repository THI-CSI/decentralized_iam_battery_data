package web

import (
	"blockchain/internal/api/web/server"
	"blockchain/internal/core"
	"context"
	"fmt"
	"log"
	"os/signal"
	"syscall"
	"time"

	"github.com/gofiber/fiber/v2"
)

// gracefulShutdown listens for termination signals (SIGINT, SIGTERM), then gracefully shuts down the server.
func gracefulShutdown(app *fiber.App, done chan bool) {
	// Create context that listens for the interrupt signal from the OS.
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	// Listen for the interrupt signal.
	<-ctx.Done()

	log.Println("shutting down gracefully, press Ctrl+C again to force")

	// The context is used to inform the server it has 5 seconds to finish
	// the request it is currently handling
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := app.ShutdownWithContext(ctx); err != nil {
		log.Printf("Server forced to shutdown with error: %v", err)
	}

	log.Println("Server exiting")

	// Notify the main goroutine that the shutdown is complete
	done <- true
}

// CreateServer initializes the Fiber server, starts it, and ensures graceful shutdown handling.
// The server runs in a goroutine to allow for concurrent shutdown handling via `gracefulShutdown`.
//
//	@title			Blockchain API
//	@version		1.0
//	@description	This is the api for the blockchain
//
//	@host		localhost:8080
//	@BasePath	/api/v1
func CreateServer(chain *core.Blockchain) {
	app := server.New(chain)

	config := server.NewConfiguration()

	// Create a done channel to signal when the shutdown is complete
	done := make(chan bool, 1)

	go func() {
		err := app.Listen(fmt.Sprintf(":%s", config.Port))
		if err != nil {
			panic(fmt.Sprintf("http server error: %s", err))
		}
	}()

	// Run graceful shutdown in a separate goroutine
	go gracefulShutdown(app, done)

	// Wait for the graceful shutdown to complete
	<-done
	log.Println("Graceful shutdown complete.")
}
