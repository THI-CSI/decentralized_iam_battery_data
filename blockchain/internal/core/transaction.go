package core

import (
	core "blockchain/internal/core/types"
	"crypto/sha3"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/google/uuid"
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

// PendingTransactions is a slice of transactions that make up the next block
var PendingTransactions []json.RawMessage

// CreateTrustAnchor Creates the EU DID transaction as trust anchor
// At the moment this is a Hardcoded DID Document for development
func CreateTrustAnchor() {
	PendingTransactions = nil
	now := time.Now().UTC().Format(time.RFC3339)

	rawJSON := fmt.Sprintf(`{
  "id": "did:batterypass.eu",
  "publicKey": {
    "id": "did:batterypass.eu#root-key",
    "type": "JsonWebKey2020",
    "controller": "did:batterypass.eu",
    "publicKeyMultibase": "z6MkjYi2M3kqXFJ7o1DnzULsoZxiDsUeHcBQkNxnKUhP4YhY"
  },
  "timestamp": "%s",
  "revoked": false
}`, now)
	PendingTransactions = append(PendingTransactions, json.RawMessage(rawJSON))
}

func (chain *Blockchain) AppendDid(did *core.Did) error {
	didState := chain.VerifyDID(did.ID)
	if didState == DidPending {
		return errors.New("DID is on the list of pending transactions and will be added to the blockchain soon")
	}
	if didState == DidRevoked {
		return errors.New("DID is already revoked")
	}
	if didState == DidValid && !did.Revoked {
		return errors.New("DID already exists")
	}

	did.Timestamp = time.Now()
	rawJson, err := did.Marshal()
	if err != nil {
		return err
	}

	PendingTransactions = append(PendingTransactions, rawJson)

	return nil
}

func (chain *Blockchain) AppendVcRecords(vcRecords *core.VCRecord) error {
	vcState := chain.VerifyVCRecord(vcRecords.ID, vcRecords.VcHash)
	if vcState == VCPending {
		return errors.New("VC Record is on the list of pending transactions and will be added to the blockchain soon")
	}
	if vcState != VCAbsent {
		return errors.New(fmt.Sprintf("VC Record is already present: '%s'", vcRecords.ID))
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

func GenerateDid() string {
	id := uuid.New()
	return fmt.Sprintf("did:batterypass:%s", id.String())
}
