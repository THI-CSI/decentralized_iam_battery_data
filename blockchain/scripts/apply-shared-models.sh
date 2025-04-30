#!/usr/bin/env bash
# Usage: apply-shared-imports.sh <models-dir>
set -e

MODELS_DIR="$1"

if [[ -z "$MODELS_DIR" ]]; then
  echo "Usage: $0 <models-dir>"
  exit 1
fi

# Insert import for shared package if not already
for f in "$MODELS_DIR"/*.go; do
  # Skip shared.go itself
  [[ $(basename "$f") == "shared.go" ]] && continue

  # Replace duplicated struct definitions with shared types
  sed -i '' 's/type Context .*/type Context = shared.Context/' "$f" || true
  sed -i '' 's/type Proof .*/type Proof = shared.Proof/' "$f" || true
  sed -i '' 's/type Issuer .*/type Issuer = shared.Issuer/' "$f" || true
done
