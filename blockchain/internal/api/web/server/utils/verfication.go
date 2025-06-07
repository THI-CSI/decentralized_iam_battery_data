package utils

import (
	"blockchain/internal/core"
	"github.com/lestrrat-go/jwx/v3/jwa"
	"github.com/lestrrat-go/jwx/v3/jwk"
	"github.com/lestrrat-go/jwx/v3/jws"
)

func VerfiyJWS(chain *core.Blockchain, token string, didId string) error {
	did, err := chain.FindDID(didId)
	if err != nil {
		return err
	}

	key, err := jwk.Import([]byte(did.VerificationMethod.PublicKeyMultibase))
	if err != nil {
		return err
	}

	if _, err = jws.Verify([]byte(token), jws.WithKey(jwa.RS256(), key)); err != nil {
		return err
	}

	return nil
}
