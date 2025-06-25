FROM golang:alpine AS builder

RUN apk add --no-cache bash python3 py3-pip nodejs npm


# install dependencies
RUN python3 -m venv /app/.venv \
 && /app/.venv/bin/pip install --upgrade pip \
 && /app/.venv/bin/pip install json-schema-for-humans
RUN npm install --save-dev @redocly/cli --prefix /app

# Set working directory
WORKDIR /app

# Copy required files
COPY ./blockchain/go.mod ./blockchain/go.sum ./
RUN go mod download

COPY ./blockchain/cmd/ cmd/
COPY ./blockchain/internal/ ./internal/
COPY ./blockchain/scripts/generate-did-vc-docs-html.sh ./
RUN chmod +x generate-did-vc-docs-html.sh

# Generate HTML docs
RUN /bin/bash "./generate-did-vc-docs-html.sh"

# Generate Swagger Html file
RUN ./node_modules/.bin/redocly build-docs ./internal/api/web/openapi.yaml --output ./docs/openapi.html

# Build blockchain application
RUN go build -o /blockchain ./cmd/main.go

FROM alpine:latest

# Set working directory
WORKDIR /app

# Copy built binary
COPY --from=builder /blockchain /bin/blockchain
COPY --from=builder /app/docs /app/docs

CMD ["/bin/blockchain", "-web"]
