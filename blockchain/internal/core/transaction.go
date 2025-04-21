package core

import "time"

// TransactionType defines the type of a transaction in the system.
// It is a string-based type for better readability and type safety.
type TransactionType string

const (
	// Create represents a transaction that creates a new entity or record.
	Create TransactionType = "Create"
	// Modify represents a transaction that modifies an existing entity or record.
	Modify TransactionType = "Modify"
	// Grant represents a transaction that grants permissions or access.
	Grant TransactionType = "Grant"
	// Revoke represents a transaction that revokes permissions or access.
	Revoke TransactionType = "Revoke"
)

// Transaction represents a single action recorded in the blockchain,
// such as creating, modifying, granting, or revoking something.
type Transaction struct {
	// Index is the sequential number of the transaction.
	Index int
	// Timestamp records the exact time the transaction occurred.
	Timestamp time.Time
	// Type indicates the kind of transaction, such as Create or Modify.
	Type TransactionType
	// Data holds additional information related to the transaction.
	Data string
}
