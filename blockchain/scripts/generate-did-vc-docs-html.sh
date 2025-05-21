#!/bin/bash

echo "Generating DID and VC docs ..."

SCHEMA_DIR="./internal/jsonschema"
DOCS="./docs/schema/html"
VENV=".venv"

mkdir -p "$DOCS"

for file in "$SCHEMA_DIR"/*.json; do
  echo "Generating html docs for: $file"
  "$VENV/bin/generate-schema-doc" "$file"
  mv schema_doc.html "$DOCS/$(basename "$file" .json).html"
done

mv "schema_doc.css" "schema_doc.min.js" "./docs/schema/html"
