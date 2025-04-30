package core

import (
	"regexp"
)

// CheckDID, method to check if the did identifyer string aligns with our conventions
func CheckDID(did string) bool {
	var didWebPattern = `^did:[a-z0-9]+:[a-zA-Z0-9.\-_:%]+$` // Basic did pattern (refine once methods and ids are known)
	re := regexp.MustCompile(didWebPattern)
	return re.MatchString(did)
}
