package services

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	"context"
	"encoding/json"
	"errors"
	"reflect"
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

func (v *vpService) VerifyVP(ctx context.Context, requestBody *models.VpSchema) error {
	verifiedBytes, err := utils.VerfiyJWS(v.chain, requestBody.Proof.Jws, requestBody.Proof.VerificationMethod)
	if err != nil {
		return err
	}
	var verified models.VpSchema
	if err := json.Unmarshal(verifiedBytes, &verified); err != nil {
		return err
	}
	requestBody.Proof.Jws = "" // Because this will default to its zero value when unmarshalling verified
	if !reflect.DeepEqual(requestBody, verified) {
		return nil
	} else {
		return errors.New("signed data differs from the payload")
	}
}
