#!/bin/bash

echo "Generating DID and VC docs ..."

SCHEMA_DIR="./internal/jsonschema"
DOCS="./docs"
VENV=".venv"

mkdir -p "$DOCS"

for file in "$SCHEMA_DIR"/*.json; do
  echo "Generating docs for: $file"
  "$VENV/bin/generate-schema-doc" "$file" --config template_name=md
  mv schema_doc.md "$DOCS/$(basename "$file" .json).md"
done
