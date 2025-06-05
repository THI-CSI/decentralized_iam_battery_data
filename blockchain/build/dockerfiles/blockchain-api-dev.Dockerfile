FROM golang:alpine AS builder

RUN apk add --no-cache bash python3 py3-pip

RUN python3 -m venv /app/.venv \
 && /app/.venv/bin/pip install --upgrade pip \
 && /app/.venv/bin/pip install json-schema-for-humans

# Set working directory
WORKDIR /app

# Copy required files
COPY go.mod go.sum ./
RUN go mod download

COPY cmd/ cmd/
COPY internal/ internal/
COPY scripts/generate-did-vc-docs-html.sh ./
RUN chmod +x generate-did-vc-docs-html.sh

# Generate HTML docs
RUN /bin/bash "./generate-did-vc-docs-html.sh"

RUN go build -o /blockchain ./cmd/main.go

FROM alpine:latest

# Set working directory
WORKDIR /app

# Copy built binary
COPY --from=builder /blockchain /bin/blockchain
COPY --from=builder /app/docs /app/docs

CMD ["/bin/blockchain", "-web"]
