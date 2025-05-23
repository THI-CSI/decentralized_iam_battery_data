package services

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"errors"
	"time"
)

// VCService defines the interface for creating and returning vcs of the blockchain
type VCService interface {
	GetVCRecord(ctx context.Context, vcId string) (*coreTypes.VCRecord, error)
	CreateVCRecord(userContext context.Context, request *domain.VCRequest) (*coreTypes.VCRecord, error)
}

// vcService is a concrete implementation of the VCService interface.
type vcService struct {
	chain *core.Blockchain
}

// NewVCService creates and returns a new instance of the VCService implementation.
func NewVCService(chain *core.Blockchain) VCService {
	return &vcService{chain: chain}
}

// GetVCRecord retrieves a VC record by urn
func (v *vcService) GetVCRecord(ctx context.Context, vcId string) (*coreTypes.VCRecord, error) {
	return v.chain.FindVCRecord(vcId)
}

// CreateVCRecord creates a new VC record on the blockchain based on the provided VC
func (v *vcService) CreateVCRecord(userContext context.Context, request *domain.VCRequest) (*coreTypes.VCRecord, error) {

	vcExists, _ := v.chain.FindVCRecord(request.ID)
	if vcExists != nil {
		return nil, errors.New("VC is already recorded on the blockchain")
	}

	vcRecord := coreTypes.VCRecord{
		ExpirationDate: request.ExpirationDate,
		ID:             request.ID,
		Timestamp:      time.Now(),
		VcHash:         request.VcHash,
	}

	// Create Transaction
	if err := v.chain.AppendVcRecords(&vcRecord); err != nil {
		return nil, err
	}

	return &vcRecord, nil
}
