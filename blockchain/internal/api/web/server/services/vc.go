package services

import (
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"encoding/json"
	"log"
)

// TODO: Change jsonschemas of create & revoke endpoint to match new infrastructure then adjust handler & service accordingly
// TODO: Add handler & service for vps +  adjust ref schemas in endpoint definition in openapi.yaml (POST /api/v1/vps/verify) + response & request schema & load the new schemas in handlers.go

// VCService defines the interface for creating and returning vcs of the blockchain
type VCService interface {
	GetVCRecord(ctx context.Context, vcId string) (*coreTypes.VCRecord, error)
	GetVCRecords(ctx context.Context) (*[]coreTypes.VCRecord, error)
	//CreateVCRecord(userContext context.Context, createVcRecord *models.VCSchema) error
	RevokeVCRecord(ctx context.Context, vcId string, vcHash string) error
}

// vcService is a concrete implementation of the VCService interface.
type vcService struct {
	chain *core.Blockchain
}

// NewVCService creates and returns a new instance of the VCService implementation.
func NewVCService(chain *core.Blockchain) VCService {
	return &vcService{chain: chain}
}

// GetVCRecords retrieves all VC records from the blockchain
func (v *vcService) GetVCRecords(ctx context.Context) (*[]coreTypes.VCRecord, error) {
	var vcRecords []coreTypes.VCRecord
	var vcRecord coreTypes.VCRecord
	var err error
	for i := len(*v.chain) - 1; i >= 0; i-- {
		block := *v.chain.GetBlock(i)
		for _, transaction := range block.Transactions {
			err = json.Unmarshal(transaction, &vcRecord)
			if err != nil {
				return nil, err
			}
			if utils.IsUrnValid(vcRecord.ID) && !containsVcRecord(vcRecords, vcRecord.ID) {
				vcRecords = append(vcRecords, vcRecord)
			}
		}
	}
	return &vcRecords, nil
}

// GetVCRecord retrieves a VC record by urn
func (v *vcService) GetVCRecord(ctx context.Context, vcId string) (*coreTypes.VCRecord, error) {
	vcRecord, err := v.chain.FindVCRecord(vcId)
	if err != nil {
		log.Printf("Error finding VC record: %v", err)
		return nil, err
	}
	return vcRecord, nil
}

//// CreateVCRecord creates a new VC record on the blockchain based on the provided VC
//func (v *vcService) CreateVCRecord(userContext context.Context, createVcRecord *models.VcRecordSchema) error {
//
//	// Transform from api types to core types - Works because of equal JSON tags
//	var err error
//	jsonBytes, err := json.Marshal(createVcRecord)
//	if err != nil {
//		log.Printf("Internal Server Error: %s", err)
//		return err
//	}
//	vcRecord, err := coreTypes.UnmarshalVCRecord(jsonBytes)
//	if err != nil {
//		log.Printf("Internal Server Error: %s", err)
//		return err
//	}
//
//	// Create Transaction
//	if err := v.chain.AppendVcRecord(&vcRecord); err != nil {
//		log.Printf("Internal Server Error: %s", err)
//		return err
//	}
//	return nil
//}

// RevokeVCRecord revokes a VC record based on its identifier and hash
func (v *vcService) RevokeVCRecord(ctx context.Context, vcId string, vcHash string) error {
	if err := v.chain.RevokeVcRecord(vcId, vcHash); err != nil {
		log.Printf("Error revoking DID: %s", err)
		return err
	}
	return nil
}

// containsDid checks if a DID is in a list of DIDs
// true if the list contains this DID already
// false if the list does not contain this DID
func containsVcRecord(didList []coreTypes.VCRecord, vcId string) bool {
	for _, did := range didList {
		if did.ID == vcId {
			return true
		}
	}
	return false
}
