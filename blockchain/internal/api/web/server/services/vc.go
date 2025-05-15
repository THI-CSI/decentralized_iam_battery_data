package services

import (
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"crypto/sha3"
	"encoding/hex"
	"encoding/json"
	"errors"
	"time"
)

// VCService defines the interface for creating and returning vcs of the blockchain
type VCService interface {
	GetVCRecord(ctx context.Context, chain *core.Blockchain, vcId string) (*coreTypes.VCRecord, error)
	CreateVCRecord(userContext context.Context, chain *core.Blockchain, vcSchema *coreTypes.Vc) (*coreTypes.VCRecord, error)
}

// vcService is a concrete implementation of the VCService interface.
type vcService struct{}

// NewVCService creates and returns a new instance of the VCService implementation.
func NewVCService() VCService {
	return &vcService{}
}

// GetVCRecord retrieves a VC record by urn
func (v *vcService) GetVCRecord(ctx context.Context, chain *core.Blockchain, vcId string) (*coreTypes.VCRecord, error) {
	return chain.FindVCRecord(vcId)
}

// CreateVCRecord creates a new VC record on the blockchain based on the provided VC
func (v *vcService) CreateVCRecord(userContext context.Context, chain *core.Blockchain, vcSchema *coreTypes.Vc) (*coreTypes.VCRecord, error) {
	hasher := sha3.New256()
	rawJson, _ := json.Marshal(vcSchema)
	_, err := hasher.Write(rawJson)
	if err != nil {
		return nil, err
	}
	hash := hasher.Sum(nil)

	vcExists, _ := chain.FindVCRecord(vcSchema.ID)
	if vcExists != nil {
		return nil, errors.New("VC is already recorded on the blockchain")
	}

	vcRecord := coreTypes.VCRecord{
		ExpirationDate: vcSchema.ExpirationDate,
		ID:             vcSchema.ID,
		Timestamp:      time.Now(),
		VcHash:         hex.EncodeToString(hash),
	}

	// Create Transaction
	if err := chain.AppendVcRecords(&vcRecord); err != nil {
		return nil, err
	}

	return &vcRecord, nil
}
