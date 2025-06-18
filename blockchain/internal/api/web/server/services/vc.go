package services

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"reflect"
	"strings"
	"time"
)

// VCService defines the interface for creating and returning vcs of the blockchain
type VCService interface {
	GetVCRecord(ctx context.Context, vcId string) (*coreTypes.VCRecord, error)
	GetVCRecords(ctx context.Context) (*[]coreTypes.VCRecord, error)
	CreateVCRecordBms(userContext context.Context, createVcRecord *models.CreateVcRecordBmsJSONRequestBody) error
	CreateVCRecordCloud(userContext context.Context, createVcRecord *models.CreateVcRecordCloudJSONRequestBody) error
	CreateVCRecordServices(userContext context.Context, createVcRecord *models.CreateVcRecordServicesJSONRequestBody) error
	RevokeVCRecord(ctx context.Context, vcId string) error
	VerifyRequestRevoke(requestBody models.RequestVcRevokeSchema) error
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
			vcRecord = coreTypes.VCRecord{}
			err = json.Unmarshal(transaction, &vcRecord)
			if err != nil {
				return nil, err
			}
			if utils.IsUrnValid(vcRecord.ID) && !containsVcRecord(vcRecords, vcRecord.ID) {
				vcRecords = append(vcRecords, vcRecord)
			}
		}
	}
	if len(vcRecords) == 0 {
		return nil, errors.New("no VC records found")
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

// CreateVCRecordCloud creates a new VC record on the blockchain based on the provided VC
func (v *vcService) CreateVCRecordCloud(userContext context.Context, createVcRecord *models.CreateVcRecordCloudJSONRequestBody) error {
	parts := strings.SplitN(createVcRecord.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]

	if createVcRecord.Issuer != verificationMethodDID {
		return fmt.Errorf("VC issuer DID '%s' does not match the proof's verification method DID '%s'", createVcRecord.Issuer, verificationMethodDID)
	}
	if createVcRecord.Holder != createVcRecord.CredentialSubject.Id {
		return fmt.Errorf("the VC holder %s does not match the credential subject id %s", createVcRecord.Holder, createVcRecord.CredentialSubject.Id)
	}
	now := time.Now()
	if now.Before(createVcRecord.CredentialSubject.Timestamp) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", createVcRecord.CredentialSubject.Timestamp.Format(time.RFC3339), now.Format(time.RFC3339))
	}

	var vcRecord coreTypes.VCRecord
	hashString, err := utils.Generate256HashHex(createVcRecord)
	if err != nil {
		log.Printf("Error generating hash: %v", err)
		return err
	}
	vcRecord.ID = createVcRecord.Id
	vcRecord.Timestamp = time.Now()
	vcRecord.ExpirationDate = createVcRecord.ExpirationDate
	vcRecord.VcHash = hashString
	err = v.chain.AppendVcRecord(&vcRecord)
	if err != nil {
		log.Printf("Error appending VC record: %v", err)
		return err
	}

	return nil
}

// CreateVCRecordBms creates a new VC record on the blockchain based on the provided VC
func (v *vcService) CreateVCRecordBms(userContext context.Context, createVcRecord *models.CreateVcRecordBmsJSONRequestBody) error {
	parts := strings.SplitN(createVcRecord.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]

	if createVcRecord.Issuer != verificationMethodDID || verificationMethodDID != createVcRecord.CredentialSubject.BmsDid {
		return fmt.Errorf("the following 3 dids have to match: VC Issuer: '%s'; VC credentialSubject BMSdid: '%s'; VC proof verification method: '%s'", createVcRecord.Issuer, createVcRecord.CredentialSubject.BmsDid, verificationMethodDID)
	}
	if createVcRecord.Holder != createVcRecord.CredentialSubject.Id {
		return fmt.Errorf("the VC holder %s does not match the credential subject id %s", createVcRecord.Holder, createVcRecord.CredentialSubject.Id)
	}
	now := time.Now()
	if now.Before(createVcRecord.CredentialSubject.Timestamp) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", createVcRecord.CredentialSubject.Timestamp.Format(time.RFC3339), now.Format(time.RFC3339))
	}

	var vcRecord coreTypes.VCRecord
	hashString, err := utils.Generate256HashHex(createVcRecord)
	if err != nil {
		log.Printf("Error generating hash: %v", err)
		return err
	}
	vcRecord.ID = createVcRecord.Id
	vcRecord.Timestamp = time.Now()
	vcRecord.ExpirationDate = createVcRecord.ExpirationDate
	vcRecord.VcHash = hashString
	err = v.chain.AppendVcRecord(&vcRecord)
	if err != nil {
		log.Printf("Error appending VC record: %v", err)
		return err
	}

	return nil
}

// CreateVCRecordServices creates a new VC record on the blockchain based on the provided VC
func (v *vcService) CreateVCRecordServices(userContext context.Context, createVcRecord *models.CreateVcRecordServicesJSONRequestBody) error {
	parts := strings.SplitN(createVcRecord.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]

	if createVcRecord.Issuer != verificationMethodDID {
		return fmt.Errorf("VC issuer DID '%s' does not match the proof's verification method DID '%s'", createVcRecord.Issuer, verificationMethodDID)
	}
	if createVcRecord.Holder != createVcRecord.CredentialSubject.Id {
		return fmt.Errorf("the VC holder %s does not match the credential subject id %s", createVcRecord.Holder, createVcRecord.CredentialSubject.Id)
	}
	now := time.Now()
	if now.Before(createVcRecord.CredentialSubject.ValidFrom) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", createVcRecord.CredentialSubject.ValidFrom.Format(time.RFC3339), now.Format(time.RFC3339))
	}
	if now.After(createVcRecord.CredentialSubject.ValidUntil) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", createVcRecord.CredentialSubject.ValidUntil.Format(time.RFC3339), now.Format(time.RFC3339))
	}

	var vcRecord coreTypes.VCRecord
	hashString, err := utils.Generate256HashHex(createVcRecord)
	if err != nil {
		log.Printf("Error generating hash: %v", err)
		return err
	}
	vcRecord.ID = createVcRecord.Id
	vcRecord.Timestamp = time.Now()
	vcRecord.ExpirationDate = createVcRecord.ExpirationDate
	vcRecord.VcHash = hashString
	err = v.chain.AppendVcRecord(&vcRecord)
	if err != nil {
		log.Printf("Error appending VC record: %v", err)
		return err
	}

	return nil
}

// RevokeVCRecord revokes a VC record based on its identifier and hash
func (v *vcService) RevokeVCRecord(ctx context.Context, vcId string) error {
	if err := v.chain.RevokeVcRecord(vcId); err != nil {
		log.Printf("Error revoking VC: %s", err)
		return err
	}

	return nil
}

// containsVcRecord checks if a VC Record is in a list of VC Records
// true if the list contains this Record already
// false if the list does not contain this Record
func containsVcRecord(vcRecordList []coreTypes.VCRecord, vcId string) bool {
	for _, vcRecord := range vcRecordList {
		if vcRecord.ID == vcId {
			return true
		}
	}
	return false
}

func (v *vcService) VerifyRequestRevoke(requestBody models.RequestVcRevokeSchema) error {
	verifiedBytes, err := utils.VerifyJWS(v.chain, requestBody.Proof.Jws, requestBody.Proof.VerificationMethod)
	if err != nil {
		return err
	}
	var verified models.RequestVcRevokeSchema
	if err := json.Unmarshal(verifiedBytes, &verified); err != nil {
		return err
	}
	requestBody.Proof.Jws = "" // Because this will default to its zero value when unmarshalling verified
	if reflect.DeepEqual(requestBody, verified) {
		return nil
	} else {
		return errors.New("signed data differs from the payload")
	}
}

func interpretDIDState(state core.DidState) error {
	if state == core.DidValid {
		return nil
	} else if state == core.DidPending {
		return errors.New("did is on the list of pending transactions try again later")
	} else if state == core.DidRevoked {
		return errors.New("did is revoked")
	}
	return errors.New("did not on the blockchain")
}
