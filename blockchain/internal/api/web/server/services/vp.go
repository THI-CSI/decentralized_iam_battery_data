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
	"strings"
)

// VPService defines the interface for creating and returning vcs of the blockchain
type VPService interface {
	VerifyVPForCloud(ctx context.Context, verify *models.VerifyVpCloudJSONRequestBody) error
	VerifyVPForServices(ctx context.Context, verify *models.VerifyVpServicesJSONRequestBody) error
	VerifyVPForBms(ctx context.Context, verify *models.VerifyVpBmsJSONRequestBody) error
}

// vcService is a concrete implementation of the VCService interface.
type vpService struct {
	chain *core.Blockchain
}

// NewVPService creates and returns a new instance of the VCService implementation.
func NewVPService(chain *core.Blockchain) VPService {
	return &vpService{chain: chain}
}

func (v *vpService) VerifyVPForCloud(ctx context.Context, requestBody *models.VpCloudSchema) error {
	verifiedBytes, err := utils.VerifyJWS(v.chain, requestBody.Proof.Jws, requestBody.Proof.VerificationMethod)
	if err != nil {
		return err
	}
	var verified models.VpCloudSchema
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

	if err := checkVPSemanticsForCloud(requestBody); err != nil {
		return err
	}

	// Check VC Hash
	if err := utils.VerifyRequestCreateCloud(&verified.VerifiableCredential[0]); err != nil {
		return err
	}

	if vcHash, err := utils.Generate256HashHex(&verified.VerifiableCredential[0]); err == nil {
		return interpretVCState(v.chain.CheckVCRecordState(verified.VerifiableCredential[0].Id, vcHash))
	}

	return nil
}

func (v *vpService) VerifyVPForBms(ctx context.Context, requestBody *models.VpBmsSchema) error {
	verifiedBytes, err := utils.VerifyJWS(v.chain, requestBody.Proof.Jws, requestBody.Proof.VerificationMethod)
	if err != nil {
		return err
	}
	var verified models.VpBmsSchema
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

	if err := checkVPSemanticsForBms(requestBody); err != nil {
		return err
	}

	// Check VC Hash
	if err := utils.VerifyRequestCreateBms(&verified.VerifiableCredential[0]); err != nil {
		return err
	}

	if vcHash, err := utils.Generate256HashHex(&verified.VerifiableCredential[0]); err == nil {
		return interpretVCState(v.chain.CheckVCRecordState(verified.VerifiableCredential[0].Id, vcHash))
	}

	return nil
}

func (v *vpService) VerifyVPForServices(ctx context.Context, requestBody *models.VpServiceSchema) error {
	verifiedBytes, err := utils.VerifyJWS(v.chain, requestBody.Proof.Jws, requestBody.Proof.VerificationMethod)
	if err != nil {
		return err
	}
	var verified models.VpServiceSchema
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

	if err := checkVPSemanticsForServices(requestBody); err != nil {
		return err
	}

	// Check VC Hash
	if err := utils.VerifyRequestCreateServices(&verified.VerifiableCredential[0]); err != nil {
		return err
	}

	if vcHash, err := utils.Generate256HashHex(&verified.VerifiableCredential[0]); err == nil {
		return interpretVCState(v.chain.CheckVCRecordState(verified.VerifiableCredential[0].Id, vcHash))
	}

	return nil
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

func checkVPSemanticsForCloud(requestBody *models.VpCloudSchema) error {
	parts := strings.SplitN(requestBody.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]
	if requestBody.VerifiableCredential[0].Holder == verificationMethodDID && verificationMethodDID == requestBody.Holder {
		return nil
	}
	return fmt.Errorf("the following 3 dids have to match: VC holder: '%s'; VP holder: '%s'; VP proof verification method: '%s'", requestBody.VerifiableCredential[0].Holder, requestBody.Holder, verificationMethodDID)
}

func checkVPSemanticsForServices(requestBody *models.VpServiceSchema) error {
	parts := strings.SplitN(requestBody.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]
	if requestBody.VerifiableCredential[0].Holder == verificationMethodDID && verificationMethodDID == requestBody.Holder {
		return nil
	}
	return fmt.Errorf("the following 3 dids have to match: VC holder: '%s'; VP holder: '%s'; VP proof verification method: '%s'", requestBody.VerifiableCredential[0].Holder, requestBody.Holder, verificationMethodDID)
}

func checkVPSemanticsForBms(requestBody *models.VpBmsSchema) error {
	parts := strings.SplitN(requestBody.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]
	if requestBody.VerifiableCredential[0].Holder == verificationMethodDID && verificationMethodDID == requestBody.Holder {
		return nil
	}
	return fmt.Errorf("the following 3 dids have to match: VC holder: '%s'; VP holder: '%s'; VP proof verification method: '%s'", requestBody.VerifiableCredential[0].Holder, requestBody.Holder, verificationMethodDID)
}
