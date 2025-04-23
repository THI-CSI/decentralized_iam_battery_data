package server

import "os"

// Configuration holds application-level configuration values.
// Currently, it only includes the HTTP server port, but can be extended as needed.
type Configuration struct {
	// Port defines the port the server should listen on.
	Port string
}

// NewConfiguration initializes a new Configuration instance.
// It reads values from environment variables, with fallback defaults.
func NewConfiguration() *Configuration {
	return &Configuration{
		Port: getEnvOrDefault("PORT", "8080"),
	}
}

// getEnvOrDefault reads an environment variable and returns its value.
// If the variable is not set, it returns the provided default value.
func getEnvOrDefault(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}
