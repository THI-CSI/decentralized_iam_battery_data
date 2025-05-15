package services

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"crypto/sha3"
	"encoding/hex"
	"encoding/json"
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
	var vcResponse coreTypes.VCRecord
	for _, block := range *chain {
		for _, transaction := range block.Transactions {
			err := json.Unmarshal(transaction, &vcResponse)
			if err != nil {
				// TODO
				// check in the future if there is a better way
				continue
			}
			if vcResponse.ID == vcId {
				return &vcResponse, nil
			}
		}
	}
	return nil, domain.NotFoundError("VC record not found")
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
	// TODO Check if VC Record hash already exists
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
