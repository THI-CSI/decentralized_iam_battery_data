# File: Makefile

.PHONY: all build clean docs run test

# Variables
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
SCHEMA_DIR="./internal/jsonschema"
OUTPUT_FILE="./internal/core/data.go"
QUICKTYPE="./node_modules/.bin/quicktype"
SCHEMA_RESOLVER='./node_modules/.bin/json-schema-resolver'
DOCS="./docs"

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
run: format
	go run cmd/main.go

# Generate ALL docs
docs: docs-go docs-did-vc docs-swagger

# Generate Go code documentation
docs-go:
	echo "Generating go docs..."
	mkdir -p $(DOCS)
	./generate-docs.sh

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
        $(SCHEMA_RESOLVER) $$file > resolved.json; \
		$(VENV)/bin/generate-schema-doc resolved.json --config template_name=md; \
		rm resolved.json; \
		mv schema_doc.md $(DOCS)/$$(basename $$file .json).md; \
	done
	@ rm $$resolved_file

# Clean build artifacts and generated docs
clean:
	rm -rf bin
	rm -rf docs
	rm -rf .venv
	rm -rf node_modules

test:
	go test -v ./internal/core

# Generate go structs from jsonschemas
generate:
	@echo "Generating Go structs using quicktype..."
	$(QUICKTYPE) --lang go \
		--package "core" \	# This option seems bugged
		--src $(SCHEMA_DIR)/did_schema_example.json \
		--top-level DID \
		--out $(OUTPUT_FILE)
	$(QUICKTYPE) --lang go \
		--package "core" \	# This option seems bugged
		--src $(SCHEMA_DIR)/vc_schema_example.json \
		--top-level VC \
		--out $(OUTPUT_FILE)

# Do everything: clean + generate + build + (format) run + docs + test
all: clean generate test build run docs

