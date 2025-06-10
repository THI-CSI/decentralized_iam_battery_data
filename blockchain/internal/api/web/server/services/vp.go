package services

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/gibson042/canonicaljson-go"
	"github.com/google/go-cmp/cmp"
)

// VPService defines the interface for creating and returning vcs of the blockchain
type VPService interface {
	VerifyVP(ctx context.Context, verify *models.VerifyVpJSONRequestBody) error
}

// vcService is a concrete implementation of the VCService interface.
type vpService struct {
	chain *core.Blockchain
}

// NewVPService creates and returns a new instance of the VCService implementation.
func NewVPService(chain *core.Blockchain) VPService {
	return &vpService{chain: chain}
}

// VerifyVP verifies that the recieved VP contains valid DIDs and a valid VC
func (v *vpService) VerifyVP(ctx context.Context, requestBody *models.VpSchema) error {
	// Check signature of VP
	verifiedBytes, err := utils.VerifyJWS(v.chain, requestBody.Proof.Jws, requestBody.Proof.VerificationMethod)
	if err != nil {
		return err
	}
	var verified models.VpSchema
	if err := json.Unmarshal(verifiedBytes, &verified); err != nil {
		return err
	}
	requestBody.Proof.Jws = "" // Because this will default to its zero value when unmarshalling verified
	canon1, err := canonicaljson.Marshal(verified)
	if err != nil {
		return err
	}
	canon2, err := canonicaljson.Marshal(requestBody)
	if err != nil {
		return err
	}
	if !bytes.Equal(canon1, canon2) {
		fmt.Println("Canonical diff:", cmp.Diff(canon1, canon2))
		return errors.New("signed data differs from the payload")
	}
	// Check VC Hash
	errr := utils.CheckVCSemantics(&verified.VerifiableCredential[0])
	if errr == nil {
		if vcBMS, err := verified.VerifiableCredential[0].AsVcBmsProducedSchema(); err == nil {
			if vcHash, err := utils.Generate256HashHex(vcBMS); err == nil {
				return interpretVCState(v.chain.CheckVCRecordState(vcBMS.Id, vcHash))
			} else {
				return err
			}
		} else if vcService, err := verified.VerifiableCredential[0].AsVcServiceAccessSchema(); err == nil {
			if vcHash, err := utils.Generate256HashHex(vcService); err == nil {
				return interpretVCState(v.chain.CheckVCRecordState(vcService.Id, vcHash))
			} else {
				return err
			}
		} else if vcCloud, err := verified.VerifiableCredential[0].AsVcCloudInstanceSchema(); err == nil {
			if vcHash, err := utils.Generate256HashHex(vcCloud); err == nil {
				return interpretVCState(v.chain.CheckVCRecordState(vcCloud.Id, vcHash))
			} else {
				return err
			}
		}
	}
	return errr
}

func interpretVCState(state core.VCState) error {
	if state == core.VCValid {
		return nil
	} else if state == core.VCPending {
		return errors.New("vc is on the list of pending transactions try again later")
	} else if state == core.VCExpired {
		return errors.New("vc is expired")
	} else if state == core.VCTampered {
		return errors.New("vc has been tampered with")
	}
	return errors.New("vc not on the blockchain")
}
