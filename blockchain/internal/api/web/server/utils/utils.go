package utils

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/core"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/golang-jwt/jwt/v5"
	"github.com/multiformats/go-multibase"
	"math/big"
	"regexp"
	"strings"
	"time"
)

// IsDidValid Checks if the DID is conformed to the specified format.
func IsDidValid(did string) bool {
	matched, _ := regexp.MatchString(`^did:batterypass:(eu|oem.|bms.|service.|cloud.)[a-zA-Z0-9.\-]*$`, did)
	return matched
}

// IsUrnValid Validates if the input string is a valid URN, according to the UUID pattern.
func IsUrnValid(urn string) bool {
	matched, _ := regexp.MatchString(`^urn:uuid:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$`, urn)
	return matched
}

// Generate256HashHex expects payload with JSON tags, marshalls it and then calculates a SHA-256 hash in hex format with that.
func Generate256HashHex(payload interface{}) (string, error) {
	jsonBytes, err := json.Marshal(payload)
	if err != nil {
		return "", err
	}
	hashBytes := sha256.Sum256(jsonBytes)
	return hex.EncodeToString(hashBytes[:]), nil
}

func VerifyJWS(chain *core.Blockchain, tokenString string, didKeyFragment string) ([]byte, error) {
	publicKeyMultibase, err := chain.GetPublicKey(didKeyFragment)
	if err != nil {
		return nil, err
	}

	// 1. Decode Multibase string
	_, decodedBytes, err := multibase.Decode(publicKeyMultibase)
	if err != nil {
		return nil, fmt.Errorf("failed to decode public key from multibase: %v", err)
	}

	// 2. Extract Multicodec and raw public key bytes
	// The multicodec for ECDSA P-256 public key is 0x1200.
	// In multicodec, it's encoded as a varint. For 0x1200, the varint is 0x8024.
	// We need to check if the decodedBytes start with the P-256 multicodec prefix.

	p256MulticodecPrefix := []byte{0x80, 0x24} // Varint encoding of 0x1200 (multicodec for P-256 public key)

	//if len(decodedBytes) < len(p256MulticodecPrefix) || !bytes.HasPrefix(decodedBytes, p256MulticodecPrefix) {
	//	return nil, fmt.Errorf("unsupported or invalid multicodec prefix for public key")
	//} // TODO: find a working format check

	rawPubKeyBytes := decodedBytes[len(p256MulticodecPrefix):]

	// 3. Parse the raw public key bytes into an ECDSA public key
	// For P-256, raw public key bytes are typically 65 bytes long:
	// 0x04 (uncompressed point indicator) followed by 32-byte X and 32-byte Y coordinates.
	curve := elliptic.P256()

	if len(rawPubKeyBytes) != 65 || rawPubKeyBytes[0] != 0x04 {
		return nil, fmt.Errorf("invalid raw P-256 public key format fetched from blockchain: expected 65 bytes starting with 0x04")
	}

	// Extract X and Y coordinates
	xBytes := rawPubKeyBytes[1 : 1+32]
	yBytes := rawPubKeyBytes[1+32 : 1+32+32]

	x := new(big.Int).SetBytes(xBytes)
	y := new(big.Int).SetBytes(yBytes)

	// Verify that the point is on the curve (crucial for security)
	if !curve.IsOnCurve(x, y) {
		return nil, fmt.Errorf("public key point is not on the P-256 curve")
	}

	ecdsaPubKey := &ecdsa.PublicKey{
		Curve: curve,
		X:     x,
		Y:     y,
	}

	// Parse and verify the JWT using ES256 (ECDSA P-256 with SHA-256)
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if token.Method.Alg() != jwt.SigningMethodES256.Alg() {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return ecdsaPubKey, nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to verify token: %v", err)
	}

	if token.Valid {
		fmt.Println("Signature verified successfully!")
		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			return nil, fmt.Errorf("could not convert claims to MapClaims")
		}

		jsonBytes, err := json.Marshal(claims)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal claims to JSON bytes: %v", err)
		}
		return jsonBytes, nil
	}

	return nil, errors.New("invalid token")
}

func VerifyRequestCreateCloud(requestBody *models.CreateVcRecordCloudJSONRequestBody) error {
	parts := strings.SplitN(requestBody.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]

	if requestBody.Issuer != verificationMethodDID {
		return fmt.Errorf("VC issuer DID '%s' does not match the proof's verification method DID '%s'", requestBody.Issuer, verificationMethodDID)
	}
	if requestBody.Holder != requestBody.CredentialSubject.Id {
		return fmt.Errorf("the VC holder %s does not match the credential subject id %s", requestBody.Holder, requestBody.CredentialSubject.Id)
	}
	now := time.Now()
	if now.Before(requestBody.CredentialSubject.Timestamp) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", requestBody.CredentialSubject.Timestamp.Format(time.RFC3339), now.Format(time.RFC3339))
	}

	return nil
}

func VerifyRequestCreateServices(requestBody *models.CreateVcRecordServicesJSONRequestBody) error {
	parts := strings.SplitN(requestBody.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]

	if requestBody.Issuer != verificationMethodDID {
		return fmt.Errorf("VC issuer DID '%s' does not match the proof's verification method DID '%s'", requestBody.Issuer, verificationMethodDID)
	}
	if requestBody.Holder != requestBody.CredentialSubject.Id {
		return fmt.Errorf("the VC holder %s does not match the credential subject id %s", requestBody.Holder, requestBody.CredentialSubject.Id)
	}
	now := time.Now()
	if now.Before(requestBody.CredentialSubject.ValidFrom) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", requestBody.CredentialSubject.ValidFrom.Format(time.RFC3339), now.Format(time.RFC3339))
	}
	if now.After(requestBody.CredentialSubject.ValidUntil) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", requestBody.CredentialSubject.ValidUntil.Format(time.RFC3339), now.Format(time.RFC3339))
	}

	return nil
}

func VerifyRequestCreateBms(requestBody *models.CreateVcRecordBmsJSONRequestBody) error {
	parts := strings.SplitN(requestBody.Proof.VerificationMethod, "#", 2)
	verificationMethodDID := parts[0]

	if requestBody.Issuer != verificationMethodDID || verificationMethodDID != requestBody.CredentialSubject.BmsDid {
		return fmt.Errorf("the following 3 dids have to match: VC Issuer: '%s'; VC credentialSubject BMSdid: '%s'; VC proof verification method: '%s'", requestBody.Issuer, requestBody.CredentialSubject.BmsDid, verificationMethodDID)
	}
	if requestBody.Holder != requestBody.CredentialSubject.Id {
		return fmt.Errorf("the VC holder %s does not match the credential subject id %s", requestBody.Holder, requestBody.CredentialSubject.Id)
	}
	now := time.Now()
	if now.Before(requestBody.CredentialSubject.Timestamp) {
		return fmt.Errorf("VC credential is not yet valid. Valid from: %s, Current time: %s", requestBody.CredentialSubject.Timestamp.Format(time.RFC3339), now.Format(time.RFC3339))
	}

	return nil
}
