#!/bin/bash

set -e

VENV=".venv"
PIP="$VENV/bin/pip"

# Activate venv
python3 -m venv $VENV
$PIP install --upgrade pip

# Go installs
go install github.com/swaggo/swag/cmd/swag@latest
go install github.com/princjef/gomarkdoc/cmd/gomarkdoc@latest
# NPM installs
npm install --save-dev quicktype@23.2.4 # flag makes sure its in the projects devDependencies not dependencies
npm install --save-dev json-schema-resolver
# PIP installs
$PIP install json-schema-for-humans
