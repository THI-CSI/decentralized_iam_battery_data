// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    vc, err := UnmarshalVc(bytes)
//    bytes, err = vc.Marshal()

package core

import "bytes"
import "errors"
import "time"

import "encoding/json"

func UnmarshalVc(data []byte) (Vc, error) {
	var r Vc
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *Vc) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

// Generic VC envelope with three supported claim types.
type Vc struct {
	// Defines the JSON-LD context, providing meaning to terms used in the credential.                 
	Context                                                                              *Context      `json:"@context"`
	// The subject of the credential, which must match one of the predefined claim types.              
	CredentialSubject                                                                    BmsProduction `json:"credentialSubject"`
	// The date and time after which the credential is no longer valid.                                
	ExpirationDate                                                                       *time.Time    `json:"expirationDate,omitempty"`
	// Identifier of the entity that holds the credential.                                             
	Holder                                                                               *string       `json:"holder,omitempty"`
	// Unique identifier for the Verifiable Credential.                                                
	ID                                                                                   string        `json:"id"`
	// The date and time the credential was issued.                                                    
	IssuanceDate                                                                         time.Time     `json:"issuanceDate"`
	// Identifier representing the entity that issued the credential.                                  
	Issuer                                                                               string        `json:"issuer"`
	// Cryptographic proof that makes the credential verifiable.                                       
	Proof                                                                                string        `json:"proof"`
	// Specifies the type(s) of the credential, must include 'VerifiableCredential'.                   
	Type                                                                                 []string      `json:"type"`
}

// The subject of the credential, which must match one of the predefined claim types.
type BmsProduction struct {
	// DID of the Battery Management System.                             
	//                                                                   
	// DID of the BMS to which access is granted.                        
	BmsDid                                                 string        `json:"bmsDid"`
	// Unique identifier for the BMS production credential.              
	//                                                                   
	// Unique identifier for the service access credential.              
	ID                                                     string        `json:"id"`
	// Optional lot number for the BMS production.                       
	LotNumber                                              *string       `json:"lotNumber,omitempty"`
	// Date when the BMS was produced.                                   
	ProducedOn                                             *string       `json:"producedOn,omitempty"`
	// Type indicator for a BMS production event.                        
	//                                                                   
	// Type indicator for a service access permission.                   
	Type                                                   Type          `json:"type"`
	// Level of access granted (read or write).                          
	AccessLevel                                            []AccessLevel `json:"accessLevel,omitempty"`
	// Start of the validity period for service access.                  
	ValidFrom                                              *time.Time    `json:"validFrom,omitempty"`
	// End of the validity period for service access.                    
	ValidUntil                                             *time.Time    `json:"validUntil,omitempty"`
}

type AccessLevel string

const (
	Read  AccessLevel = "read"
	Write AccessLevel = "write"
)

type Type string

const (
	BMSProduction Type = "BMSProduction"
	ServiceAccess Type = "ServiceAccess"
)

// Defines the JSON-LD context, providing meaning to terms used in the credential.
type Context struct {
	String      *string
	StringArray []string
}

func (x *Context) UnmarshalJSON(data []byte) error {
	x.StringArray = nil
	object, err := unmarshalUnion(data, nil, nil, nil, &x.String, true, &x.StringArray, false, nil, false, nil, false, nil, false)
	if err != nil {
		return err
	}
	if object {
	}
	return nil
}

func (x *Context) MarshalJSON() ([]byte, error) {
	return marshalUnion(nil, nil, nil, x.String, x.StringArray != nil, x.StringArray, false, nil, false, nil, false, nil, false)
}

func unmarshalUnion(data []byte, pi **int64, pf **float64, pb **bool, ps **string, haveArray bool, pa interface{}, haveObject bool, pc interface{}, haveMap bool, pm interface{}, haveEnum bool, pe interface{}, nullable bool) (bool, error) {
	if pi != nil {
			*pi = nil
	}
	if pf != nil {
			*pf = nil
	}
	if pb != nil {
			*pb = nil
	}
	if ps != nil {
			*ps = nil
	}

	dec := json.NewDecoder(bytes.NewReader(data))
	dec.UseNumber()
	tok, err := dec.Token()
	if err != nil {
			return false, err
	}

	switch v := tok.(type) {
	case json.Number:
			if pi != nil {
					i, err := v.Int64()
					if err == nil {
							*pi = &i
							return false, nil
					}
			}
			if pf != nil {
					f, err := v.Float64()
					if err == nil {
							*pf = &f
							return false, nil
					}
					return false, errors.New("Unparsable number")
			}
			return false, errors.New("Union does not contain number")
	case float64:
			return false, errors.New("Decoder should not return float64")
	case bool:
			if pb != nil {
					*pb = &v
					return false, nil
			}
			return false, errors.New("Union does not contain bool")
	case string:
			if haveEnum {
					return false, json.Unmarshal(data, pe)
			}
			if ps != nil {
					*ps = &v
					return false, nil
			}
			return false, errors.New("Union does not contain string")
	case nil:
			if nullable {
					return false, nil
			}
			return false, errors.New("Union does not contain null")
	case json.Delim:
			if v == '{' {
					if haveObject {
							return true, json.Unmarshal(data, pc)
					}
					if haveMap {
							return false, json.Unmarshal(data, pm)
					}
					return false, errors.New("Union does not contain object")
			}
			if v == '[' {
					if haveArray {
							return false, json.Unmarshal(data, pa)
					}
					return false, errors.New("Union does not contain array")
			}
			return false, errors.New("Cannot handle delimiter")
	}
	return false, errors.New("Cannot unmarshal union")

}

func marshalUnion(pi *int64, pf *float64, pb *bool, ps *string, haveArray bool, pa interface{}, haveObject bool, pc interface{}, haveMap bool, pm interface{}, haveEnum bool, pe interface{}, nullable bool) ([]byte, error) {
	if pi != nil {
			return json.Marshal(*pi)
	}
	if pf != nil {
			return json.Marshal(*pf)
	}
	if pb != nil {
			return json.Marshal(*pb)
	}
	if ps != nil {
			return json.Marshal(*ps)
	}
	if haveArray {
			return json.Marshal(pa)
	}
	if haveObject {
			return json.Marshal(pc)
	}
	if haveMap {
			return json.Marshal(pm)
	}
	if haveEnum {
			return json.Marshal(pe)
	}
	if nullable {
			return json.Marshal(nil)
	}
	return nil, errors.New("Union must not be null")
}
