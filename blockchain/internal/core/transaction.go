package core

import (
	core "blockchain/internal/core/types"
	"crypto/sha3"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"time"
)

// PendingTransactions is a slice of transactions that make up the next block
var PendingTransactions []json.RawMessage

// CreateTrustAnchor Creates the EU DID transaction as trust anchor
// At the moment this is a Hardcoded DID Document for development
func CreateTrustAnchor() {
	PendingTransactions = PendingTransactions[:0]
	now := time.Now().UTC().Format(time.RFC3339)

	rawJSON := fmt.Sprintf(`{
  "id": "did:batterypass.eu",
  "publicKey": {
    "id": "did:batterypass.eu#root-key",
    "type": "JsonWebKey2020",
    "controller": "did:batterypass.eu",
    "publicKeyMultibase": "z6MkjYi2M3kqXFJ7o1DnzULsoZxiDsUeHcBQkNxnKUhP4YhY"
  },
  "created": "%s",
  "updated": "%s",
  "revoked": false
}`, now, now)
	PendingTransactions = append(PendingTransactions, json.RawMessage(rawJSON))
}

// AppendTransaction appends a DID or VC record as a transaction to the blockchain
func AppendTransaction(jsonData json.RawMessage) {
	if diddoc, err := core.UnmarshalDid(jsonData); err == nil {

		fmt.Println("Handled as DidSchema:", diddoc)
	} else if vcrec, err := core.UnmarshalVCRecord(jsonData); err == nil {
		// Handle VcRecordSchema
		fmt.Println("Handled as VcRecordSchema:", vcrec)
	} else {
		// Handle error
		fmt.Println("Error: JSON does not match either schema")
	}
}

// CalculateTransactionHash computes the SHA-256 hash of a transaction
func CalculateTransactionHash(tx json.RawMessage) string {
	record := fmt.Sprintf("%d%s%s", tx)
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
