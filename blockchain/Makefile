# File: Makefile

.PHONY: all build clean docs run test

# Install dependencies
install:
	go install github.com/swaggo/swag/cmd/swag@latest
	go install github.com/princjef/gomarkdoc/cmd/gomarkdoc@latest

# Build your Go binary
build:
	go build -o bin/blockchain ./cmd/main.go

# Format sourcecode
format:
	gofmt -l -s -w .

# Run the app (example)
run: format
	go run cmd/main.go

# Generate ALL docs
docs: docs-go docs-swagger

# Generate Go code documentation
docs-go:
	echo "Generating go docs..."
	./generate-docs.sh

# Process/copy Swagger documentation
docs-swagger:
	echo "Generating swagger docs ..."
	swag init -g cmd/main.go -o internal/api/web/docs

# Clean build artifacts and generated docs
clean:
	rm -rf bin
	rm -f DOCS.md
	rm -rf internal/cmd/api/web/docs

# Do everything: build + docs + test
all: clean test build docs

