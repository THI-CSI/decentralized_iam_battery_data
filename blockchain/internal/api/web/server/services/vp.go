package services

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/core"
	"context"
)

// VCService defines the interface for creating and returning vcs of the blockchain
type VPService interface {
	VerifyVP(ctx context.Context, verify *models.VerifyVpJSONRequestBody) error
}

// vcService is a concrete implementation of the VCService interface.
type vpService struct {
	chain *core.Blockchain
}

// NewVCService creates and returns a new instance of the VCService implementation.
func NewVPService(chain *core.Blockchain) VPService {
	return &vpService{chain: chain}
}

func (v *vpService) VerifyVP(ctx context.Context, verify *models.VpSchema) error {
	// TODO: implement (JWS contains the signed content - can be parsed from JWS token and compared to payload)
	return nil
}
