# File: Makefile

.PHONY: all build clean docs run test

# Variables
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
SCHEMA_DIR="./internal/jsonschema"
QUICKTYPE="./node_modules/.bin/quicktype"
SCHEMA_RESOLVER='./node_modules/.bin/json-schema-resolver'
DOCS="./docs"
TYPES="./internal/core/types.go"

# Activate venv
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

# Install dependencies
install: $(VENV)/bin/activate
	# Go installs
	go install github.com/swaggo/swag/cmd/swag@latest
	go install github.com/princjef/gomarkdoc/cmd/gomarkdoc@latest
	# NPM installs
	npm install --save-dev quicktype	# flag makes sure its in the projects devDependencies not dependencies
	npm install --save-dev json-schema-resolver
	# PIP installs
	$(PIP) install json-schema-for-humans


# Build your Go binary
build:
	go build -o bin/blockchain ./cmd/main.go

# Format sourcecode
format:
	gofmt -l -s -w .

# Run the app (example)
run: format docs
	go run cmd/main.go --web

# Generate ALL docs
docs: docs-go docs-did-vc docs-swagger

# Generate Go code documentation
docs-go:
	echo "Generating go docs..."
	mkdir -p $(DOCS)
	./scripts/generate-docs.sh

# Process/copy Swagger documentation
docs-swagger:
	echo "Generating swagger docs ..."
	mkdir -p $(DOCS)/swagger/
	swag init -g ./cmd/main.go -o $(DOCS)/swagger/

# Generate DID and VC documentation
docs-did-vc:
	@echo "Generating DID and VC docs ..."
	@mkdir -p $(DOCS)
	@for file in $(SCHEMA_DIR)/*.json; do \
      		echo "Generating docs for: $$file"; \
    		$(VENV)/bin/generate-schema-doc $$file --config template_name=md; \
    		mv schema_doc.md $(DOCS)/$$(basename $$file .json).md; \
    done

# Clean build artifacts and generated docs
clean:
	rm -rf bin
	rm -rf docs
	rm -rf .venv
	rm -rf node_modules

test:
	go test -v ./internal/core

# Generate go types from jsonschemas
# to seperate packages from each other one needs to seperate the sourcefiles of these with directories and run the command once per directory
generate:
	@echo "Generating Go structs using quicktype..."

	$(QUICKTYPE) --lang go \
		--top-level DID \
		--package "core" \
		--src $(SCHEMA_DIR) \
		--out $(TYPES)

# Do everything: clean + install + generate + test + build + (format, docs) run
all: clean install generate test build run

