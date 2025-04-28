package core

import (
	"testing"
	"time"
)

func TestCreateTransaction(t *testing.T) {
	type args struct {
		txType TransactionType
		data   string
	}
	tests := []struct {
		name string
		args args
		want Transaction
	}{
		{
			name: "Create transaction",
			args: args{
				txType: Create,
				data:   "Test transaction data",
			},
			want: Transaction{
				Header: TransactionHeader{
					Index:     0,
					Timestamp: time.Now(), // We can't compare exact time, so we can ignore this.
					Type:      Create,
					Data:      "Test transaction data",
				},
				Body: "Test transaction data",
			},
		},
		// Add more cases here if necessary
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Clear pending transactions before the test to reset index
			pendingTransactions = []Transaction{}

			got := CreateTransaction(tt.args.txType, tt.args.data)

			// Check if the index is as expected
			if got.Header.Index != tt.want.Header.Index {
				t.Errorf("CreateTransaction() Index = %v, want %v", got.Header.Index, tt.want.Header.Index)
			}
			// Check if the type is as expected
			if got.Header.Type != tt.want.Header.Type {
				t.Errorf("CreateTransaction() Type = %v, want %v", got.Header.Type, tt.want.Header.Type)
			}
			// Check if the data is as expected
			if got.Header.Data != tt.want.Header.Data {
				t.Errorf("CreateTransaction() Data = %v, want %v", got.Header.Data, tt.want.Header.Data)
			}
			// Check if the body is as expected
			if got.Body != tt.want.Body {
				t.Errorf("CreateTransaction() Body = %v, want %v", got.Body, tt.want.Body)
			}
		})
	}
}

// setFixedTimestamp Helper function to set a fixed timestamp for transactions
func setFixedTimestamp(txs []Transaction) {
	fixedTimestamp := time.Date(2025, 4, 28, 12, 0, 0, 0, time.UTC)
	for i := range txs {
		txs[i].Header.Timestamp = fixedTimestamp
	}
}

func TestHashTransaction(t *testing.T) {
	type args struct {
		tx Transaction
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{
			name: "Hash a transaction with fixed timestamp",
			args: args{
				tx: CreateTransaction(Create, "Test data for hashing"),
			},
			want: "406a766fca9b09a7f011b16e4b92b2a5cba6d9da7bec2add542594d9d137d8fc",
		},
		// Add more test cases as needed
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set a fixed timestamp to avoid variations in the hash
			setFixedTimestamp([]Transaction{tt.args.tx})

			if got := CalculateTransactionHash(tt.args.tx); got != tt.want {
				t.Errorf("CalculateTransactionHash() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestBuildMerkleRoot(t *testing.T) {
	type args struct {
		txs []Transaction
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{
			name: "Build Merkle root with multiple transactions",
			args: args{
				txs: []Transaction{
					CreateTransaction(Create, "Transaction 1"),
					CreateTransaction(Modify, "Transaction 2"),
					CreateTransaction(Grant, "Transaction 3"),
					CreateTransaction(Revoke, "Transaction 4"),
				},
			},
			want: "a058b3aa1b083461561e7e1836a46512e9f83c25bd0080dbdd4a71e8b8c0ee13",
		},
		{
			name: "Build Merkle root with no transactions",
			args: args{
				txs: []Transaction{},
			},
			want: "0",
		},
		// Add more test cases as needed
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set a fixed timestamp for all transactions to avoid variations in the hash
			setFixedTimestamp(tt.args.txs)

			if got := BuildMerkleRoot(tt.args.txs); got != tt.want {
				t.Errorf("BuildMerkleRoot() = %v, want %v", got, tt.want)
			}
		})
	}
}
