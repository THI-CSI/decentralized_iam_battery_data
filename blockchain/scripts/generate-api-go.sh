#!/bin/bash

set -e

WORKINGDIR="./internal/api/web/"
#INPUT_SPEC="./internal/api/web/openapi.yaml"
BUNDLED_SPEC="./internal/api/web/openapi.bundled.yaml"
OUTPUT_DIR="./internal/api/web/generated"
PACKAGE_NAME="web"
REDOCLY="../../../node_modules/.bin/redocly"

echo "Bundling OpenAPI spec with Redocly..."
cd $WORKINGDIR
$REDOCLY bundle "openapi.yaml" -o "openapi.bundled.yaml"
cd ../../..

echo "Ensuring output directory exists..."
mkdir -p "$OUTPUT_DIR"

echo "Generating Go types and server interface..."
oapi-codegen -generate types,server -package "$PACKAGE_NAME" -o "$OUTPUT_DIR/api.gen.go" "$BUNDLED_SPEC"

echo "Done. Output written to $OUTPUT_DIR/api.gen.go"