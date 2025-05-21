#!/bin/bash

echo "Generating DID and VC docs ..."

SCHEMA_DIR="./internal/jsonschema"
DOCS="./docs/schema/md"
VENV=".venv"

mkdir -p "$DOCS"

for file in "$SCHEMA_DIR"/*.json; do
  echo "Generating md docs for: $file"
  "$VENV/bin/generate-schema-doc" "$file" --config template_name=md
  mv schema_doc.md "$DOCS/$(basename "$file" .json).md"
done
