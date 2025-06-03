#!/bin/bash

set -e

SPEC="./internal/api/web/openapi.yaml"
BUNDLED_SPEC="./internal/api/web/openapi.bundled.yaml"
OUTPUT_DIR="./internal/api/web/server"
PACKAGE_NAME="models"

echo "Bundling OpenAPI spec with Redocly..."
npx redocly bundle "$SPEC" -o "$BUNDLED_SPEC"

echo "Ensuring output directory exists..."
mkdir -p "$OUTPUT_DIR"

echo "Generating Go types and server interface..."
oapi-codegen -generate models,server -package "$PACKAGE_NAME" -o "$OUTPUT_DIR/api.gen.go" "$BUNDLED_SPEC"

echo "Done. Output written to $OUTPUT_DIR/api.gen.go"

#echo "Generating Go server code with openapi-generator-cli..."
#npx @openapitools/openapi-generator-cli generate \
#  -i "$BUNDLED_SPEC" \
#  -g go-server \
#  -o "$OUTPUT_DIR" \
#  --package-name "$PACKAGE_NAME"
#
#echo "Done. Output written to $OUTPUT_DIR"
