package utils

import (
	"blockchain/internal/core"
	"github.com/lestrrat-go/jwx/v3/jwa"
	"github.com/lestrrat-go/jwx/v3/jws"
)

func VerfiyJWS(chain *core.Blockchain, token string, didKeyFragment string) error {
	key, err := chain.GetPublicKey(didKeyFragment)
	if err != nil {
		return err
	}

	if _, err = jws.Verify([]byte(token), jws.WithKey(jwa.RS256(), key)); err != nil {
		return err
	}
	// TODO: Compare the signed content currently unused return of jws.Verify contains the content that was signed with key - we need to compare this against the payload that was sent
	// We will need to umarshal the return value into the respected generated type and then compare them. Which is why I prepared the individual functions in server/services
	return nil
}
