FROM golang:alpine AS builder

RUN <<EOF
set -e
go install github.com/swaggo/swag/cmd/swag@latest
EOF

WORKDIR /app

# Copy only required files
COPY go.mod go.sum ./
RUN go mod download

COPY cmd/ cmd/
COPY internal/ internal/

RUN swag init -g ./cmd/main.go -o ./docs/swagger/
# Build the application
RUN go build -o /blockchain ./cmd/main.go

# Final image
FROM alpine:latest

# Set working directory
WORKDIR /app

# Copy binary from builder
COPY --from=builder /blockchain /bin/blockchain

CMD ["/bin/blockchain", "-web"]
