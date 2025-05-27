package domain

// TransactionResponse maps json.RawMessage to object which `swag` does understand
// this mapping is needed for the frontend
type TransactionResponse []map[string]interface{}
