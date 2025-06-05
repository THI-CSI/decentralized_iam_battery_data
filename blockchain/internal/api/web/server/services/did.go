package services

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"encoding/json"
	"log"
)

// DidService defines the interface for managing Decentralized Identifiers (DIDs)
// and their associated access rights.
type DidService interface {
	GetDIDs(ctx context.Context) (*[]coreTypes.Did, error)
	GetDID(userContext context.Context, did string) (*coreTypes.Did, error)
	CreateOrModifyDID(userContext context.Context, create *models.DidSchema) error
	RevokeDid(userContext context.Context, did string) error
	GetPublicKey(did string) (string, error)
}

// didService is a concrete implementation of the DidService interface.
type didService struct {
	chain *core.Blockchain
}

// NewDidService creates and returns a new instance of the DidService implementation.
func NewDidService(chain *core.Blockchain) DidService {
	return &didService{chain: chain}
}

// GetDIDs returns all DIDs in the blockchain
func (s *didService) GetDIDs(ctx context.Context) (*[]coreTypes.Did, error) {
	var dids []coreTypes.Did
	var did coreTypes.Did
	var err error
	for i := len(*s.chain) - 1; i >= 0; i-- {
		block := *s.chain.GetBlock(i)
		for _, transaction := range block.Transactions {
			err = json.Unmarshal(transaction, &did)
			if err != nil {
				return nil, err
			}
			if utils.IsDidValid(did.ID) && !containsDid(dids, did.ID) {
				dids = append(dids, did)
			}
		}
	}
	return &dids, nil
}

// GetDID returns a single DID
func (s *didService) GetDID(userContext context.Context, did string) (*coreTypes.Did, error) {
	didDoc, err := s.chain.FindDID(did)
	if err != nil {
		log.Printf("Error finding DID: %s", err)
		return nil, err
	}
	return didDoc, nil
}

// CreateOrModifyDID appends a new DID or a modification to the blockchain
func (s *didService) CreateOrModifyDID(userContext context.Context, createDid *models.DidSchema) error {
	// Transform from api types to core types - Works because of equal JSON tags
	var err error
	jsonBytes, err := json.Marshal(createDid)
	if err != nil {
		log.Printf("Internal Server Error: %s", err)
		return err
	}
	did, err := coreTypes.UnmarshalDid(jsonBytes)
	if err != nil {
		log.Printf("Internal Server Error: %s", err)
		return err
	}

	// Create Transaction
	if err := s.chain.AppendDid(&did); err != nil {
		log.Printf("Internal Server Error: %s", err)
		return err
	}
	return nil
}

// RevokeDid revokes an existing DID on the blockchain
func (s *didService) RevokeDid(userContext context.Context, didId string) error {
	if err := s.chain.RevokeDid(didId); err != nil {
		log.Printf("Error revoking DID: %s", err)
		return err
	}

	return nil
}

// containsDid checks if a DID is in a list of DIDs
// true if the list contains this DID already
// false if the list does not contain this DID
func containsDid(didList []coreTypes.Did, didId string) bool {
	for _, did := range didList {
		if did.ID == didId {
			return true
		}
	}
	return false
}

func (s *didService) GetPublicKey(did string) (string, error) {
	didDoc, err := s.chain.FindDID(did)
	if err != nil {
		log.Printf("Error finding DID: %s", err)
		return "", err
	}

	return didDoc.VerificationMethod.PublicKeyMultibase, nil
}
