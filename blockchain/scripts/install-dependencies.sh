#!/bin/bash

set -e

VENV=".venv"
PIP="$VENV/bin/pip"

# Activate venv
python3 -m venv $VENV
$PIP install --upgrade pip

# Go installs
go install github.com/swaggo/swag/cmd/swag@latest
go get github.com/multiformats/go-multibase@latest
go install github.com/princjef/gomarkdoc/cmd/gomarkdoc@latest
go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest
go get github.com/labstack/echo/v4
go get github.com/oapi-codegen/runtime
go get github.com/xeipuuv/gojsonschema

# NPM installs
npm install --save-dev quicktype@23.2.4 # flag makes sure its in the projects devDependencies not dependencies
npm install --save-dev json-schema-resolver
npm install --save-dev typedoc
npm install --save-dev @redocly/cli # openapi cli for doc generateion and linting
npm install --save-dev @types/react @types/react-dom @tanstack/react-router @radix-ui/react-slot @radix-ui/react-navigation-menu
npm install --save-dev class-variance-authority
npm install --save-dev lucide-react
npm install --save-dev tailwind-merge
npm install --save-dev web-vitals
npm install --save-dev typedoc typedoc-plugin-markdown
npm install --save-dev prettier
# PIP installs
$PIP install json-schema-for-humans
