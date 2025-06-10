package core

import (
	core "blockchain/internal/core/types"
	"crypto/sha3"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"time"
)

type DidState int

const (
	DidValid DidState = iota
	DidAbsent
	DidRevoked
	DidPending
)

type VCState int

const (
	VCValid VCState = iota
	VCAbsent
	VCTampered
	VCExpired
	VCPending
)

// TrustanchorPath is the relative path from tools.py to the trustanchor.json file.
// The trustanchor.json file contains the EU DID Document.
const TrustanchorPath = "internal/core/trustanchor.json"

// PendingTransactions is a slice of transactions that make up the next block
var PendingTransactions []json.RawMessage

// CreateTrustAnchor loads the EU DID transaction as a trust anchor from a file
func CreateTrustAnchor() error {
	PendingTransactions = nil

	// Read the DID document from a file
	data, err := os.ReadFile(TrustanchorPath)
	if err != nil {
		return fmt.Errorf(`failed to read trustanchor.json: %w`, err)
	}

	// Unmarshal using the generated function
	did, err := core.UnmarshalDid(data)
	if err != nil {
		return fmt.Errorf("failed to unmarshal DID document: %w", err)
	}

	// Update the timestamp field
	did.Timestamp = time.Now().UTC().Truncate(time.Second)

	// Marshal using the generated method
	modifiedData, err := did.Marshal()
	if err != nil {
		return fmt.Errorf("failed to marshal DID document: %w", err)
	}
	PendingTransactions = append(PendingTransactions, modifiedData)
	return nil
}

// AppendDid Checks a given did and adds it or calls ModifyDid
func (chain *Blockchain) AppendDid(did *core.Did) error {
	didState := chain.CheckDIDState(did.ID)
	if didState == DidPending {
		return errors.New("did is on the list of pending transactions and will be added to the blockchain soon")
	}
	if didState == DidRevoked {
		return errors.New("did is already revoked")
	}
	if didState == DidValid && !did.Revoked {
		if err := chain.ModifyDid(did); err != nil {
			return err
		}
		return nil
	} else {
		did.Timestamp = time.Now().UTC().Truncate(time.Second)
		rawJson, err := did.Marshal()
		if err != nil {
			return err
		}

		PendingTransactions = append(PendingTransactions, rawJson)

		return nil
	}
}

// ModifyDid Checks that the identifier hasn't been manipulated and appends the modified DID doc
func (chain *Blockchain) ModifyDid(did *core.Did) error {
	didOld, _ := chain.FindDID(did.ID)
	if didOld.ID != did.ID {
		return errors.New("new did does not match existing did")
	}
	did.Timestamp = time.Now()
	rawJson, err := did.Marshal()
	if err != nil {
		return err
	}
	PendingTransactions = append(PendingTransactions, rawJson)
	return nil
}

// RevokeDid revokes a given did if it's saved in the blockchain and not yet revoked
func (chain *Blockchain) RevokeDid(did string) error {
	didState := chain.CheckDIDState(did)
	if didState == DidPending {
		return errors.New("did is on the list of pending transactions try again later")
	}
	if didState == DidRevoked {
		return errors.New("did is already revoked")
	}
	if didState == DidAbsent {
		return errors.New("did does not exist")
	}
	didDoc, err := chain.FindDID(did)
	if err != nil {
		return err
	}
	didDoc.Revoked = true
	rawJson, err := didDoc.Marshal()
	if err != nil {
		return err
	}
	PendingTransactions = append(PendingTransactions, rawJson)
	return nil
}

func (chain *Blockchain) RevokeVcRecord(vcUri string) error {
	vcRecord, err := chain.FindVCRecord(vcUri)
	if err != nil {
		return err
	}
	vcHash := vcRecord.VcHash
	vcRecordState := chain.CheckVCRecordState(vcUri, vcHash)
	if vcRecordState == VCPending {
		return errors.New("vc record is on the list of pending transactions try again later")
	}
	if vcRecordState == VCExpired {
		return errors.New("vc is already expired")
	}
	if vcRecordState == VCAbsent {
		return errors.New("vc does not exist")
	}

	now := time.Now()
	vcRecord.ExpirationDate = &now
	rawJson, err := vcRecord.Marshal()
	if err != nil {
		return err
	}
	PendingTransactions = append(PendingTransactions, rawJson)
	return nil
}

// AppendVcRecord Checks a given vc record and adds it
func (chain *Blockchain) AppendVcRecord(vcRecords *core.VCRecord) error {
	vcState := chain.CheckVCRecordState(vcRecords.ID, vcRecords.VcHash)
	if vcState == VCPending {
		return errors.New("vc Record is on the list of pending transactions and will be added to the blockchain soon")
	}
	if vcState != VCAbsent {
		return errors.New(fmt.Sprintf("vc Record is already present: '%s'", vcRecords.ID))
	}

	vcRecords.Timestamp = time.Now()
	rawJson, err := vcRecords.Marshal()
	if err != nil {
		return err
	}

	PendingTransactions = append(PendingTransactions, rawJson)

	return nil
}

// CalculateTransactionHash computes the SHA-256 hash of a transaction
func CalculateTransactionHash(tx json.RawMessage) string {
	record := fmt.Sprintf("%d", tx)
	hash := sha3.Sum256([]byte(record))
	return hex.EncodeToString(hash[:])
}

// BuildMerkleRoot computes the Merkle Root from a list of transactions
func BuildMerkleRoot(txs []json.RawMessage) string {
	if len(txs) == 0 {
		return "0"
	}

	// Step 1: Hash each transaction
	hashes := make([]string, len(txs))
	for i, tx := range txs {
		hashes[i] = CalculateTransactionHash(tx)
	}

	// Step 2: Build the tree
	for len(hashes) > 1 {
		var newLevel []string

		for i := 0; i < len(hashes); i += 2 {
			// If odd number of hashes, duplicate the last
			var left = hashes[i]
			var right string
			if i+1 < len(hashes) {
				right = hashes[i+1]
			} else {
				// Duplicate the last hash
				right = left
			}
			// Concatenate and hash the pair
			combined := fmt.Sprintf("%s%s", left, right)
			hash := sha3.Sum256([]byte(combined))
			newLevel = append(newLevel, hex.EncodeToString(hash[:]))
		}

		hashes = newLevel
	}

	// Root hash is the only hash left
	return hashes[0]
}
