package storage

import (
	"blockchain/internal/core"
	"bytes"
	"encoding/json"
	"io"
	"os"
)

func Load(path string, v *[]core.Block) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()

	r, err := io.ReadAll(f)
	if err != nil {
		return err
	}
	return json.Unmarshal(r, v)
}

func Save(path string, v []core.Block) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()
	r, err := json.Marshal(v)
	if err != nil {
		return err
	}
	_, err = io.Copy(f, bytes.NewReader(r))
	return err
}
