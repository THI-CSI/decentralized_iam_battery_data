package storage

import (
	"bytes"
	"encoding/json"
	"io"
	"os"
)

func Load(path string, v interface{}) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer func(f *os.File) {
		err := f.Close()
		if err != nil {
			print("Error closing file: %v\n", err)
		}
	}(f)

	r, err := io.ReadAll(f)
	if err != nil {
		return err
	}
	return json.Unmarshal(r, v)
}

func Save(path string, v interface{}) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer func(f *os.File) {
		err := f.Close()
		if err != nil {
			print("Error closing file: %v\n", err)
		}
	}(f)
	r, err := json.Marshal(v)
	if err != nil {
		return err
	}
	_, err = io.Copy(f, bytes.NewReader(r))
	return err
}
