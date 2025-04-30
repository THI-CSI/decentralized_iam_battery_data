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
OUTPUT_DIR="./internal/core/models"

# Activate venv
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

# Install dependencies
install: $(VENV)/bin/activate
	# Go installs
	go install github.com/swaggo/swag/cmd/swag@latest
	go install github.com/princjef/gomarkdoc/cmd/gomarkdoc@latest
	go get github.com/fiorix/jsonschema2go
	#go install github.com/fiorix/jsonschema2go
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
	@mkdir -p $(OUTPUT_DIR)

	# DID Schema
	$(QUICKTYPE) --lang go \
		--top-level DID \
		--src $(SCHEMA_DIR)/did/didDocument.schema.json \
		--out $(OUTPUT_DIR)/did_document.go

	# VC - Entity Schemas
	$(QUICKTYPE) --lang go \
		--top-level CreateEntity \
		--src $(SCHEMA_DIR)/vc/entity/create-entity.schema.json \
		--out $(OUTPUT_DIR)/create_entity.go

	$(QUICKTYPE) --lang go \
		--top-level ModifyEntity \
		--src $(SCHEMA_DIR)/vc/entity/modify-entity.schema.json \
		--out $(OUTPUT_DIR)/modify_entity.go

	# VC - Access Schemas
	$(QUICKTYPE) --lang go \
		--top-level GrantAccess \
		--src $(SCHEMA_DIR)/vc/access/grant-access.schema.json \
		--out $(OUTPUT_DIR)/grant_access.go

	$(QUICKTYPE) --lang go \
		--top-level RevokeAccess \
		--src $(SCHEMA_DIR)/vc/access/revoke-access.schema.json \
		--out $(OUTPUT_DIR)/revoke_access.go

	# VC - Relationship Schemas
	$(QUICKTYPE) --lang go \
		--top-level BmsLinked \
		--src $(SCHEMA_DIR)/vc/relationships/bms-linked.schema.json \
		--out $(OUTPUT_DIR)/bms_linked.go

	$(QUICKTYPE) --lang go \
		--top-level Produced \
		--src $(SCHEMA_DIR)/vc/relationships/produced.schema.json \
		--out $(OUTPUT_DIR)/produced.go

	@echo "Applying common imports and refactoring duplicates..."
	@./scripts/apply-shared-models.sh $(OUTPUT_DIR)

#generate:
#	@echo "Generating Go structs using go-jsonschema..."
#	mkdir -p $(OUTPUT_DIR)
#
#	# DID Schema
#	jsonschema2go \
#		-p models \
#		-o $(OUTPUT_DIR)/did_document.go \
#		$(SCHEMA_DIR)/did/didDocument.schema.json
#
#	# VC - Entity Schemas
#	jsonschema2go -p models -o $(OUTPUT_DIR)/create_entity.go \
#		$(SCHEMA_DIR)/vc/entity/create-entity.schema.json
#	jsonschema2go -p models -o $(OUTPUT_DIR)/modify_entity.go \
#		$(SCHEMA_DIR)/vc/entity/modify-entity.schema.json
#
#	# VC - Access Schemas
#	jsonschema2go -p models -o $(OUTPUT_DIR)/grant_access.go \
#		$(SCHEMA_DIR)/vc/access/grant-access.schema.json
#	jsonschema2go -p models -o $(OUTPUT_DIR)/revoke_access.go \
#		$(SCHEMA_DIR)/vc/access/revoke-access.schema.json
#
#	# VC - Relationship Schemas
#	jsonschema2go -p models -o $(OUTPUT_DIR)/bms_linked.go \
#		$(SCHEMA_DIR)/vc/relationship/bms-linked.schema.json
#	jsonschema2go -p models -o $(OUTPUT_DIR)/ownership.go \
#		$(SCHEMA_DIR)/vc/relationship/ownership.schema.json
#
#	@echo "Applying common imports and refactoring duplicates..."
#	@./scripts/apply-shared-models.sh $(OUTPUT_DIR)

# Do everything: clean + generate + build + (format) run + docs + test
all: clean generate test build run docs

