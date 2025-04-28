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
				Index:     0,
				Timestamp: time.Now().String(), // We can't compare exact time, so we can ignore this.
				Type:      Create,
				Data:      "Test transaction data",
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
			if got.Index != tt.want.Index {
				t.Errorf("CreateTransaction() Index = %v, want %v", got.Index, tt.want.Index)
			}
			// Check if the type is as expected
			if got.Type != tt.want.Type {
				t.Errorf("CreateTransaction() Type = %v, want %v", got.Type, tt.want.Type)
			}
			// Check if the data is as expected
			if got.Data != tt.want.Data {
				t.Errorf("CreateTransaction() Data = %v, want %v", got.Data, tt.want.Data)
			}
		})
	}
}

// setFixedTimestamp Helper function to set a fixed timestamp for transactions
func setFixedTimestamp(txs []Transaction) {
	fixedTimestamp := time.Date(2025, 4, 28, 12, 0, 0, 0, time.UTC).String()
	for i := range txs {
		txs[i].Timestamp = fixedTimestamp
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
			want: "042c966f91d2f829dbd579e3448fbe6219ae242eb77f8c786e63787838f1c997",
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
			want: "0fb4f5b88adcf61c467d451e90660e40ec847efd30902e078e910075c0e6837c",
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
