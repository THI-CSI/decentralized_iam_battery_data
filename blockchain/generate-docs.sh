#!/bin/bash

set -e

DOC_FILE="./docs/go.md"
echo "# Blockchain Go Documentation" > $DOC_FILE
echo "" >> $DOC_FILE
echo -e "\n---\n" >> $DOC_FILE

echo "Finding all packages..."
for pkg in $(go list ./... | grep -v /vendor/); do
    echo "Processing package: $pkg"
    gomarkdoc "$pkg" >> $DOC_FILE
    echo -e "\n---\n" >> $DOC_FILE
done

echo "Documentation written to $DOC_FILE"
