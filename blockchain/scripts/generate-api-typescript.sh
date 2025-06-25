#!/usr/bin/env bash

set -e

PROJECT_ROOT=$(dirname "$(dirname "$0")")
SPEC="${PROJECT_ROOT}/internal/api/web/openapi.bundled.yaml"
GENERATED="${PROJECT_ROOT}/frontend/src/api/generated"
CONFIG="${GENERATED}/config.json"
TMP="${PROJECT_ROOT}/tmp"

mkdir -p "${TMP}"
mkdir -p "${GENERATED}/.openapi-generator"
touch "${GENERATED}/config.json" "${GENERATED}/.openapi-generator-ignore" "${GENERATED}/README.md"
mv "${GENERATED}/config.json" "${GENERATED}/.openapi-generator-ignore" "${GENERATED}/.openapi-generator" "${GENERATED}/README.md" "${TMP}"
rm -rf "$GENERATED"
mkdir -p "$GENERATED"
mv "${TMP}/config.json" "${TMP}/.openapi-generator-ignore" "${TMP}/.openapi-generator" "${TMP}/README.md" "${GENERATED}"

npx @openapitools/openapi-generator-cli generate -g typescript-fetch -i "${SPEC}" -o "${GENERATED}" -c "${CONFIG}"

npx prettier --write "${SPEC}"