package core

import (
	"fmt"
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
			PendingTransactions = []Transaction{}

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
	fixedTimestamp := "2025-04-28 12:00:00"
	for i := range txs {
		txs[i].Timestamp = fixedTimestamp
	}
}

func TestHashTransaction(t *testing.T) {
	type args struct {
		tx []Transaction
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{
			name: "Hash a transaction with fixed timestamp",
			args: args{
				tx: []Transaction{CreateTransaction(Create, "Test data for hashing")},
			},
			want: "0051b28cdd362ad864b5f323f55301bc0587fe4623b221b3005b4278fe13584f",
		},
		// Add more test cases as needed
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set a fixed timestamp to avoid variations in the hash
			setFixedTimestamp(tt.args.tx)
			fmt.Println(tt.args.tx)
			for i := range tt.args.tx {
				if got := CalculateTransactionHash(tt.args.tx[i]); got != tt.want {
					t.Errorf("CalculateTransactionHash() = %v, want %v", got, tt.want)
				}
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
			want: "848132405a40d74bc5f06427c40840aa732037b8d4d088b24e356a8d7fb62f42",
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
