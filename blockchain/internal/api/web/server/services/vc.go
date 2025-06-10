package services

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/utils"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"encoding/json"
	"errors"
	"log"
	"reflect"
	"time"
)

// VCService defines the interface for creating and returning vcs of the blockchain
type VCService interface {
	GetVCRecord(ctx context.Context, vcId string) (*coreTypes.VCRecord, error)
	GetVCRecords(ctx context.Context) (*[]coreTypes.VCRecord, error)
	CreateVCRecord(userContext context.Context, createVcRecord *models.RequestVcCreateSchema) error
	RevokeVCRecord(ctx context.Context, vcId string) error
	VerifyRequestCreate(requestBody *models.RequestVcCreateSchema) error
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

// CreateVCRecord creates a new VC record on the blockchain based on the provided VC
func (v *vcService) CreateVCRecord(userContext context.Context, createVcRecord *models.RequestVcCreateSchema) error {
	hashString, err := utils.Generate256HashHex(createVcRecord)
	if err != nil {
		log.Printf("Error generating hash: %v", err)
		return err
	}

	log.Println("after generating hash")

	var vcRecord coreTypes.VCRecord
	if vcBms, err := createVcRecord.AsVcBmsProducedSchema(); err == nil {
		vcRecord.ID = vcBms.Id
		vcRecord.Timestamp = time.Now()
		vcRecord.ExpirationDate = &vcBms.ExpirationDate
		vcRecord.VcHash = hashString
		jsonBytes, err := json.Marshal(vcBms.Proof)
		if err != nil {
			log.Printf("Error marshalling proof: %v", err)
			return err
		}
		err = json.Unmarshal(jsonBytes, &vcRecord.Proof)
		if err != nil {
			log.Printf("Error unmarshalling proof: %v", err)
			return err
		}
		err = v.chain.AppendVcRecord(&vcRecord)
		if err != nil {
			log.Printf("Error appending VC record: %v", err)
			return err
		}
	} else if vcService, err := createVcRecord.AsVcServiceAccessSchema(); err == nil {
		vcRecord.ID = vcService.Id
		vcRecord.Timestamp = time.Now()
		vcRecord.ExpirationDate = &vcService.ExpirationDate
		vcRecord.VcHash = hashString
		jsonBytes, err := json.Marshal(vcService.Proof)
		if err != nil {
			log.Printf("Error marshalling proof: %v", err)
			return err
		}
		err = json.Unmarshal(jsonBytes, &vcRecord.Proof)
		if err != nil {
			log.Printf("Error unmarshalling proof: %v", err)
			return err
		}
		err = v.chain.AppendVcRecord(&vcRecord)
		if err != nil {
			log.Printf("Error appending VC record: %v", err)
			return err
		}
	} else if vcCloud, err := createVcRecord.AsVcCloudInstanceSchema(); err == nil {
		vcRecord.ID = vcCloud.Id
		vcRecord.Timestamp = time.Now()
		vcRecord.ExpirationDate = &vcCloud.ExpirationDate
		vcRecord.VcHash = hashString
		jsonBytes, err := json.Marshal(vcCloud.Proof)
		if err != nil {
			log.Printf("Error marshalling proof: %v", err)
			return err
		}
		err = json.Unmarshal(jsonBytes, &vcRecord.Proof)
		if err != nil {
			log.Printf("Error unmarshalling proof: %v", err)
			return err
		}
		err = v.chain.AppendVcRecord(&vcRecord)
		if err != nil {
			log.Printf("Error appending VC record: %v", err)
			return err
		}
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

func (v *vcService) VerifyRequestCreate(requestBody *models.RequestVcCreateSchema) error {
	erro := utils.CheckVCSemantics(requestBody)
	if erro == nil {
		errro := errors.New("signed data differs from the payload")
		if VCBms, err := requestBody.AsVcBmsProducedSchema(); err == nil {
			verifiedBytes, err := utils.VerifyJWS(v.chain, VCBms.Proof.Jws, VCBms.Proof.VerificationMethod)
			if err != nil {
				return err
			}
			var verified models.VcBmsProducedSchema
			if err := json.Unmarshal(verifiedBytes, &verified); err != nil {
				return err
			}
			VCBms.Proof.Jws = "" // Because this will default to its zero value when unmarshalling verified
			if reflect.DeepEqual(VCBms, verified) {
				return nil
			} else {
				return errro
			}
		} else if VCService, err := requestBody.AsVcServiceAccessSchema(); err == nil {
			verifiedBytes, err := utils.VerifyJWS(v.chain, VCService.Proof.Jws, VCService.Proof.VerificationMethod)
			if err != nil {
				return err
			}
			var verified models.VcServiceAccessSchema
			if err := json.Unmarshal(verifiedBytes, &verified); err != nil {
				return err
			}
			VCService.Proof.Jws = "" // Because this will default to its zero value when unmarshalling verified
			if reflect.DeepEqual(VCService, verified) {
				return nil
			} else {
				return errro
			}
		} else if VCCloud, err := requestBody.AsVcCloudInstanceSchema(); err == nil {
			verifiedBytes, err := utils.VerifyJWS(v.chain, VCCloud.Proof.Jws, VCCloud.Proof.VerificationMethod)
			if err != nil {
				return err
			}
			var verified models.VcCloudInstanceSchema
			if err := json.Unmarshal(verifiedBytes, &verified); err != nil {
				return err
			}
			VCCloud.Proof.Jws = "" // Because this will default to its zero value when unmarshalling verified
			if reflect.DeepEqual(VCCloud, verified) {
				return nil
			} else {
				return errro
			}
		}
	}
	return erro
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
